# RAG Chatbot
* Frontend
  * [Streamlit](https://streamlit.io/)
* Backend
  * [FastAPI](https://fastapi.tiangolo.com/)
  * Vector database
    * [ChromaDB](https://www.trychroma.com/)

## 1. Install libraries
```
$pip install -r requirements.txt
```

## 2. Start frontend
```
$cd frontend
$streamlit run app.py
```

## 3. Start backend
```
$cd backend
$export OPENAI_API_KEY=your-key
$fastapi dev api.py
```