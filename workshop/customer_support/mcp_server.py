#!/usr/bin/env python3

import json
from fastmcp import FastMCP
from fake_database import FakeDatabase

# Create Fake Database instance
database = FakeDatabase()

# Create FastMCP server
mcp = FastMCP("Customer Support")

@mcp.tool()
def get_customer(key: str, value: str) -> str:
    """Looks up a customer by email, phone, or username.
    
    Args:
        key: The attribute to search for a customer by (email, phone, username)
        value: The value to match for the specified attribute
    """
    if key not in ["email", "phone", "username"]:
        result = {"error": f"Invalid key: {key}. Must be one of: email, phone, username"}
    else:
        result = database.get_customer(key, value)
        if isinstance(result, str):  # Error message
            result = {"error": result}
    
    return json.dumps(result)

@mcp.tool()
def get_order_by_id(order_id: str) -> str:
    """Retrieves the details of a specific order based on the order ID.
    
    Args:
        order_id: The unique identifier for the order
    """
    result = database.get_order_by_id(order_id)
    
    if result is None:
        result = {"error": f"Order with ID {order_id} not found"}
        
    return json.dumps(result)

@mcp.tool()
def get_customer_orders(customer_id: str) -> str:
    """Retrieves the list of orders belonging to a customer based on the customer's ID.
    
    Args:
        customer_id: The customer ID to get orders for
    """
    result = database.get_customer_orders(customer_id)
    return json.dumps(result)

@mcp.tool()
def cancel_order(order_id: str) -> str:
    """Cancels an order based on a provided order_id. Only orders that are 'processing' can be cancelled.
    
    Args:
        order_id: The order ID pertaining to a particular order
    """
    result = database.cancel_order(order_id)
    return json.dumps({"message": result})

if __name__ == "__main__":
    mcp.run()