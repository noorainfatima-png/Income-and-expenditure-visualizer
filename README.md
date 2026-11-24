<div align="center">

# Expense Visualizer

**A Python desktop application for parsing bank CSV statements, classifying transactions, and analyzing personal cash flow through interactive visual breakdowns.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter%20%2F%20ttk-111827?style=for-the-badge)
![Data](https://img.shields.io/badge/Formats-CSV%20%7C%20JSON%20%7C%20TXT-10B981?style=for-the-badge)
![Testing](https://img.shields.io/badge/Tests-unittest-6366F1?style=for-the-badge)
![ML](https://img.shields.io/badge/Model-Rule--Based%20(No%20ML)-64748B?style=for-the-badge)

[Overview](#overview) • [Features](#interactive-features) • [Architecture & Tech Stack](#architecture--tech-stack)  • [Controls Guide](#controls--interface-guide)

</div>

---

## Overview

**Expense Visualizer** transforms raw bank statement CSV files into an organized financial dashboard. Built entirely with Python's standard library, it cleans and validates transaction records, separates income from expenditure, and classifies expenses using a deterministic rule-based keyword engine—requiring zero external dependencies or machine learning overhead.

---

## Interactive Features

- **CSV File Upload & Validation:** Parses raw bank statements, cleans malformed entries, and aggregates totals automatically.
- **Rule-Based Transaction Classification:** Separates inflows (`Income`) from outflows (`Expense`) and assigns spending categories via keyword matching.
- **Real-Time Summary Cards:** Displays live metrics for **Total Expenses**, **Total Income**, and **Transaction Count** upon import.
- **Interactive Pie Chart & Legend:** Custom Tkinter `Canvas` visualization where clicking any pie slice or legend item automatically switches to the Expenses view and filters the ledger by that category.
- **Dual-Tab Ledger (`Expenses` & `Income`):** Dedicated `ttk.Treeview` tables displaying **Date**, **Narration**, **Category**, and **Amount** with vertical scrolling.
- **Instant Search & Category Filtering:** Live keyword search across dates, descriptions, and categories paired with a dropdown category selector.
- **Exportable Summary Reports:** Generates and saves a formatted `.txt` financial summary containing overall totals, category-wise expense breakdowns, and itemized income records.

---

## Architecture & Tech Stack

| Layer | Components |
| :--- | :--- |
| **Languages & Formats** | Python, CSV, JSON |
| **GUI Framework** | Tkinter, Tkinter `ttk`, Tkinter `Canvas` |
| **Standard Library Modules** | `csv`, `json`, `collections`, `unittest` |
| **Classification Approach** | Rule-Based Classification Model, Keyword-Based Categorization (No Machine Learning) |

<details>
<summary><strong>Click to expand: Core Engineering Techniques</strong></summary>
<br>

- **Data Pipeline:** File Handling, CSV Data Processing, Data Cleaning, Data Validation
- **Analytics & Logic:** Income and Expense Classification, Rule-Based Expense Categorization, Keyword Matching, Data Aggregation, Category-Wise Summarization, Monthly Expense Analysis
- **Interface & Interaction:** Event-Driven Programming, GUI Development, Pie Chart Rendering, Real-Time Search and Filtering
- **Output & Verification:** Structured Report Generation, Data Export, Unit Testing (`unittest`)

</details>

---

## Controls & Interface Guide

| Control / Element | Location | Function |
| :--- | :--- | :--- |
| **Upload CSV** | Top Header | Opens a file dialog to select and process a bank `.csv` statement. |
| **Export Report** | Top Header | Exports aggregated totals, category summaries, and income entries to a `.txt` file. |
| **Summary Cards** | Upper Dashboard | Displays Total Expenses, Total Income, and Total Transactions. |
| **Interactive Pie Chart** | Left Panel | Renders proportional category spending; click any slice or legend label to filter expenses. |
| **Expense / Income Tabs** | Right Panel | Switches between categorized expenditure records and income transactions. |
| **Category Filter** | Expense Tab | Filters the expense table by a specific spending category or resets to `All`. |
| **Search Bar** | Expense & Income Tabs | Filters visible rows dynamically as you type across date, narration, and category fields. |

---



### Prerequisites

- Python **3.8** or higher (includes `tkinter`, `csv`, `json`, `collections`, and `unittest` out of the box—no `pip install` required).

