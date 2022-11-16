# Uses iMessages in a Wordle group chat to give a summary, standings and more.
# Date: 16-11-2022
# Author: Samir Gupta

from sqlite3 import (
    connect as sql_db_connect,
    Connection as SQLConnection,
    OperationalError as SQLOperationalError,
)
from pandas import read_sql_query


def get_messages(conn: SQLConnection):

    # get the 10 entries of the message table using pandas
    messages = read_sql_query(
        """
        select 
            m.ROWID as message_id, 
            text,
            id as phone,
            datetime(date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime") as date_uct 
        from 
            (message m JOIN chat_message_join c ON m.ROWID = c.message_id) JOIN handle h on h.ROWID = m.handle_id
        where
            chat_id = (
                select ROWID from chat where LOWER(display_name) = "wordle crew"
            )
        """,
        conn,
    )

    chat = read_sql_query(
        """
        select 
            *
        from 
            chat_handle_join c JOIN handle h on c.handle_id = h.ROWID
        where
            chat_id = 2
        """,
        conn,
    )

    print(messages)


def get_db_connection() -> SQLConnection:
    conn: SQLConnection
    while True:
        user = input("enter mac username : ")
        try:
            conn = sql_db_connect(f"/Users/{user}/Library/Messages/chat.db")
            break
        except SQLOperationalError:
            print("invalid username - try again")
    return conn


def main():
    conn = get_db_connection()

    # connect to the database
    cur = conn.cursor()
    # get the names of the tables in the database
    cur.execute(" select name from sqlite_master where type = 'table' ")

    get_messages(conn)


if __name__ == "__main__":
    main()
