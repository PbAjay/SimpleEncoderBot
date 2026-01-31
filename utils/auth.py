from config import OWNER_ID

def is_authorized(uid: int) -> bool:
    return uid == OWNER_ID
