from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from enum import Enum

import csv
import re


class TransactionType(Enum):
    CREDIT = 1
    DEBIT = 2

    @classmethod
    def from_str(cls, trans_type: str):
        if trans_type == "credit":
            return cls.CREDIT
        elif trans_type == "debit":
            return cls.DEBIT
        else:
            raise IllegalArgumentException(
                "Transaction type not of proper format")


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

    def __init__(self, write_file: str):
        self.data = defaultdict(UserAnalysis)
        self.write_file = write_file

    def add_transaction(
            self,
            user_id: int,
            transaction_date: date,
            trans: Transaction):
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
                writer.writerow(
                    (user_id,
                     report.num_transactions,
                     "{0:.2f}".format(round(report.sum_transactions, 2)),
                     "{0:.2f}".format(round(report.min_balance, 2)),
                     "{0:.2f}".format(round(report.max_balance, 2))))
