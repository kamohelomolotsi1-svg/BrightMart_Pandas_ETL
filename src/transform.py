import pandas as pd


def clean_product_categories(df):
    """Fill missing product categories using SKU prefixes."""

    clean_df = df.copy()

    category_map = {
        "BPC": "Beauty & Personal Care",
        "CLO": "Clothing",
        "ELE": "Electronics",
        "GRO": "Groceries",
        "HOM": "Home & Kitchen"
    }

    sku_prefix = clean_df["sku"].str.split("-").str[1]

    missing_category_mask = clean_df["category"].isna()

    clean_df.loc[
        missing_category_mask, "category"
    ] = sku_prefix.loc[missing_category_mask].map(category_map)

    return clean_df
