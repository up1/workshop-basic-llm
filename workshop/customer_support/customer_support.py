from openai import OpenAI
from fake_database import FakeDatabase
from tools import tools_list
from typing import Any, Dict, List
import json

# Create Fake Database instance
database = FakeDatabase()

# OpenAI
model_name = "gpt-4.1"
client = OpenAI()

def process_tool_call(tool_name: str, tool_input: Any) -> Any:
    if tool_name == "get_customer":
        return database.get_customer(tool_input["key"], tool_input["value"])
    elif tool_name == "get_order_by_id":
        return database.get_order_by_id(tool_input["order_id"])
    elif tool_name == "get_customer_orders":
        return database.get_customer_orders(tool_input["customer_id"])
    elif tool_name == "cancel_order":
        return database.cancel_order(tool_input["order_id"])



def chat():
    system_prompt = """
    You are a customer support chat bot for an online retailer called NTL. 
    Your job is to help users look up their account, orders, and cancel orders.
    Be helpful and brief in your responses.
    You have access to a set of tools, but only use them when needed.  
    If you do not have enough information to use a tool correctly, ask a user follow up questions to get the required inputs.
    Do not call any of the tools unless you have the required data from a user. 
    """
    # Initial user message
    user_message = input("\nUser: ")
    messages = [{"role": "user", "content": [{"type": "text", "text": user_message}]}]

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

        # If the model wants to use a tool, process the tool call in openai
        tool_calls = response.choices[0].message.tool_calls
        print(tool_calls)

        if tool_calls:
            tool_use = tool_calls[0]
            tool_name = tool_use.function.name
            tool_input = tool_use.function.arguments

            print(f"OpenAI wants to use the {tool_name} tool")
            print(f"Tool Input:")
            print(json.dumps(tool_input, indent=2))

            # Run the underlying tool functionality on the fake database
            result = process_tool_call(tool_name, json.loads(tool_input))

            print(f"\nTool Result:")
            print(json.dumps(result, indent=2))

            # Append tool result message
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Assistant used the {tool_name} tool to get the result {str(result)}",
                        }
                    ],
                }
            )
        else:
            print(
                "\nNTL Assistant Support:"
                + f"{result}"
            )

        # Append assistant's message to the conversation
        print(result)
        messages.append(
            {"role": "assistant", "content": [{"type": "text", "text": str(result)}]}
        )


if __name__ == "__main__":
    chat()