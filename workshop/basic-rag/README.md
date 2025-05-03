# Basic of RAG
* Read PDF file
* Chunking
* Embedding


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




## Reference Websites
* https://langchain-text-splitter.streamlit.app/
* [LangChain RAG](https://python.langchain.com/docs/tutorials/rag/)