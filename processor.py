
import csv
import json
from collections import defaultdict
from datetime import datetime


# ==========================================
# 1. DEFAULT EXPENSE CATEGORIES
# ==========================================

DEFAULT_RULES = {
    "Food": [
        "swiggy", "zomato", "cafe",
        "restaurant", "blinkit", "zepto",
        "dominos", "pizza"
    ],

    "Travel": [
        "uber", "ola", "rapido",
        "irctc", "metro", "petrol",
        "bus", "train"
    ],

    "Shopping": [
        "amazon", "flipkart",
        "myntra", "zudio"
    ],

    "Bills": [
        "airtel", "jio", "electricity",
        "broadband", "recharge"
    ],

    "Health": [
        "pharmacy", "hospital",
        "medicine", "medplus"
    ],

    "Education": [
        "college", "books",
        "course", "education"
    ]
}


# ==========================================
# 2. LOAD CATEGORY RULES
# ==========================================

def load_rules():
    try:
        with open(
            "rules.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_RULES


# ==========================================
# 3. SAVE CATEGORY RULES
# ==========================================

def save_rules(rules):
    with open(
        "rules.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            rules,
            file,
            indent=4
        )


# ==========================================
# 4. AUTOMATIC CATEGORIZATION
# ==========================================

def categorize(description, rules=None):

    if rules is None:
        rules = load_rules()

    description = description.lower()

    for category, keywords in rules.items():

        for keyword in keywords:

            if keyword.lower() in description:
                return category

    return "Other"


# ==========================================
# 5. CLEAN AMOUNT VALUES
# ==========================================

def clean_amount(value):

    if value is None:
        return 0.0

    value = str(value).strip()

    value = value.replace("₹", "")
    value = value.replace("INR", "")
    value = value.replace(",", "")
    value = value.replace(" ", "")

    if value == "":
        return 0.0

    try:
        return float(value)

    except ValueError:
        return None


# ==========================================
# 6. PROCESS BANK STATEMENT
# ==========================================

def process_csv(filepath):

    transactions = []

    category_totals = defaultdict(float)

    with open(
        filepath,
        "r",
        encoding="utf-8-sig"
    ) as file:

        sample = file.read(2048)
        file.seek(0)

        delimiter = "\t" if "\t" in sample.splitlines()[0] else ","
        reader = csv.DictReader(file, delimiter=delimiter)

        # Normalize column names
        headers = {
            str(header).strip().lower()
            for header in reader.fieldnames or []
        }

        # Identify Debit and Credit columns
        debit_column = None
        credit_column = None

        debit_options = [
            "debit",
            "withdrawal",
            "withdrawals",
            "dr",
            "debit amount"
        ]

        credit_options = [
            "credit",
            "deposit",
            "deposits",
            "cr",
            "credit amount"
        ]

        for column in debit_options:

            if column in headers:
                debit_column = column
                break

        for column in credit_options:

            if column in headers:
                credit_column = column
                break

        # Read every transaction
        for row in reader:

            # Normalize row keys
            row = {
                str(key).strip().lower(): value or ""
                for key, value in row.items()
                if key is not None
            }

            date = row.get("date", "").strip()

            description = row.get(
                "description",
                row.get("narration", "")
            ).strip()

            amount = 0.0
            transaction_type = ""

            # ----------------------------------
            # BANK STATEMENT WITH DEBIT/CREDIT
            # ----------------------------------

            if debit_column or credit_column:

                debit_amount = clean_amount(
                    row.get(debit_column, "")
                    if debit_column
                    else ""
                )

                credit_amount = clean_amount(
                    row.get(credit_column, "")
                    if credit_column
                    else ""
                )

                if debit_amount is None or credit_amount is None:
                    continue

                if debit_amount > 0:

                    amount = debit_amount
                    transaction_type = "Expense"

                elif credit_amount > 0:

                    amount = credit_amount
                    transaction_type = "Income"

                else:
                    continue

            # ----------------------------------
            # BANK STATEMENT WITH AMOUNT COLUMN
            # ----------------------------------

            else:

                raw_amount = clean_amount(
                    row.get("amount", "0")
                )

                if raw_amount is None:
                    continue

                if raw_amount < 0:

                    amount = abs(raw_amount)
                    transaction_type = "Income"

                elif raw_amount > 0:

                    amount = raw_amount
                    transaction_type = "Expense"

                else:
                    continue

            # ----------------------------------
            # CATEGORIZE TRANSACTION
            # ----------------------------------

            if transaction_type == "Income":

                category = "Income"

            else:

                category = categorize(description)

            # ----------------------------------
            # STORE TRANSACTION
            # ----------------------------------

            transaction = {
                "date": date,
                "description": description,
                "amount": amount,
                "category": category,
                "type": transaction_type
            }

            transactions.append(transaction)

            # Add only expenses to spending totals
            if transaction_type == "Expense":

                category_totals[category] += amount

    return transactions, dict(category_totals)


# ==========================================
# 7. MONTHLY SPENDING ANALYSIS
# ==========================================

def monthly_summary(transactions):

    monthly_totals = defaultdict(float)

    for transaction in transactions:

        # Ignore income
        if transaction["type"] != "Expense":
            continue

        date_text = transaction["date"].strip()

        date = None

        # Supported date formats
        date_formats = (
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%d-%b-%Y",
            "%d %b %Y"
        )

        # Try each date format
        for date_format in date_formats:

            try:

                date = datetime.strptime(
                    date_text,
                    date_format
                )

                break

            except ValueError:
                continue

        # Skip invalid dates
        if date is None:
            continue

        # Example: November 2026
        month = date.strftime("%B %Y")

        monthly_totals[month] += transaction["amount"]

    # No valid expense data
    if not monthly_totals:
        return {}, None

    # Find highest spending month
    highest_month = max(
        monthly_totals,
        key=monthly_totals.get
    )

    return dict(monthly_totals), highest_month
