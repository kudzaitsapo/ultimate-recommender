from pathlib import Path
import uuid
import pandas as pd
import psycopg2 as py
import psycopg2.extras as extras


extras.register_uuid()

BASE_DIR = Path(__file__).resolve().parent
data_file = BASE_DIR / "data/dataset.csv"
connection_params = {"host": "db", "database": "postgres", "user": "postgres", "password": "postgres"}


def connect(params_dic):
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # connect to the PostgreSQL server
        print("[+] Connecting to the PostgreSQL database...")
        conn = py.connect(**params_dic)
    except (Exception, py.DatabaseError) as error:
        raise error

    print("[+] Connection to %s successful." % params_dic["database"])
    return conn


def execute_values(conn, df, table):
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ",".join(list(df.columns))
    # SQL quert to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, py.DatabaseError) as error:
        print("[-] Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("[+] execute_values() done")
    cursor.close()


def main():
    try:
        print("[+] Importing data from csv file.")
        dataframe = pd.read_csv(data_file)

        print("[+] Cleaning dataframe to match database.")
        dataframe = dataframe[["title", "Desc", "author", "genre", "image_link", "rating"]]
        dataframe.rename(columns={"Desc": "description"}, inplace=True)
        dataframe["id"] = [uuid.uuid4() for _ in range(len(dataframe.index))]

        db_connection = connect(connection_params)
        execute_values(db_connection, dataframe, "books_book")

        print("[+] Finished importing %d records." % len(dataframe.index))

    except Exception as e:
        print("[-] Error: %s" % str(e))


if __name__ == "__main__":
    main()
