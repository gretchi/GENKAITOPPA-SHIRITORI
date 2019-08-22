#!/usr/bin/env python3

import logging

import jaconv
from sqlalchemy.exc import IntegrityError

from db import Database, Dictionaly
from dict_loader import DictLoader

logging.basicConfig(level=logging.INFO)

FROM_ROW            = 399328
TO_ROW              = 3103020
DICT_PATH           = "../../src/mecab-ipadic-neologd/seed/mecab-user-dict-seed.20190808.csv"
DB_PATH             = "./dict.sqlite3"
TRANSACTION_LIMIT   = 8192


def main():
    db = Database(DB_PATH)
    dl = DictLoader(DICT_PATH)

    for i, row in enumerate(dl.load(FROM_ROW, TO_ROW)):
        text = jaconv.kata2hira(row[11])
        db.session.add(Dictionaly(kana=text, length=len(text)))

        if not i % TRANSACTION_LIMIT:
            try:
                db.session.commit()
            except IntegrityError as e:
                logging.warning(str(e))

            logging.info(f"commited: {i}")


    db.session.commit()
    db.close()



if __name__ == "__main__":
    main()
