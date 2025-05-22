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
```
$python step_1_embedding.py
```

## 4. Search data from database
```
$python step_2_query.py
```

| Operators    | Distance Function |
| -------- | ------- |
| <->  | L2 Distance|
| <=>  | Negative inner product|
| <#>  | Cosine distance|
| <+>  | L1 Distance|
