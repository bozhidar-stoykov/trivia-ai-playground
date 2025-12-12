# Data Ingestion Script

This script ingests trivia questions from the Jeopardy CSV dataset and stores them in a PostgreSQL database using SQLAlchemy ORM.

## Features

- Loads data from `JEOPARDY_CSV.csv`
- Filters questions with monetary values up to $1200
- Creates a PostgreSQL database schema using SQLAlchemy ORM
- Performs batch insertion for optimal performance
- Includes data validation and verification

## Requirements

- Python 3.8+
- PostgreSQL database
- Required Python packages (see requirements.txt)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database:
```sql
CREATE DATABASE trivia_db;
```

## Configuration

The script uses the following database connection string by default:
```
postgresql://postgres:postgres@localhost:5432/trivia_db
```

You can override this by setting the `DATABASE_URL` environment variable:

```bash
# Windows PowerShell
$env:DATABASE_URL = "postgresql://username:password@host:port/database"

# Linux/Mac
export DATABASE_URL="postgresql://username:password@host:port/database"
```

## Usage

Run the ingestion script:

```bash
python ingestion_script.py
```

The script will:
1. Create the `trivia_questions` table if it doesn't exist
2. Load and filter data from the CSV (values up to $1200)
3. Clean and prepare the data
4. Insert the data into PostgreSQL
5. Verify the insertion with sample records

## Database Schema

The script creates a `trivia_questions` table with the following columns:

| Column       | Type         | Description                                    |
|--------------|--------------|------------------------------------------------|
| id           | Integer      | Auto-incrementing primary key                  |
| show_number  | Integer      | Unique identifier for the show                 |
| air_date     | Date         | The show air date                              |
| round        | String(50)   | Round type (Jeopardy!, Double Jeopardy!, etc.) |
| category     | String(255)  | Question category                              |
| value        | Integer      | Monetary value (e.g., 200)                    |
| question     | Text         | The trivia question                            |
| answer       | Text         | The correct answer                             |

## Data Filtering

The script filters for questions with values up to $1200, which includes:
- $200
- $400
- $600
- $800
- $1000
- $1200

Questions with no value or values above $1200 are excluded.

## Example Output

```
Creating database tables...
Tables created successfully!
Loading data from data/JEOPARDY_CSV.csv...
Total records loaded: 216930
Records with values up to $1200: 162141
Inserting data into database...
Cleared existing data.
Inserted 162141 records into the database!

Verification: Total records in database: 162141

Sample records:
  - Show: 4680, Category: HISTORY, Value: 200
  - Show: 4680, Category: ESPN's TOP 10 ALL-TIME ATHLETES, Value: 200
  ...

Data ingestion completed successfully!
```

## Troubleshooting

**Database Connection Error:**
- Ensure PostgreSQL is running
- Verify the connection credentials
- Check that the database exists

**CSV File Not Found:**
- Verify the CSV file is located in `data/JEOPARDY_CSV.csv`
- Check file permissions

**Import Errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
