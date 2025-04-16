import os
from supabase import create_client
from supabase.client import ClientOptions
from hashlib import sha256
import classes

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
    options=ClientOptions(schema="dev"),
)


def create_error_msg(msg: str) -> dict:
    """Creates an error message.

    Args:
        msg (str): The message.

    Returns:
        dict: The error message.
    """
    return {"message": msg}


def hash_string(str: str) -> str:
    """Hashes a string.

    Args:
        str (str): The string to hash.

    Returns:
        str: The hashed string.
    """
    return sha256(str.encode("utf-8")).hexdigest()


def get_auth(key: str) -> classes.Auth | None:
    """Gets the auth of a key.

    Args:
        key (str): The key, unhashed, to check.

    Returns:
        classes.Auth | None: Returns an Auth object if successful, returns None if not.
    """
    key_hash = hash_string(key)

    query = supabase.table("auth").select().eq("key_hash", key_hash).execute()

    if len(query.data) >= 1:
        return classes.Auth.from_dict(query.data[0])
    else:
        return None
