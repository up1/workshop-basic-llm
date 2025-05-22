# Workshop Embedding with PostgreSQL and pgvector

## 1. Start Postgresql + pgvector
```
$docker compose up -d
$docker compose ps
```

## 2. Install dependencies
```
$pip install -r requirements.txt
```

## 3. Create embedding for existing data
* Use OpenAI's Embedding
* Generate vector from existing data
```
$python step_1_embedding.py
```

## 4. Retrieve data from database
* Keywork search
* Semantic search
* Hybrid search

```
$python step_2_retriever.py
```

| Operators    | Distance Function |
| -------- | ------- |
| <->  | L2 Distance (Euclidean distance)|
| <=>  | Negative inner product|
| <#>  | Cosine distance|
| <+>  | L1 Distance (Manhattan distance)|

## 5. Re-ranking results
* Cross-encoder

```
$python step_3_rerank.py
```