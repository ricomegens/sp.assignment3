import psycopg2
import os
import dotenv
database = "huwebshop_test"


def run_query(query, arguments=None, fetch=False):
    # loading env file for password
    dotenv.load_dotenv()
    # connect to the database
    con = psycopg2.connect(host="localhost",
                           database=database,
                           user="postgres",
                           password=os.getenv("PASSWORD"))
    # create cursor
    cur = con.cursor()
    # execute a query for inserting the given data to the database
    cur.execute(query, arguments)
    data = cur.fetchall()
    # commit queries and close cursor and connection
    con.commit()
    cur.close()
    con.close()
    if not fetch:
        return
    return data