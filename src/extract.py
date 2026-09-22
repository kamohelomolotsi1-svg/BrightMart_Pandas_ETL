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


# ---------------------------------------------------------
# Investigate anonymous customer transactions
# ---------------------------------------------------------

anonymous_customers = clean_df[
    clean_df["customer_first_name"].isna()
]

print("\nAnonymous customer transactions:")
print(anonymous_customers.shape)

print(
    anonymous_customers[
        [
            "customer_first_name",
            "customer_last_name",
            "customer_email",
            "customer_phone",
            "customer_city",
            "customer_province",
            "customer_loyalty_tier",
            "customer_since",
            "payment_method",
            "transaction_amount"
        ]
    ].head(10)
)


# ---------------------------------------------------------
# Investigate whether missing emails can be recovered
# ---------------------------------------------------------

known_customers_missing_email = clean_df[
    clean_df["customer_email"].isna()
    & clean_df["customer_first_name"].notna()
]

print("\nKnown customers with missing email:")
print(known_customers_missing_email.shape)

print(
    known_customers_missing_email[
        [
            "customer_first_name",
            "customer_last_name",
            "customer_phone",
            "customer_email"
        ]
    ].head(10)
)


# ---------------------------------------------------------
# Investigate all records for one customer
# ---------------------------------------------------------

musa_records = clean_df[
    (clean_df["customer_first_name"] == "Musa")
    & (clean_df["customer_last_name"] == "Ntuli")
]

print("\nAll records for Musa Ntuli:")

print(
    musa_records[
        [
            "customer_first_name",
            "customer_last_name",
            "customer_phone",
            "customer_city",
            "customer_province",
            "customer_email"
        ]
    ].drop_duplicates()
)


# ---------------------------------------------------------
# Check customer-email consistency
# ---------------------------------------------------------

customer_email_counts = (
    clean_df[
        clean_df["customer_first_name"].notna()
        & clean_df["customer_email"].notna()
    ]
    .groupby(
        [
            "customer_first_name",
            "customer_last_name",
            "customer_phone"
        ]
    )["customer_email"]
    .nunique()
    .reset_index(name="unique_email_count")
)

print("\nCustomer email consistency check:")

print(
    customer_email_counts[
        customer_email_counts["unique_email_count"] > 1
    ]
)

print(
    "\nCustomers with multiple different known emails:",
    (
        customer_email_counts["unique_email_count"] > 1
    ).sum()
)


# ---------------------------------------------------------
# Check how many missing emails are recoverable
# ---------------------------------------------------------

email_lookup = (
    clean_df[
        clean_df["customer_email"].notna()
    ]
    .drop_duplicates(
        subset=[
            "customer_first_name",
            "customer_last_name",
            "customer_phone"
        ]
    )
    .set_index(
        [
            "customer_first_name",
            "customer_last_name",
            "customer_phone"
        ]
    )["customer_email"]
)

print("\nEmail lookup sample:")
print(email_lookup.head())