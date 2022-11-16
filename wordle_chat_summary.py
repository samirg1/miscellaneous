# Uses iMessages in a Wordle group chat to give a summary, standings and more.
# Date: 16-11-2022
# Author: Samir Gupta

from os import listdir
from sqlite3 import Connection, OperationalError, connect
from typing import Generator, Iterable, cast

from pandas import Series, read_sql_query


class User:
    def __init__(self, name: str, number: str):
        self._name = name
        self._number = number
        self._games: dict[int, int] = {}

    def __repr__(self) -> str:
        return f"({self._name}, {self._number}"


def get_db_connection() -> Connection:
    """
    Get the database connection for the right user.
    - Returns (Connection): The database connection.
    """
    # list all users
    potential_users = listdir("/Users")
    print("\nSELECT USER")
    for i, user in enumerate(potential_users, start=1):
        print(f"- {i}: {user}")

    connection: Connection
    while True:
        user = input("enter user number : ")  # get user to pick which user to use
        try:
            index = int(user) - 1
            connection = connect(f"/Users/{potential_users[index]}/Library/Messages/chat.db")  # get db connection
            break
        except (ValueError, IndexError):
            print("invalid user number - try again")
        except OperationalError:
            print("messages not found for this user - try again")

    return connection


def get_chat_id(connection: Connection) -> int:
    """
    Get the chat id of the wordle chat the user wants the information for.
    - Input:
        - connection (Connection): The database connection.
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


def get_chat_members(connection: Connection, chat_id: int) -> list[User]:
    """
    Get the members of a particular chat.
    - Input:
        - connection (Connection): The database connnection.
        - chat_id (int): The chat id of the chat to find members of.
    - Returns (list[User]): The list of members.
    """
    numbers: Series[str] = read_sql_query(
        f"""
        SELECT 
            id
        FROM 
            chat_handle_join c 
            JOIN 
                handle h 
            ON 
                c.handle_id = h.ROWID
        WHERE
            chat_id = {chat_id}
        """,
        connection,
    )[
        "id"
    ]  # get all numbers in a chat

    return get_users_from_numbers(numbers)  # get users from the numbers


def get_users_from_numbers(numbers: Iterable[str]) -> list[User]:
    """
    Get users based on their numbers.
    - Input:
        - numbers (Iterable[str]): The numbers of the users.
    - Returns (list[User]): The list of users belonging to each number.
    """
    # connect to contacts
    contacts_connection = connect("/Users/samir/Library/Application Support/AddressBook/Sources/AABB697B-2862-4D43-AAAD-94EB8D1EAD03/AddressBook-v22.abcddb")
    all_contacts = read_sql_query(
        """
        SELECT 
            zfirstname, zlastname, zfullnumber
        FROM
            zabcdrecord r 
            JOIN 
                zabcdphonenumber p 
            ON 
                r.z_pk = p.zowner
        """,
        contacts_connection,
    )  # get all contacts

    found_users: list[User] = []

    for number in numbers:
        for i in range(len(all_contacts)):
            first, last, contact_number = cast(tuple[str, str, str], all_contacts.iloc[i, :])  # retrieve data from all contacts
            contact_number = "".join([n for n in contact_number if n != " "])  # remove spaces
            if contact_number[0] == "0":  # replace 0 at start with +61
                contact_number = "+61" + contact_number[1:]
            name = (first or "" + " " + last or "").strip()  # combine first and last names

            if number == contact_number:  # add a found user and break
                found_users.append(User(name, number))
                break

    return found_users


def get_messages(connection: Connection, chat_id: int) -> Generator[tuple[str, str], None, None]:
    """
    Get the messages from a particular chat.
    - Input:
        - connection (Connection): The database connection.
        - chat_id (int): The chat to find messages in.
    - Returns (Generator[tuple[str, str]]): Generator of (text, number) for each message.
    """
    messages = read_sql_query(
        f"""
        SELECT  
            text,
            id as phone
        FROM 
            (
                message m 
                JOIN 
                    chat_message_join c 
                ON 
                    m.ROWID = c.message_id
            ) 
            LEFT OUTER JOIN 
                handle h 
            ON 
                h.ROWID = m.handle_id
        WHERE
            chat_id = {chat_id}
        """,
        connection,
    )  # get all messages from the chat

    return (cast(tuple[str, str], messages.iloc[i, :]) for i in range(len(messages)))  # return generator of info access


def main():
    connection = get_db_connection()
    chat_id = get_chat_id(connection)
    print(get_chat_members(connection, chat_id))

    for text, phone in get_messages(connection, chat_id):
        print(text, phone)


if __name__ == "__main__":
    main()
