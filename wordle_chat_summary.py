# Uses iMessages in a Wordle group chat to give a summary, standings and more.
# Date: 16-11-2022
# Author: Samir Gupta

from sqlite3 import (
    Connection as SQLConnection,
    OperationalError as SQLOperationalError,
    connect as sql_db_connect
)
from typing import cast
from pandas import read_sql_query, DataFrame


def get_messages(connection: SQLConnection):

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
        connection,
    )

    _ = read_sql_query(
        """
        select 
            *
        from 
            chat_handle_join c JOIN handle h on c.handle_id = h.ROWID
        where
            chat_id = 2
        """,
        connection,
    )

    print(messages)


def get_db_connection() -> SQLConnection:
    connection: SQLConnection
    while True:
        user = input("enter mac username : ")
        try:
            connection = sql_db_connect(f"/Users/{user}/Library/Messages/chat.db")
            break
        except SQLOperationalError:
            print("invalid username - try again")
    return connection


def get_chat_id(connection: SQLConnection) -> int:
    chat_name: str = ''
    chat_id_query: DataFrame = DataFrame()
    while True:
        chat_name = input("enter wordle chat name : ").lower()
        chat_id_query = read_sql_query(
            f"""
            SELECT
                ROWID
            FROM
                chat
            WHERE
                LOWER(display_name) = "{chat_name}"
            """,
            connection,
        )
        try: 
            if chat_id_query.empty or not chat_name:
                raise ValueError
            break
        except:
            print('invalid chat name - try again')

    return int(cast(str, chat_id_query["ROWID"][0]))


def main():
    connection = get_db_connection()
    print(get_chat_id(connection))


if __name__ == "__main__":
    main()
