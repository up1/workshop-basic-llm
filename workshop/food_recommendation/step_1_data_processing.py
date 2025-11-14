import pandas as pd

# Load the datasets
food = pd.read_csv("./data/main_food.csv")
rating = pd.read_csv("./data/ratings.csv")

# Display column names
print("Food Dataset Columns:")
print(food.columns.tolist()) 
print("Rating Dataset Columns:")
print(rating.columns.tolist())

# Merge the datasets
merged_df = pd.merge(rating, food, on="Food_ID", how="inner")
merged_df.to_csv("./data/merged_df.csv")
merged_df.head()

# Merge same "Food_ID" with different "Raing" by average rating
merged_df = merged_df.groupby("Food_ID").agg({
    "Rating": "first",
    "User_ID": "first",
    "Name": "first",
    "C_Type": "first",
    "Veg_Non": "first",
    "Describe": "first",
}).reset_index()

# Change value of non-veg to "non-vegetarian"
merged_df["Veg_Non"] = merged_df["Veg_Non"].replace({"non-veg": "non-vegetarian", "veg": "vegetarian"})


# Preprocess the data
merged_df["search_data"] = merged_df.apply(
    lambda row: f"{row['Name']} {row['C_Type']} {row['Veg_Non']}: {row['Describe']}",
    axis=1,
)
print("Merged Dataset Columns:")
print(merged_df.columns.tolist())
print("==== Preprocessed Data Sample: ====")
print(merged_df[["search_data", "Rating"]].head())

# Improve accuracy by mapping
# Create a mapping from numbers to strings with range 0-10
num_to_string = {
    0: "bad",
    1: "bad",
    2: "bad",
    3: "bad",
    4: "bad",
    5: "normal",
    6: "good",
    7: "good",
    8: "good",
    9: "good",
    10: "good",
}
# Replace numerical ratings with their string equivalents
merged_df["Rating_str"] = merged_df["Rating"].map(num_to_string)
merged_df["Rating"] = merged_df["Rating"].astype(int)
print("==== Preprocessed Data Sample: ====")
print("Search data:")
print(merged_df["search_data"][0])
print("Sample merged data:")
print(merged_df[["search_data", "Rating", "Rating_str"]].head())

# Add new column for search and embedding
merged_df["search_data"] = merged_df.apply(
    lambda row: f"{row['search_data']} ,review is {row['Rating_str']}", axis=1
)
# Save the final preprocessed data
print("==== Final Preprocessed Data Sample: ====")
print("Search data:")
print(merged_df["search_data"][0])
print(merged_df[["search_data", "Rating"]].head())

# Drop unnecessary columns
print(merged_df.columns.tolist())
merged_df = merged_df.drop(["User_ID", "Describe", "Rating_str"], axis=1)

merged_df.to_csv("./data/final_food_data.csv")
print("Successfully saved the final preprocessed data to ./data/final_food_data.csv")
