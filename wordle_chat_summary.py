# Uses iMessages in a Wordle group chat to give a summary, standings and more.
# Date: 16-11-2022
# Author: Samir Gupta

from sqlite3 import (
    Connection as SQLConnection,
    OperationalError as SQLOperationalError,
    connect as sql_db_connect,
)
from pandas import Series, read_sql_query
from os import listdir


def get_messages(connection: SQLConnection):

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
    """
    Get the database connection for the right user.
    - Returns (SQLConnection): The database connection.
    """
    # list all users
    potential_users = listdir("/Users")
    print("\nSELECT USER")
    for i, user in enumerate(potential_users, start=1):
        print(f"- {i}: {user}")

    connection: SQLConnection
    while True:
        user = input("enter user number : ") # get user to pick which user to use
        try:
            index = int(user) - 1
            connection = sql_db_connect(f"/Users/{potential_users[index]}/Library/Messages/chat.db") # get db connection
            break
        except (ValueError, IndexError):
            print("invalid user number - try again")
        except SQLOperationalError:
            print("messages not found for this user - try again")

    return connection


def get_chat_id(connection: SQLConnection) -> int:
    """
    Get the chat id of the wordle chat the user wants the information for.
    - Input:
        - connection (SQLConnection): The database connection.
    - Returns (int): The chat id. 
    """    
    all_chats_query = read_sql_query(
        """
        SELECT
            display_name, ROWID
        FROM
            chat
        WHERE
            display_name != ''
        """,
        connection,
    )  # get all group chats
    chat_names: Series[str] = all_chats_query["display_name"]  # extract the names of each chat
    chat_ids: Series[int] = all_chats_query["ROWID"]  # extract the ids of each chat

    print("\nSELECT CHAT FROM BELOW")  # print chat name options
    for i, name in enumerate(chat_names, start=1):
        print(f"- {i}: {name}")

    index: int
    while True:
        index_string = input("enter correct chat number : ")  # get user to select chat number
        try:
            index = int(index_string) - 1
            break
        except (ValueError, IndexError):
            print("invalid chat number - try again")

    return chat_ids[index]


def main():
    connection = get_db_connection()
    print(get_chat_id(connection))


if __name__ == "__main__":
    main()
