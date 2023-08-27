from threading import Thread
from time import time


BLOCKLIST = {}


def _check_expired_tokens_in_blocklist():
    global BLOCKLIST
    jti_to_delete = set()
    for jti, exp in BLOCKLIST.items():
        if exp < time():
            jti_to_delete.add(jti)
    for jti in jti_to_delete:
        BLOCKLIST.pop(jti)


def add_to_blocklist(jti: str, exp: int) -> None:
    global BLOCKLIST
    BLOCKLIST[jti] = exp
    clearing_tokens_thread = Thread(target=_check_expired_tokens_in_blocklist,
                                    name="clearing_tokens")
    clearing_tokens_thread.start()
