def validate_product_categories(raw_df, clean_df):
    """Validate the product category cleaning step."""

    if len(raw_df) != len(clean_df):
        raise ValueError(
            "Row count changed during category cleaning"
        )

    missing_categories = int(
        clean_df["category"].isna().sum()
    )

    if missing_categories != 0:
        raise ValueError(
            f"Clean data still has {missing_categories} missing categories"
        )

    print("Category validation passed")
    print("Rows checked:", len(clean_df))
    print("Missing clean categories:", missing_categories)
