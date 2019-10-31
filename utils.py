from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Dict
from enum import Enum

import re


class TransactionType(Enum):
    CREDIT = 1
    DEBIT = 2


@dataclass(frozen=True)
class Transaction:
    amount: float
    transaction_type: TransactionType


class UserAnalysis:
    def __init__(self):
        self.num_transactions = 0
        self.sum_transactions = 0
        self.balances = defaultdict(float)


@dataclass(frozen=True)
class UserReport:
    num_transactions: int
    sum_transactions: int
    min_balance: float
    max_balance: float


class Analyzer:
    start_row = ("user_id", "n", "sum", "min", "max")

    def __init__(self, read_file):
        self.data = defaultdict(UserAnalysis)
        self.write_file = re.sub(r"(.*)\.csv", r"\1_output.csv", read_file)

    def add_transaction(self, user_id: int, transaction_date: date, trans: Transaction):
        analysis = self.data[user_id]
        analysis.num_transactions += 1

        if trans.transaction_type == TransactionType.CREDIT:
            analysis.sum_transactions += trans.amount
            analysis.balances[transaction_date] += trans.amount
        else:
            analysis.sum_transactions -= trans.amount
            analysis.balances[transaction_date] -= trans.amount

    @staticmethod
    def get_report(analysis: UserAnalysis) -> UserReport:
        running_balance = 0.0
        min_balance = 0.0
        max_balance = 0.0

        for transaction_date in sorted(analysis.balances.keys()):
            running_balance += analysis.balances[transaction_date]

            min_balance = min(min_balance, running_balance)
            max_balance = max(max_balance, running_balance)

        return UserReport(
            analysis.num_transactions,
            analysis.sum_transactions,
            min_balance,
            max_balance)

    def write_output(self):
        with open(self.write_file, "w", newline="") as fp:
            writer = csv.writer(fp, delimiter=",")
            writer.writerow(Analyzer.start_row)

            for (user_id, analysis) in self.data.items():
                report = Analyzer.get_report(analysis)
                writer.writerow((user_id,) + report.astuple())
