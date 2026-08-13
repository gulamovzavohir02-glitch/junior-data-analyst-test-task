"""Run the SQL answers against small boundary-case datasets."""

from pathlib import Path
import re

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_PATH = PROJECT_ROOT / "solutions.sql"


def load_queries() -> list[str]:
    sql_text = SQL_PATH.read_text(encoding="utf-8")
    queries = re.findall(r"(?ims)^SELECT\b.*?;", sql_text)
    if len(queries) != 2:
        raise AssertionError(f"Expected 2 SELECT queries, found {len(queries)}")
    return queries


def check_rating_query(connection: duckdb.DuckDBPyConnection, query: str) -> None:
    connection.execute("CREATE TABLE examination(id INTEGER, scores INTEGER)")
    connection.execute(
        "INSERT INTO examination VALUES "
        "(1, 100), (2, 90), (3, 90), (4, 70), (5, NULL)"
    )

    actual = connection.execute(query).fetchall()
    expected = [
        (1, 100, 1),
        (2, 90, 2),
        (3, 90, 2),
        (4, 70, 4),
        (5, None, 5),
    ]
    if actual != expected:
        raise AssertionError(f"Unexpected rating result: {actual}")


def check_purchase_query(connection: duckdb.DuckDBPyConnection, query: str) -> None:
    connection.execute(
        "CREATE TABLE account("
        "id INTEGER, client_id INTEGER, open_dt DATE, close_dt DATE)"
    )
    connection.execute(
        'CREATE TABLE "transaction"('
        "id INTEGER, account_id INTEGER, transaction_date DATE, "
        "amount DECIMAL(10, 2), type VARCHAR)"
    )
    connection.execute(
        "INSERT INTO account VALUES "
        "(1, 10, current_date, NULL), (2, 10, current_date, NULL), "
        "(3, 20, current_date, NULL), (4, 30, current_date, NULL), "
        "(5, 40, current_date, NULL), (6, 50, current_date, NULL), "
        "(7, 60, current_date, NULL)"
    )
    connection.execute(
        'INSERT INTO "transaction" VALUES '
        "(1, 1, current_date, 2000, 'PUR'), "
        "(2, 2, current_date, 2499, 'PUR'), "
        "(3, 3, current_date, 6000, 'PUR'), "
        "(4, 4, current_date - INTERVAL '2 months', 100, 'PUR'), "
        "(5, 5, current_date, 100, 'REF'), "
        "(6, 6, current_date - INTERVAL '1 month', 4999, 'PUR'), "
        "(7, 7, current_date, 5000, 'PUR')"
    )

    actual = connection.execute(query).fetchall()
    expected = [(10,), (50,)]
    if actual != expected:
        raise AssertionError(f"Unexpected purchase result: {actual}")


def main() -> None:
    rating_query, purchase_query = load_queries()
    connection = duckdb.connect()
    check_rating_query(connection, rating_query)
    check_purchase_query(connection, purchase_query)
    print("SQL checks passed.")


if __name__ == "__main__":
    main()
