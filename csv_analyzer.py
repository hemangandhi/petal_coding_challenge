#!/usr/bin/env python
from datetime import date, datetime
from typing import List
import multiprocessing as mp

import argparse
import csv
import re
import sys
import utils


def process_csv(read_file):
    if not re.match(r"(.*)\.csv$", read_file):
        raise ValueError("All files must be given the .csv extension")

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


def main(files: List[str], processes: int):
    csv.register_dialect("pipes", delimiter="|", escapechar="\\")
    processes = min(processes, len(files), mp.cpu_count())
    
    if processes > 1:
        pool = mp.Pool(processes)
        pool.map(process_csv, files)
    else:
        for read_file in files:
            process_csv(read_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", nargs="+", help="CSV files to be processed")
    parser.add_argument("-p", "--processes", help="Max number of processes to be spawned", type=int, default=1)

    args = parser.parse_args()
    main(args.files, args.processes)
