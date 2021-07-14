Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@awaudun 
hahnjas
/
python-exercise-solutions
Private
2
30
Code
Issues
Pull requests
Actions
Projects
Security
Insights
python-exercise-solutions/etl/cdc/cdc_using_sql/example_solution/exercise_2_advanced.py /
@pehe2217
pehe2217 Add example solution for cdc, exercise 2
Latest commit 35d8fe7 9 days ago
 History
 1 contributor
137 lines (116 sloc)  5.26 KB
  
from typing import List

import psycopg2


# Let's define some global variables we will be using.
# See them as constants, they will never be changed.
SOURCE_DB_NAME = "cdc_source_db"
DESTINATION_DB_NAME = "cdc_datawarehouse"
DESTINATION_SCHEMA_NAME = "staging"
TABLE_NAME = "product_line"
COLUMNS = ["product_line_id", "product_line", "manager", "updated_at"]
PASSWORD = "postgres"
PORT = 9999


def get_rows_from_source_table():
    """
    ###########################################
    # Step 1: Extract from the source table   #
    ###########################################
    Returns a list of tuples. One tuple is one row in the source database.
    """
    # You need a connection to your source database.
    # Make sure the `dbname` and the rest of the config is right.
    # Here, we are using the concept of context manager.
    # When writing more advanced code, we want to use the 'with' keyword
    # to open and close a resource in a safe way.
    # If you are curious to learn more about the subject, please see e.g.
    # https://realpython.com/python-with-statement/
    with psycopg2.connect(
        host="localhost",
        dbname=SOURCE_DB_NAME,
        user="postgres",
        password=PASSWORD,
        port=PORT,
    ) as connection_source_db:
        # Now, let's get a cursor. For doing that, let's use the 'with' keyword:
        with connection_source_db.cursor() as cursor:
            # Now we have instantiated the cursor variable.
            cursor.execute(f"select * from {TABLE_NAME};")
            list_of_rows = cursor.fetchall()
        # Usually, here we close the cursor by typing:
        # cursor.close()
        # But when using the "with" keyword, we don't need to do that.
        # It's closed implicitly for us when we exit the code block.

    # And usually we need to close our connection object:
    # connection_source_db.close()
    # But beause we created our connection object using the "with" keyword
    # we don't need to close it, it's closed implicitly for us
    # when we exit the code block.
    return list_of_rows


def get_insert_query(
    schema_name: str, table_name: str, columns: List[str], list_of_rows: List[tuple]
):
    """
    This function is a big hackz.
    I don't require you to come up with the same solution yourself.
    I don't require you to under stand all of it.
    You can go ahead and copy this function and use it somewhere else,
    You can execute the function to get an arbitrary INSERT query.
    Returns a SQL query of type str, ready to be executed.
    Inputs:
    - `schema_name` is of type string
    - `table_name` is of type string
    - `columns` is of type list, containing strings
    - `list_of_rows` is of type list, containing tuples
    # Hackz from here:
    # https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
    """
    columns_str = ", ".join(columns)  # The resulting string: 'product_line_id, product_line, manager, updated_at'
    list_w_percent_s = ["%s"] * len(list_of_rows)  # Resulting list: ['%s', '%s', '%s', '%s', '%s', '%s', '%s']
    records_list_template = ", ".join(list_w_percent_s)  # Resulting string: '%s, %s, %s, %s, %s, %s, %s'
    insert_query = f"INSERT INTO {schema_name}.{table_name} ({columns_str}) VALUES {records_list_template}"
    # The resulting string looks like this:
    # 'INSERT INTO staging.product_line (product_line_id, product_line, manager, updated_at) VALUES %s, %s, %s, %s, %s, %s, %s'
    return insert_query


def load_into_destination_table(list_of_rows: List[tuple]):
    """
    ###########################################
    # Step 2: Load into the destination table #
    ###########################################
    """
    # First, let's get a SQL insert query,
    # ready to be executed against the database:
    insert_query = get_insert_query(
        schema_name=DESTINATION_SCHEMA_NAME,
        table_name=TABLE_NAME,
        columns=COLUMNS,
        list_of_rows=list_of_rows,
    )

    # Then, let's set up a connection the the db.
    # Remember, we are connecting to the destination db this time,
    # as that's where we want to write to.
    # Here, we instantiate a connection object by using the "with"
    # keyword. Please read comment above for details about the "with" keyword.
    with psycopg2.connect(
        host="localhost",
        dbname=DESTINATION_DB_NAME,
        user="postgres",
        password=PASSWORD,
        port=PORT,
    ) as connection_destination_db:
        # Here, the "with" code block starts for the connection.

        with connection_destination_db.cursor() as cursor:
            # Here, the "with" code block starts for the cursor.
            cursor.execute(insert_query, list_of_rows)
        # The cursor is closed implicitly
        # after exiting the second "with" code block.

        # In this case, we execute an INSERT query.
        # Therefore, before we close the connection
        # we need to commit our changes to the database.
        connection_destination_db.commit()

    # The connection is closed implicitly
    # after exiting the first "with" code block.
    # And we are done! 

if __name__ == "__main__":
    # Step 1: Extract from the source table
    list_of_rows = get_rows_from_source_table()

    # Step 2: Load into the destination table
    load_into_destination_table(list_of_rows)
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Loading complete