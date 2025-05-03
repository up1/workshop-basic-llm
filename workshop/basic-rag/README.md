# Basic of RAG
* Read PDF file
* Chunking
* Embedding
* Vector database with [ChromaDB](https://www.trychroma.com/)


## 1. Initial Python environment
```
$python -m venv ./demo/venv
$source ./demo/venv/bin/activate
$export PATH=.:$(pwd)/demo/venv/bin/:$PATH
$alias pip=pip3
```

## 2. Install libraries
```
$pip install -r requirements.txt
```

## 3. Run step 1 to read data from PDF file
```
$python step_1_read_pdf.py
```

## 4. Cleasing and chunking data
```
$python step_2_chunking.py
```

## 5. Token spliter
``` 
$python step_3_token_split.py
```

## 6. Try to embedding token
```
$python step_4_embedding.py
```

## 7. Save to vector database
```
$python step_5_save_to_vectordb.py
```

## 8. Retrive data from vector database
```
$python step_6_retrieve.py
```

## 9. RAG with OpenAI
```
$export TOKENIZERS_PARALLELISM=false
$export OPENAI_API_KEY=<your api key>
$python step_7_rag.py
```


## Reference Websites
* https://langchain-text-splitter.streamlit.app/
* [LangChain RAG](https://python.langchain.com/docs/tutorials/rag/)