#!/usr/bin/env python
import unittest
from utils import *
from datetime import date, timedelta


class TestUtils(unittest.TestCase):
    def test_file_name(self):
        analyzer = Analyzer("test_file.csv")
        self.assertEqual(analyzer.write_file, "test_file_output.csv")

    def test_add_transaction(self):
        analyzer = Analyzer("test_file.csv")
        user_id = 1
        trans_date = date(2019, 10, 30)

        transactions = [(100.00, TransactionType.CREDIT),
                (200.00, TransactionType.CREDIT),
                (50, TransactionType.DEBIT)]

        for trans in transactions:
            transaction = Transaction(*trans)
            analyzer.add_transaction(user_id, trans_date, transaction)

        analysis = analyzer.data[user_id]
        self.assertEqual(analysis.num_transactions, 3)
        self.assertEqual(analysis.sum_transactions, 250.00)
        self.assertEqual(analysis.balances, {trans_date: 250.00})

        new_trans_date = trans_date + timedelta(days=1)

        for trans in transactions:
            transaction = Transaction(*trans)
            analyzer.add_transaction(1, new_trans_date, transaction)

        self.assertEqual(analysis.num_transactions, 6)
        self.assertEqual(analysis.sum_transactions, 500.00)
        self.assertEqual(analysis.balances, {trans_date: 250.00, new_trans_date: 250.00})

    def test_get_report(self):
        analyzer = Analyzer("test_file.csv")
        user_id = 1
        trans_date = date(2019, 10, 30)

        transactions = [(100.00, TransactionType.CREDIT),
                (200.00, TransactionType.CREDIT),
                (50, TransactionType.DEBIT)]

        for trans in transactions:
            transaction = Transaction(*trans)
            analyzer.add_transaction(user_id, trans_date, transaction)

        new_trans_date = trans_date + timedelta(days=1)

        for trans in transactions:
            transaction = Transaction(*trans)
            analyzer.add_transaction(1, new_trans_date, transaction)

        analysis = analyzer.data[user_id]
        report = Analyzer.get_report(analysis)

        self.assertEqual(report, UserReport(num_transactions=6, sum_transactions=500, min_balance=0, max_balance=500))


if __name__ == "__main__":
    unittest.main()
