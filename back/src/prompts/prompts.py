def score_prompt(context: str, ad_text: str) -> str:
    prompt = f"""
                You are an expert ad evaluator.
                Use ONLY the context.
                Return JSON. 

                Context:
                {context}

                Ad:
                {ad_text}

                Output format:
                {{
                    "clarity": "0-10",
                    "brand_alignment": "0-10",
                    "compliance": "0-10",
                    "conversion": "0-10",
                    "justification": "..."
                }}
                """
    return prompt


def improve_prompt(context: str, ad_text: str, scores: str) -> str:
    prompt = f"""
                You are a marketing consultant.
                Use the context and scores to improve the ad:
                1. Suggest 3 improvements as suggestions
                2. Rewrite the ad as a new_ad
                Return JSON.

                Context:
                {context}

                Scores:
                {scores}

                Ad:
                {ad_text}

                Output format:
                {{
                    "suggestions": ["...", "...", "..."],
                    "new_ad": "..."
                }}
                

                """ 
    return prompt