import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import re
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/trivia_db"
)

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


class TriviaQuestion(Base):
    """SQLAlchemy ORM model for trivia questions"""

    __tablename__ = "trivia_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    show_number = Column(Integer, nullable=False)
    air_date = Column(Date, nullable=True)
    round = Column(String(50), nullable=True)
    category = Column(String(255), nullable=True)
    value = Column(Integer, nullable=True)
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)

    def __repr__(self):
        return f"<TriviaQuestion(show_number={self.show_number}, category='{self.category}', value='{self.value}')>"


def parse_value(value_str):
    """
    Extract numeric value from strings like '$200', '$1,000', etc.
    Returns None if value cannot be parsed.
    """
    if pd.isna(value_str) or value_str == "None" or value_str == "":
        return None

    # Remove $ and commas, then convert to integer
    try:
        value_str = str(value_str).strip()
        numeric_value = re.sub(r"[^\d]", "", value_str)
        if numeric_value:
            return int(numeric_value)
    except (ValueError, AttributeError):
        pass

    return None


def load_and_filter_data(csv_path, max_value=1200):
    """
    Load CSV data and filter for questions with values up to max_value.

    Args:
        csv_path: Path to the CSV file
        max_value: Maximum question value to include (default: 1200)

    Returns:
        Filtered pandas DataFrame
    """
    print(f"Loading data from {csv_path}...")

    df = pd.read_csv(csv_path)

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    print(f"Total records loaded: {len(df)}")

    # Parse the Value column and filter
    df["numeric_value"] = df["Value"].apply(parse_value)

    filtered_df = df[df["numeric_value"].notna() & (df["numeric_value"] <= max_value)]
    print(f"Records with values up to ${max_value}: {len(filtered_df)}")

    return filtered_df


def clean_data(df):
    """
    Clean and prepare data for database insertion.

    Args:
        df: pandas DataFrame

    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    df["Air Date"] = pd.to_datetime(df["Air Date"], errors="coerce")

    # Strip whitespace
    string_columns = ["Round", "Category", "Question", "Answer"]
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    df["Show Number"] = (
        pd.to_numeric(df["Show Number"], errors="coerce").fillna(0).astype(int)
    )
    df["Value"] = df["Value"].apply(parse_value)

    return df


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "JEOPARDY_CSV.csv")

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    try:
        # Step 1: Create tables

        # Step 2: Load and filter data

        # Step 3: Clean data

        # Step 4: Insert data into database

        # Step 5: Verify insertion

        print("\nData ingestion completed successfully!")

    except Exception as e:
        print(f"\nError during data ingestion: {e}")
        raise


if __name__ == "__main__":
    main()
