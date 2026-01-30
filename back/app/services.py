from .database.schemas import User, UserOut, TextEntry
from .database.models import UserTable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from fastapi import HTTPException
from typing import Any
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from back.config.config import MODEL_CONFIG

from back.src.core.pipeline import Pipeline
from back.src.core.local_llm import ScorerV1, CriticV1
import time

scorer_llm = ScorerV1(**MODEL_CONFIG)
scorer_llm.load()

critic_llm = CriticV1(**MODEL_CONFIG)
critic_llm.load()

pipeline = Pipeline(scorer_llm, critic_llm)

_inference_executor = ThreadPoolExecutor(
    max_workers=max(2, multiprocessing.cpu_count() - 1)
)


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

                    text_entry = TextEntry(**message)

                    def run_pipeline():
                        pipeline.ingest(text_entry)
                        return list(pipeline.run())

                    time_start = time.time()
                    loop = asyncio.get_event_loop()
                    results = await loop.run_in_executor(
                        _inference_executor, run_pipeline
                    )
                    time_end = time.time()
                    print(f"Time taken: {time_end - time_start} seconds")
                    for out in results:
                        print("Out: ", out)
                        await websocket.send_text(out)

                except WebSocketDisconnect:
                    break  # client left, don't try to send
                except Exception as e:
                    print(f"Error processing message: {e}")
                    import traceback
                    traceback.print_exc()
                    try:
                        await websocket.send_text(json.dumps({
                            "error": "Error processing request",
                            "details": str(e)
                        }))
                    except (RuntimeError, Exception):
                        pass  # connection already closed
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
