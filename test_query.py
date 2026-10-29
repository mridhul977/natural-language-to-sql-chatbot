
from sql_generator import generate_sql
from sql_validator import validate_sql
from database import execute_sql

question = input("Enter your question: ")

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)

if not validate_sql(sql):
    print("\nQuery rejected: only permitted SELECT queries are allowed.")
else:
    try:
        results = execute_sql(sql)

        print("\nQuery results:")
        for row in results:
            print(row)

    except Exception as error:
        print("\nQuery execution failed:", error)
