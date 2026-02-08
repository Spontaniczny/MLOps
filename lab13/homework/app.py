import asyncio
import json
from contextlib import AsyncExitStack
from openai import OpenAI
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from guardrails import Guard, OnFailAction
from guardrails.hub import LlamaGuard7B, RestrictToTopic


class MCPManager:
    def __init__(self, servers: dict[str, str]):
        self.servers = servers
        self.clients = {}
        self.tools = []  # in OpenAI format
        self._stack = AsyncExitStack()

    async def __aenter__(self):
        for url in self.servers.values():
            # initialize MCP session with Streamable HTTP client
            read, write, session_id = await self._stack.enter_async_context(
                streamable_http_client(url)
            )
            session = await self._stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            # use /list_tools MCP endpoint to get tools
            # parse each one to get OpenAI-compatible schema
            tools_resp = await session.list_tools()
            for t in tools_resp.tools:
                self.clients[t.name] = session
                self.tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": t.name,
                            "description": t.description,
                            "parameters": t.inputSchema,
                        },
                    }
                )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._stack.aclose()

    async def call_tool(self, name: str, args: dict) -> dict | str:
        # call the MCP tool with given arguments
        result = await self.clients[name].call_tool(name, arguments=args)
        return result.content[0].text


async def make_llm_request(conversation_history):
    mcp_servers = {
        "predict_weather_server": "http://localhost:8002/mcp"
    }

    vllm_client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

    async with MCPManager(mcp_servers) as mcp:
        if isinstance(conversation_history, str):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for trip planning. You are supposed to help ONLY with trip planning"
                        # "If the task is impossible based on your knowledge and tools, "
                        # "return that information."
                    ),
                },
                {"role": "user", "content": prompt},
            ]
        else:
            messages = list(conversation_history)
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for trip planning. You are supposed to help ONLY with trip planning"
                    ),
                })


        # guard: loop limit, we break as soon as we get an answer
        for _ in range(10):
            response = vllm_client.chat.completions.create(
                model="",
                messages=messages,
                tools=mcp.tools,
                tool_choice="auto",
                max_completion_tokens=1000,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}},
            )

            response = response.choices[0].message
            
            if not response.tool_calls:
                return response.content

            content = response.choices[0].message.content.strip()

            # applies all LLaMa Guard checks by default
            guard = (
                Guard()
                .use(LlamaGuard7B, on_fail=OnFailAction.EXCEPTION)
                .use(RestrictToTopic(
                    valid_topics=["trip", "trip planning", "adventure", "weather"],
                    disable_classifier=True,
                    disable_llm=False,
                    on_fail="exception")
                )
            )

            try:
                guard.validate(content)
            except Exception as e:
                return f"Sorry, I cannot help you with that, reason: {e}"

            messages.append(response)
            for tool_call in response.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"Executing tool '{func_name}'")
                func_result = await mcp.call_tool(func_name, func_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": str(func_result),
                    }
                )
        return "Error: Max turns reached without final answer"


if __name__ == "__main__":
    prompt = input("Enter your message (to quit type exit):")
    while prompt.lower() != "exit":
        response = asyncio.run(make_llm_request(prompt))
        print("Response:\n", response)
