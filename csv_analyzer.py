#!/usr/bin/env python
from datetime import date, datetime
import csv
import re
import sys
import utils


csv.register_dialect("pipes", delimiter="|", escapechar="\\")


def process_csv(read_file):
    with open(read_file, "r", newline="") as fp:
        write_file = re.sub(r"(.*)\.csv", r"\1_output.csv", read_file)
        analyzer = utils.Analyzer(write_file)

        reader = csv.reader(fp, dialect="pipes")
        next(reader)

        for row in reader:
            (user_id, _, amount, _, trans_date, trans_type, _) = row

            user_id = int(user_id)
            amount = float(amount)
            trans_date = datetime.fromisoformat(trans_date).date()
            trans_type = utils.TransactionType.from_str(trans_type)

            trans = utils.Transaction(amount=amount, transaction_type=trans_type)

            analyzer.add_transaction(user_id, trans_date, trans)

        analyzer.write_output()


def main():
    for file_name in sys.argv[1:]:
        process_csv(file_name)


if __name__ == "__main__":
    main()
