import pandas as pd

file_path = "data/raw/BrightLearn_Raw_Data (Recovered).csv"
df = pd.read_csv(file_path)

print(df.head())
print(df.shape)
print(df.columns.tolist())

df.info()

print(df.isna().sum())

missing_customers = df[df["customer_first_name"].isna()]

print(missing_customers.shape)

print(missing_customers[
    [
        "customer_first_name",
        "customer_last_name",
        "customer_email",
        "customer_phone",
        "customer_city",
        "customer_province",
        "customer_loyalty_tier",
        "customer_since"
    ]
].isna().sum())

missing_email_only = df[
    df["customer_email"].isna()
    & df["customer_first_name"].notna()
]

print(missing_email_only.shape)

missing_category = df[df["category"].isna()]

print(missing_category.shape)

print(
    missing_category[
        ["sku", "product_name", "category"]
    ].drop_duplicates()
)

print(
    df[df["sku"] == "SKU-CLO-004"][
        ["sku", "product_name", "category"]
    ].drop_duplicates()
)

print(df["category"].value_counts())

valid_categories = df[df["category"].notna()].copy()

valid_categories["sku_prefix"] = (
    valid_categories["sku"]
    .str.split("-")
    .str[1]
)

print(
    valid_categories[
        ["sku_prefix", "category"]
    ].drop_duplicates().sort_values("sku_prefix")
)


category_map = {
    "BPC": "Beauty & Personal Care",
    "CLO": "Clothing",
    "ELE": "Electronics",
    "GRO": "Groceries",
    "HOM": "Home & Kitchen"
}

print(category_map)


clean_df = df.copy()

print(clean_df.shape)

clean_df["sku_prefix"] = (
    clean_df["sku"]
    .str.split("-")
    .str[1]
)

print(clean_df[["sku", "sku_prefix"]].head())

clean_df["category"] = clean_df["category"].fillna(
    clean_df["sku_prefix"].map(category_map)
)

print(clean_df["category"].isna().sum())

print("Raw category nulls:", df["category"].isna().sum())
print("Clean category nulls:", clean_df["category"].isna().sum())