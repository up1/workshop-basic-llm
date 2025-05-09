# Workshop for Food recommendation
* Data source from [Kaggle](https://www.kaggle.com/datasets/schemersays/food-recommendation-system/data)
* Working with embedding process
* Vector database with [LanceDB](https://www.lancedb.com/)

## 1. Install libraries
```
$pip install -r requirements.txt
```

## 2. Download datasets from kaggle
```
$wget https://raw.githubusercontent.com/lancedb/vectordb-recipes/main/examples/archived_examples/Food_recommendation/main_food.csv -O ./data/main_food.csv


$wget https://raw.githubusercontent.com/lancedb/vectordb-recipes/main/examples/archived_examples/Food_recommendation/ratings.csv -O ./data/ratings.csv

```

## 3. Data processing for requirements
* Merge 2 files
* Add new column for embedding and search
* Save data to file `./data/final_food_data.csv`

```
$python step_1_data_processing.py
```

