# Step 1 :: Load data from file to Vector Database
* Log files
* PDF files
* Vector database
  * MongoDB Atlas

## 1. Install libraries
```
$pip install -r requirements.txt
```

## 2. Create Vector database
```
$docker compose up -d
$docker compose ps

NAME                  IMAGE                         COMMAND                  SERVICE   CREATED              STATUS                        PORTS
1_load_data-mongo-1   mongodb/mongodb-atlas-local   "/usr/local/bin/runn…"   mongo     About a minute ago   Up About a minute (healthy)   0.0.0.0:27017->27017/tcp
```

## 3. Load data and store in vector database
```
$export MONGODB_URL=mongodb://localhost:27017/?directConnection=true
$export MONGODB_DBNAME='logs_database'
$export LOGS_DIR='/Users/somkiatpuisungnoen/data/slide/AI/course-llm-2025/workshop/log-analysis/data/log'
$export SPRINGBOOT_GUIDE_PDF='/Users/somkiatpuisungnoen/data/slide/AI/course-llm-2025/workshop/log-analysis/data/spring-boot-reference.pdf'

$python load_data.py
```

Check data in MongoDB server
* database=logs_database
  * collections
    * logs_collection
    * devguide_collection
