#!/usr/bin/env python3

from openai import OpenAI
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Any, Dict

# OpenAI
model_name = "gpt-4o"
client = OpenAI()

# MCP Server configuration
server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"],
)


async def call_mcp_tool(session: ClientSession, tool_name: str, tool_arguments: Dict[str, Any]) -> Any:
    """Call a tool via MCP protocol"""
    result = await session.call_tool(tool_name, arguments=tool_arguments)
    
    # Extract the content from the result
    if hasattr(result, 'content') and len(result.content) > 0:
        content_item = result.content[0]
        if hasattr(content_item, 'text'):
            return json.loads(content_item.text)
    
    return result


async def chat_with_mcp():
    """Chat loop that uses MCP server for tool calls"""
    
    system_prompt = """
    You are a customer support chat bot for an online retailer called ABC. 
    Your job is to help users look up their account, orders, and cancel orders.
    Be helpful and brief in your responses.
    You have access to a set of tools, but only use them when needed.  
    If you do not have enough information to use a tool correctly, ask a user follow up questions to get the required inputs.
    Do not call any of the tools unless you have the required data from a user. 
    """
    
    messages = [{"role": "system", "content": [{"type": "text", "text": system_prompt}]}]
    
    # Connect to MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools from MCP server
            tools_response = await session.list_tools()
            
            # Convert MCP tools to OpenAI tools format
            tools_list = []
            for tool in tools_response.tools:
                tool_def = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema if hasattr(tool, 'inputSchema') else {
                            "type": "object",
                            "properties": {},
                        }
                    }
                }
                tools_list.append(tool_def)
            
            print("Connected to MCP server. Available tools:")
            for tool in tools_response.tools:
                print(f"  - {tool.name}: {tool.description}")
            print("\n")
            
            # Initial user message
            user_message = input("User: ")
            messages.append({"role": "user", "content": [{"type": "text", "text": user_message}]})
            
            while True:
                # If the last message is from the assistant, get another input from the user
                if messages[-1].get("role") == "assistant":
                    user_message = input("\nUser: ")
                    messages.append({"role": "user", "content": [{"type": "text", "text": user_message}]})
                
                # exit if user types "bye"
                if user_message.lower() == "bye":
                    print("Bye, Exiting chat.")
                    break
                
                # Get response from OpenAI model
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    tools=tools_list,
                )
                
                result = response.choices[0].message.content
                
                # If the model wants to use a tool, process the tool call via MCP
                tool_calls = response.choices[0].message.tool_calls
                
                if tool_calls:
                    tool_use = tool_calls[0]
                    tool_name = tool_use.function.name
                    tool_input = tool_use.function.arguments
                    
                    print(f"\nOpenAI wants to use the {tool_name} tool")
                    print("Tool Input:")
                    print(json.dumps(json.loads(tool_input), indent=2))
                    
                    # Call the tool via MCP protocol
                    tool_result = await call_mcp_tool(session, tool_name, json.loads(tool_input))
                    
                    print("\nTool Result:")
                    print(json.dumps(tool_result, indent=2))
                    
                    # Append tool result message
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Assistant used the {tool_name} tool to get the result {str(tool_result)}",
                                }
                            ],
                        }
                    )
                else:
                    print(
                        "\nABC Assistant Support: "
                        + f"{result}"
                    )
                    
                    # Append assistant's message to the conversation
                    messages.append(
                        {"role": "assistant", "content": [{"type": "text", "text": str(result)}]}
                    )


def main():
    """Entry point for the chat application"""
    asyncio.run(chat_with_mcp())


if __name__ == "__main__":
    main()
