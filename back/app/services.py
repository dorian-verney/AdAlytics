from .database.schemas import User, UserOut
from .database.models import UserTable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from fastapi import HTTPException
from typing import Any
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from typing import Generator
from back.config.config import MODEL_CONFIG
from back.src.rag.embedder import embed
from back.src.rag.retriever import retrieve
from back.src.rag.indexer import build_context
from back.src.rag.vector_store import collection

from back.src.core.local_llm import ScorerV1, CriticV1
from llama_cpp import Llama

scorer_llm = ScorerV1(**MODEL_CONFIG)
scorer_llm.load()

critic_llm = CriticV1(**MODEL_CONFIG)
critic_llm.load()

def get_context(main_text: str) -> str:
    """
    Get the context for the ad by embedding the main text and 
    retrieving the most relevant chunks
    """
    query_emb = embed([main_text])[0].tolist()
    results = retrieve(collection, query_emb)
    context = build_context(results)
    return context


async def token_progress_stream(main_text: str, context: str) -> Generator[str, int]:
    """
    Token and progress stream that handles the scoring and feedback
    First phase, the scorer yield scores and progress
    Then the critic yields suggestions and progress
    """
    # PHASE 1: The Scorer (generates scores and justification) ---
    scores_result = None
    for result, progress in scorer_llm.stream(main_text, context):
        if result is None:
            # This is just a progress update
            yield json.dumps({"stage": "scorer", "progress": progress})
        else:
            # This is the final parsed result
            scores_result = result
            yield json.dumps({"stage": "scorer", "result": result, "progress": 100})
        # Yield control to event loop so websocket sends happen immediately
        await asyncio.sleep(0)

    # PHASE 2: The Critic (generates suggestions and new_ad) ---
    # Convert scores_result dict to string for the prompt
    scores_str = json.dumps(scores_result) if scores_result else "{}"
    for result, progress in critic_llm.stream(main_text, scores_str, context):
        if result is None:
            # This is just a progress update
            yield json.dumps({"stage": "critic", "progress": progress})
        else:
            # This is the final parsed result
            yield json.dumps({"stage": "critic", "result": result, "progress": 100})
        # Yield control to event loop so websocket sends happen immediately
        await asyncio.sleep(0)



def db_obj_to_dict(obj: Any) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class Services:
    @staticmethod
    async def read_root():
        return {"message": "Hello, World!"}


    @staticmethod
    async def create_user(user: User, db_session: AsyncSession) -> UserOut:
        user_entry = UserTable(**user.model_dump())
        db_session.add(user_entry)
        await db_session.commit()
        await db_session.refresh(user_entry)
        return user_entry


    @staticmethod
    async def read_users(db_session: AsyncSession) -> list[UserOut]:
        res = await db_session.execute(text(f"select * from {UserTable.__tablename__}"))
        return [UserOut(**dict(row)) for row in res.mappings().all()]


    @staticmethod
    async def read_user(user_id: int, db_session: AsyncSession) -> UserOut:
        result = await db_session.execute(
            select(UserTable).where(UserTable.id == user_id)
        )
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user


    @staticmethod
    async def update_user(user_id: int, new_user: User, db_session: AsyncSession) -> UserOut:
        result = await db_session.execute(
            select(UserTable).where(UserTable.id == user_id)
        )
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.email = new_user.email
        user.password = new_user.password
        await db_session.commit()
        await db_session.refresh(user)
        return user

    @staticmethod
    async def delete_user(user_id: int, db_session: AsyncSession) -> dict:
        try:
            result = await db_session.execute(
                select(UserTable).where(UserTable.id == user_id)
            )
            user = result.scalars().first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            await db_session.delete(user)
            await db_session.commit()
            return {"success": True, "message": "User deleted successfully"}

        except Exception as e:
            await db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))



    #### Login
    @staticmethod
    async def login(user: User, db_session: AsyncSession) -> dict:
        result = await db_session.execute(
            select(UserTable).where(UserTable.email == user.email)
        )
        db_user = result.scalars().first()
        if db_user is None:
            # create user if not exists
            new_user = await Services.create_user(user, db_session)
            return {"success": True, 
                    "message": "User created successfully", 
                    "user": db_obj_to_dict(new_user)}
        else:
            if db_user.password != user.password:
                return {"success": False, "message": "Invalid password"}
            return {"success": True, 
                    "message": "User logged in successfully", 
                    "user": db_obj_to_dict(db_user)}


    @staticmethod
    async def websocket_endpoint(websocket: WebSocket):
        """
        WebSocket endpoint that handles bidirectional communication.
        Clients send messages and receive predictions on the same connection.
        """
        await websocket.accept()
        print("WebSocket client connected")

        try:
            while True:
                try:
                    # Wait for messages from this client
                    data = await websocket.receive_text()
                    message = json.loads(data)

                    main_text = message.get("main_text", "")
                    # TODO incorporate into context
                    additional_context = message.get("additional_context", "")

                    context = get_context(main_text)

                    async for data in token_progress_stream(main_text, context):
                        await websocket.send_text(data)
                
                except Exception as e:
                    print(f"Error processing message: {e}")
                    import traceback
                    traceback.print_exc()
                    # Send error back to client but keep connection open
                    await websocket.send_text(json.dumps({
                        "error": "Error processing request",
                        "details": str(e)
                    }))
        except WebSocketDisconnect:
            print("WebSocket client disconnected")
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            import traceback
            traceback.print_exc()
            try:
                await websocket.close()
            except:
                pass