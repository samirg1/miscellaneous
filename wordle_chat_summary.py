# Uses iMessages in a Wordle group chat to give a summary, standings and more.
# Date: 16-11-2022
# Author: Samir Gupta

from math import inf, log10
from os import listdir
from sqlite3 import Connection, OperationalError, connect
from typing import Callable, Iterable, Iterator, Sequence, TypeVar, cast

from pandas import DataFrame, Series, read_sql_query

T = TypeVar("T")


class Member:
    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number
        self._games: dict[int, int] = {}
        self._current_guess_sum = 0

        self.completed = 0
        self.fails = 0
        self.average_guesses = 0

    def __repr__(self) -> str:
        return f"({self.name}, {self.number}, {self._games})"

    def add_wordle(self, no: int, guesses: int):
        self._games[no] = guesses
        self._current_guess_sum += guesses
        self.completed = len(self._games)
        self.average_guesses = self._current_guess_sum / self.completed

    @property
    def attempted(self) -> int:
        return self.completed + self.fails


def find(sequence: Sequence[T], /, *, key: Callable[[T], bool]) -> T | None:
    """
    Find the first element in a sequence that satisfies a condition.
    - Input:
        - sequence (Sequence[T]): The sequence to look in.
        - callable (Callable[[T], bool]): Callable to test for the condition.
    - Returns (T | None): The element or None if no element was found.
    - Time Complexity: O(S), where S is the length of the sequence.
    - Aux space complexity: O(1).
    """
    for element in sequence:
        if key(element):
            return element


def get_db_connection() -> tuple[Connection, str]:
    """
    Get the database connection for the right user.
    - Returns (tuple[Connection, str]): The database connection and the user name responsible.
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

    return connection, potential_users[index]


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


def get_chat_members(connection: Connection, chat_id: int, user: str) -> list[Member]:
    """
    Get the members of a particular chat.
    - Input:
        - connection (Connection): The database connnection.
        - chat_id (int): The chat id of the chat to find members of.
        - user (str): The name of the user.
    - Returns (list[Member]): The list of members.
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

    return get_members_from_numbers(numbers, user)  # get members from the numbers


def get_addressbook_db_path(user: str) -> str:
    """
    Get the address-book database path.
    - Input:
        - user (str): The user.
    - Returns (str): The path to the database file.
    - Raises (ValueError): If no file is found.
    """
    address_source_path = f"/Users/{user}/Library/Application Support/AddressBook/Sources"  # base path
    for dir in listdir(address_source_path):
        if not dir.count("."):  # go one step in each folder
            for file in listdir(f"{address_source_path}/{dir}"):
                if file.count("."):  # find the correct file
                    if file == "AddressBook-v22.abcddb":
                        return f"{address_source_path}/{dir}/{file}"
    raise ValueError


def get_members_from_numbers(numbers: Iterable[str], user: str) -> list[Member]:
    """
    Get users based on their numbers.
    - Input:
        - numbers (Iterable[str]): The phone numbers of the members.
        - user (str): The name of the user.
    - Returns (list[Member]): The list of members belonging to each number.
    """
    # connect to contacts
    address_path: str
    all_contacts = DataFrame()
    try:
        address_path = get_addressbook_db_path(user)
        contacts_connection = connect(address_path)

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
    except (ValueError, OperationalError):  # contact info was not able to be found
        print("unable to find contacts")
        return [Member(number, number) for number in numbers] + [Member("self", "")]

    found_users: list[Member] = []

    for number in numbers:
        for i in range(len(all_contacts)):
            first, last, contact_number = cast(tuple[str, str, str], all_contacts.iloc[i, :])  # retrieve data from all contacts
            contact_number = "".join([n for n in contact_number if n != " "])  # remove spaces
            if contact_number[0] == "0":  # replace 0 at start with +61
                contact_number = "+61" + contact_number[1:]
            name = first or "" + " " + last or ""  # combine first and last names
            name = ("".join(n for n in name if n.isalnum() or n == " ")).strip()  # clean up

            if number == contact_number:  # add a found user and break
                found_users.append(Member(name, number))
                break
        else:  # if we did not find a contact, set the contact name to just the number
            found_users.append(Member(number, number))

    print("\nENTER USER NAME")
    self_name = input("enter user's display name: ")
    found_users.append(Member(self_name, ""))
    return found_users


