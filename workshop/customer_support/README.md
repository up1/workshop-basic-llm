# Workshop with Customer support assistant for e-commerce system
* Function calling
  * Get customer information
  * Get order information
  * Get orders by customer
  * Order operations
    * cancel order

## 1. Install dependencies
```
$pip install -r requirements.txt
```

## 2. Fake database
* Customer
* Order

Open code in file `fake_database.py`

## 3. Declare tools in Functions calling pattern
* Open code in file `tools.py`

## 4. Chat ...
```
$export OPENAI_API_KEY=your-key
$python customer_support.py
```


## 5. Working with [MCP(Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro)
* [FastMCP](https://gofastmcp.com/)

```
$pip install -r requirements.txt

$export OPENAI_API_KEY=your-key

$python python mcp_client.py
```
