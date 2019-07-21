from enum import Enum

token = "989390225:AAGSd5U8U4fusOyqZWw2lFukhN7YoGDpqqA"
db_file = "database.vdb"


class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_SEND_PIC = "3"
