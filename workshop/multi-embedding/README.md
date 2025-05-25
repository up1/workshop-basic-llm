# Workshop with Multi-Embedding
* Python 3.12
* [Weaviate](https://weaviate.io/)
  * Vector database

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

## 3. Start Weaviate :: Vector database on local machine
```
$docker container run --detach -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.30.1

$docker container ps
CONTAINER ID   IMAGE                                             COMMAND                  CREATED         STATUS         PORTS                                              NAMES
788fde3c54a1   cr.weaviate.io/semitechnologies/weaviate:1.30.1   "/bin/weaviate --hos…"   3 minutes ago   Up 3 minutes   0.0.0.0:8080->8080/tcp, 0.0.0.0:50051->50051/tcp   quizzical_murdock
```

## 4. Connect to database
```
$python3.12 step_1_connect_db.py
```








### Reference Websites
* https://huggingface.co/lightonai/Reason-ModernColBERT
* https://weaviate.io/developers/weaviate/tutorials/multi-vector-embeddings