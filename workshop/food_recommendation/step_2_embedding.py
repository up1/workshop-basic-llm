import lancedb
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector
import pandas as pd

# Hugging Face sentence transformer embeddings
registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get("sentence-transformers").create()

class Words(LanceModel):
    search_data: str = func.SourceField()  # Text column is combinations of all columns
    Food_ID: str = func.SourceField()  # food id is food store name
    Name: str = func.SourceField()  # Name of menu
    Rating: str = func.SourceField()  # Rating given by users
    C_Type: str = func.SourceField()  # category type of food
    Veg_Non: str = func.SourceField()  # type of food its veg or non-veg
    vector: Vector(func.ndims()) = func.VectorField() # embedding vector

def create_table(food_data):
    # Create a LanceDB database
    db = lancedb.connect("./lancedb/foods")

    # Load the data
    table = db.create_table("food_recommendations", schema=Words, mode="overwrite")
    table.add(data=food_data)

    # Full text search support
    table.create_fts_index("search_data", replace=True)



if __name__ == "__main__":
    # Load the data
    food_data = pd.read_csv("./data/final_food_data.csv")
    print("Food Data Columns:")
    food_data = food_data.drop(["Unnamed: 0"], axis=1)
    print(food_data.columns.tolist())

    # Create the table
    create_table(food_data)
    print("Embedding and Table created successfully.")
