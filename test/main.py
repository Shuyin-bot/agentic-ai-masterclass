from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import (OpenAIChatModel)
from pydantic_ai import Agent
from dotenv import load_dotenv
import os


load_dotenv()

api_key=os.environ["OPENROUTER_API_KEY"]
model_name=os.environ["MODEL"]
print(f"key: {api_key}")


provider = OpenAIProvider(
    base_url="https://api.openai.com/v1"    ,
    api_key=api_key
)


# # pydantic-ai 会自动根据模型名称识别并调用对应的 OpenAI / OpenRouter 提供商
# # agent = Agent('openai:gpt-4o')


# model = OpenAIChatModel(
#     model_name="MODEL",
#     provider=provider,
# )

# # instantiate
# agent = Agent(
#     model=model,
#     instructions="You are a python coding agent, ..."
# )