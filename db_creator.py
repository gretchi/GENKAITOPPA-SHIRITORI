#!/usr/bin/env python3

import logging
import re

import jaconv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func

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

    # laod_dictionaly(db, dl)

    initial = ""
    length = -1
    used = []
    last = ""

    message = ""

    pattern_hiragana = re.compile(r"^[ぁ-ん]$")
    pattern_digit = re.compile(r"^\d+$")
    pattern_invalid = re.compile(r"^.*ん$")

    while True:
        command = ""
        command = input(f"{message}:{last}> ")

        if len(command) == 0:
            if length == -1:
                continue

        elif len(command) != 0 and command[0] == ":":
            striped_command = command.strip(":")
            if len(striped_command):
                print(striped_command)
                last = striped_command
            else:
                last = ""

            continue

        elif len(command) < 2:
            message = f"Syntax error"
            continue

        else:
            initial = jaconv.kata2hira(command[0])
            length  = jaconv.z2h(command[1:], digit=True)

            if not pattern_hiragana.match(initial):
                message = "Syntax error"
                continue

            if not pattern_digit.match(length):
                message = "Syntax error"
                continue


            message = f"{initial}:{length}"


        for row in db.session.query(Dictionaly.kana, Dictionaly.length).filter(Dictionaly.kana.like(f"{initial}%")).filter_by(length=int(length)).group_by(Dictionaly.kana).order_by(func.random()):
            suggest = row[0]

            if suggest in used:
                continue
            
            if pattern_invalid.match(suggest):
                continue
            
            if last != "" and suggest[-1] != last:
                continue

            used.append(suggest)
            break

        print(f"{suggest}\n")

    db.close()




def laod_dictionaly(db, dl):
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
    
    return



if __name__ == "__main__":
    main()
