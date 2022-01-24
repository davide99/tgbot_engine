import psycopg2
import consts


class DB:
    def __init__(self) -> None:
        self.__con = psycopg2.connect(consts.DB_DSN)

    def setChatStatus(self, chat_id: int, status: bool) -> None:
        cur = self.__con.cursor()
        cur.execute('UPDATE users SET enabled={} WHERE id={}'.format('TRUE' if status else 'FALSE', chat_id))
        self.__con.commit()

    def getChatStatus(self, chat_id: int) -> bool:
        cur = self.__con.cursor()
        cur.execute('SELECT enabled FROM users WHERE id={}'.format(chat_id))
        row = cur.fetchone()

        return row[0]

    def setRate(self, chat_id: int, rate: float) -> None:
        cur = self.__con.cursor()
        cur.execute('UPDATE users SET rate={} WHERE id={}'.format(rate, chat_id))
        self.__con.commit()

    def getRate(self, chat_id: int) -> float:
        cur = self.__con.cursor()
        cur.execute('SELECT rate FROM users WHERE id={}'.format(chat_id))
        row = cur.fetchone()

        return row[0]
