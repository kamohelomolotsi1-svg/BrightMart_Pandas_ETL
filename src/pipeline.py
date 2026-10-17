from src.extract_module import extract_brightmart_csv
from src.transform import clean_product_categories
from src.validate import validate_product_categories


def run_pipeline():
    """Run the BrightMart extraction, transformation and validation."""

    file_path = "data/raw/BrightLearn_Raw_Data (Recovered).csv"

    print("\nSTEP 1: EXTRACT")
    raw_df = extract_brightmart_csv(file_path)
    print("Rows extracted:", len(raw_df))

    print("\nSTEP 2: TRANSFORM")
    clean_df = clean_product_categories(raw_df)
    print("Rows transformed:", len(clean_df))

    print("\nSTEP 3: VALIDATE")
    validate_product_categories(raw_df, clean_df)

    print("\nBrightMart pipeline completed successfully")

    return clean_df


if __name__ == "__main__":
    run_pipeline()
