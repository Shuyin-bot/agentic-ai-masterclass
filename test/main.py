# 导入环境变量工具
from dotenv import load_dotenv
import os
# 导入异步工具
import asyncio
# 用于格式化打印
import dataclasses
import json
# 导入模型厂商，模型和实例化agent方法
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai import Agent

# 加载 .env 文件中的环境变量到系统里（默认找当前目录）
load_dotenv()

# 从环境变量读取配置
provider = OpenAIProvider(
    base_url=os.getenv("OPENROUTER_API_BASE"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

model = OpenAIChatModel(
    model_name=os.getenv("MODEL"),
    provider=provider,
)

# pydantic-ai 会自动根据模型名称识别并调用对应的 OpenAI / OpenRouter 提供商
# agent = Agent(model)

# instantiate an agent
agent = Agent(
    model=model,
    instructions="You are a python coding agent, ..."
)

async def main():
    # --- 第一轮：发起任务 ---
    print("--- 发起指令: 指示 agent 查找 PyData 上关于 agentic AI 的最新三场演讲 ---")
    # await 语法规定只能在异步函数内使用
    result1 = await agent.run("查找 PyData 上关于 agentic AI 的最新三场演讲。")
    
    # 关键点：用 .all_messages() 抓取刚才产生的所有对话和工具调用历史（对应 PDF 12-15 页的 JSON）
    # print("--- print new messages ---")
    # 将消息（一长串python对象）转换为词典列表
    # json_new_msg = [dataclasses.asdict(msg) for msg in result1.new_messages()]
    # print(json.dumps(json_new_msg, indent=2, ensure_ascii=False, default=str))
    # print("--- print all messages ---")
    # print(result1.all_messages())
    print("--- print output ---")
    print(result1.output)
    print("--- print usage ---")
    print(result1.usage())
#     print("--- 第一轮结束 ---")

    # --- 第二轮：带着历史继续聊 ---
    # 把第一轮的 history 传给 message_history，模型就能“看到”刚才查到的网页和工具结果！
    result2 = await agent.run(
        "太棒了！请根据这些演讲内容，帮我写一篇简短的 LinkedIn 动态。", 
        message_history=result1.all_messages()
    )
    
    print("\n--- 第二轮（连接历史后的）回答 ---")
    print(result2.output)
    print("--- print usage ---")
    print(result1.usage())

if __name__ == "__main__":
    asyncio.run(main())