import pandas as pd
from pathlib import Path


def load_csv(file_path):
    """
    Load a CSV file and return it as a pandas DataFrame.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return pd.read_csv(file_path)


def save_csv(dataframe, file_path):
    """
    Save a pandas DataFrame to a CSV file.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dataframe.to_csv(
        file_path,
        index=False
    )


def check_required_columns(dataframe, required_columns):
    """
    Check whether all required columns exist.
    """

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return True


def get_unique_count(dataframe, column):
    """
    Return the number of unique values in a column.
    """

    if column not in dataframe.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    return dataframe[column].nunique()


if __name__ == "__main__":

    print("Data utility functions loaded successfully.")