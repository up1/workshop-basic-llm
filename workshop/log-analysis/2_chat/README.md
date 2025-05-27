# Chat with data from MongoDB
* RAG
* UI with [Gradio](https://www.gradio.app/)
* Local LLM with Ollama


## 1. Install libraries
```
$pip install -r requirements.txt
```

## 2. Run app
```
$export MONGODB_URL=mongodb://localhost:27017/?directConnection=true
$export MONGODB_DBNAME='logs_database'

$python app.py

```


