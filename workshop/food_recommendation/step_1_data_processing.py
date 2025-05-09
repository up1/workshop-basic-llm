import pandas as pd

# Load the datasets
food = pd.read_csv("./data/main_food.csv")
rating = pd.read_csv("./data/ratings.csv")

# Display column names
print("Food Dataset Columns:")
print(food.columns.tolist()) 
print("Rating Dataset Columns:")
print(rating.columns.tolist())

# Drop unnecessary columns
food.dropna(axis=0 ,inplace=True)
rating.dropna(axis=0 ,inplace=True)

# Merge the datasets
merged_df = pd.merge(food, rating, on="Food_ID")
merged_df.to_csv("./data/merged_df.csv")
merged_df.head()
print("Merged Dataset Columns:")
print(merged_df.columns.tolist())

# Preprocess the data
merged_df["search_data"] = merged_df.apply(
    lambda row: f"{row['Name']} {row['C_Type']} {row['Veg_Non']}: {row['Describe']}",
    axis=1,
)
print("==== Preprocessed Data Sample: ====")
print(merged_df[["search_data", "Rating"]].head())

# Improve accuracy by mapping
# Create a mapping from numbers to strings
num_to_string = {
    0.0: "zero",
    1.0: "one",
    2.0: "two",
    3.0: "three",
    4.0: "four",
    5.0: "five",
    6.0: "six",
    7.0: "seven",
    8.0: "eight",
    9.0: "nine",
    10.0: "ten",
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
    lambda row: f"{row['search_data']} rating: {row['Rating']} {row['Rating_str']}", axis=1
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
