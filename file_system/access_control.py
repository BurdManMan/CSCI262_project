"""Bell-LaPadula rules"""


def can_read(user_clearance: int, file_clearance: int) -> bool:
    return user_clearance >= file_clearance  # no read up


def can_write(user_clearance: int, file_clearance: int) -> bool:
    return user_clearance <= file_clearance  # no write down
