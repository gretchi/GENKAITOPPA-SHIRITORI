
import csv

class DictLoader(object):
    def __init__(self, path):
        self.path = path

    def load(self, from_row, to_row, charset="utf-8"):
        with open(self.path, encoding=charset) as fh:
            reader = csv.reader(fh)

            for line_num, row in enumerate(reader):
                if line_num < from_row:
                    continue
                elif line_num > to_row:
                    break

                yield row

        return
