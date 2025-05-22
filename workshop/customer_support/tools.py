tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_customer",
            "description": "Looks up a customer by email, phone, or username.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "enum": ["email", "phone", "username"],
                        "description": "The attribute to search for a customer by (email, phone, or username).",
                    },
                    "value": {
                        "type": "string",
                        "description": "The value to match for the specified attribute.",
                    }
                },
                "required": ["key", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_by_id",
            "description": "Retrieves the details of a specific order based on the order ID. Returns the order ID, product name, quantity, price, and order status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique identifier for the order.",
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_orders",
            "description": "Retrieves the list of orders belonging to a customer based on the customer's ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer_id belonging to the customer",
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancels an order based on a provided order_id. Only orders that are 'processing' can be cancelled",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order_id pertaining to a particular order",
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]
