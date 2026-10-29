
import sqlglot


def validate_sql(query):
    try:
        statements = sqlglot.parse(query, read="mysql")

        # Allow exactly one SQL statement.
        if len(statements) != 1 or statements[0] is None:
            return False

        statement = statements[0]

        # Allow only SELECT queries at this stage.
        if statement.key.upper() != "SELECT":
            return False

        return True

    except Exception:
        return False
