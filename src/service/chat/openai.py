from openai import OpenAI


class ChatService:
    def __init__(self, base_url:str, api_key: str):
        self.client: OpenAI = OpenAI(base_url=base_url, api_key=api_key)

    async def validate_task(self, text: str):
        res = await self.client.responses.create(model="gpt-4.1-nano", input=text)

client =
