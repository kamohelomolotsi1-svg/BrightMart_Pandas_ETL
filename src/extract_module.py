import pandas as pd
from pathlib import Path


def extract_brightmart_csv(file_path):
    """Read the BrightMart CSV file."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Source CSV not found: {path}"
        )

    df = pd.read_csv(
        path,
        dtype={"customer_phone": "string"}
    )

    return df