def get_messages(connection: Connection, chat_id: int) -> Iterator[tuple[str, str]]:
    """
    Get the messages from a particular chat.
    - Input:
        - connection (Connection): The database connection.
        - chat_id (int): The chat to find messages in.
    - Returns (Iterator[tuple[str, str]]): Iterator of (text, number) for each message.
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

    return (cast(tuple[str, str], messages.iloc[i, :]) for i in range(len(messages)))  # return iterator of info access


def anaylse_messages(members: list[Member], messages: Iterator[tuple[str, str]]) -> int | float:
    """
    Analyse messages to add wordle games to chat members.
    - Input:
        - members (list[User]): The chat members.
        - messages (Iterator[tuple[str, str]]): The messages in form (text, number).
    - Returns (int): The amount of days the messages were from or 0 if no messages were found.
    """
    max_wordle_number: int = 0
    min_wordle_number: int | float = inf
    for text, phone in messages:
        fail_detected = False
        match text.split(" "):  # match texts to 'Wordle <num> <guesses>/6
            case ["Wordle", number, score, *_]:
                try:
                    wordle_number = int(number)
                    max_wordle_number = max(max_wordle_number, wordle_number)
                    min_wordle_number = min(min_wordle_number, wordle_number)
                except ValueError:
                    continue

                try:
                    guesses = int(score[0])
                except ValueError:
                    if score[0] == "X":  # if user fails it will be X/6
                        fail_detected = True
                        guesses = 0
                    else:
                        continue
            case _:  # continue if text doesnt match
                continue

        member = find(members, key=lambda member: member.number == phone) if phone is not None else members[-1]  # find the member, if phone is None member is user
        if member is not None:
            if fail_detected:
                member.fails += 1
            else:
                member.add_wordle(wordle_number, guesses)  # add wordle

    return max(max_wordle_number - min_wordle_number + 1, 0)  # return total amount of days or 0 if no messages


def print_summary(members: list[Member], messages: Iterator[tuple[str, str]]):
    """
    Print the summary of the Wordle group chat.
    - Input:
        - members (list[Member]): The members in the chat.
        - messages (Iterator[tuple[str, str]]): The messages in the chat.
    """
    total_days = anaylse_messages(members, messages)  # analyse messages
    if total_days == 0:
        return print("\nno wordle messages found")

    max_name_length = len(max(members, key=lambda user: len(user.name)).name)  # get the length of the longest name
    max_completed = max(members, key=lambda user: user.completed).completed  # get the maximum amount of completions
    completed_width = int(log10(max_completed)) + 1  # get width for completion

    members.sort(key=lambda user: user.completed, reverse=True)  # sort by completions

    print(f"\nCOMPLETIONS ({total_days} days)")  # print completion summary
    for i, member in enumerate(members, start=1):
        print(f"{i}. {member.name:.<{max_name_length}}..{member.completed:.>{completed_width}d}/{member.attempted}")

    members.sort(key=lambda user: user.average_guesses)  # sort by average guesses
    print("\nAVERAGE GUESSES")  # print average guess summary
    for i, member in enumerate(members, start=1):
        print(f"{i}. {member.name:.<{max_name_length}}..{member.average_guesses:.2f}")


def main():
    connection, user = get_db_connection()  # get main db connection
    chat_id = get_chat_id(connection)  # get chat id of wordle chat
    members = get_chat_members(connection, chat_id, user)  # get members of the chat
    messages = get_messages(connection, chat_id)  # get the messages of the chat
    print_summary(members, messages)  # print the summary of the chat

    # m = read_sql_query(
    #     """
    #     SELECT text from message m JOIN chat_message_join c on m.ROWID = c.message_id WHERE chat_id = 2
    #     """,
    #     connection,
    # )
    # print(len(m))


if __name__ == "__main__":
    main()
