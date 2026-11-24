
import unittest
import tempfile
import os

from processor import categorize, process_csv, monthly_summary


class TestExpenseProcessor(unittest.TestCase):

    def test_food_category(self):
        self.assertEqual(categorize("Swiggy Order"), "Food")

    def test_travel_category(self):
        self.assertEqual(categorize("Uber Ride"), "Travel")

    def test_unknown_category(self):
        self.assertEqual(categorize("Unknown Payment"), "Other")

    def test_csv_processing(self):
        csv_data = (
            "Date,Description,Amount\n"
            "2026-11-01,Swiggy,450\n"
            "2026-11-02,Uber,180\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".csv",
            delete=False,
            encoding="utf-8"
        ) as file:
            file.write(csv_data)
            filepath = file.name

        try:
            transactions, totals = process_csv(filepath)

            self.assertEqual(len(transactions), 2)
            self.assertEqual(totals["Food"], 450)
            self.assertEqual(totals["Travel"], 180)

        finally:
            os.remove(filepath)

    def test_monthly_summary(self):
        transactions = [
            {
                "date": "2026-11-01",
                "description": "Swiggy",
                "amount": 450,
                "category": "Food",
                "type": "Expense"
            },
            {
                "date": "2026-11-02",
                "description": "Uber",
                "amount": 180,
                "category": "Travel",
                "type": "Expense"
            }
        ]

        totals, highest_month = monthly_summary(transactions)

        self.assertEqual(totals["November 2026"], 630)
        self.assertEqual(highest_month, "November 2026")


if __name__ == "__main__":
    unittest.main()
