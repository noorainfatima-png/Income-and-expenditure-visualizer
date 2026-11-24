import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from processor import process_csv

CHART_COLORS = [
    "#6366F1", "#10B981", "#F59E0B", "#EF4444",
    "#8B5CF6", "#06B6D4", "#64748B", "#EC4899",
    "#14B8A6", "#F97316"
]


class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Visualizer")
        self.root.geometry("1180x740")
        self.root.minsize(950, 620)
        self.root.configure(bg="#F3F4F6")

        self.transactions = []
        self.category_totals = {}
        self.expense_search = tk.StringVar()
        self.income_search = tk.StringVar()

        self.build_header()
        self.build_summary_cards()
        self.build_main_area()
        self.build_footer()

    def build_header(self):
        header = tk.Frame(self.root, bg="#111827")
        header.pack(fill="x")

        tk.Label(
            header, text="EXPENSE VISUALIZER",
            bg="#111827", fg="white",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=22, pady=18)

        tk.Button(
            header, text="Export Report", command=self.export_report,
            bg="#10B981", fg="white", activebackground="#059669",
            relief="flat", font=("Arial", 10, "bold"),
            padx=16, pady=8
        ).pack(side="right", padx=(0, 20), pady=14)

        tk.Button(
            header, text="Upload CSV", command=self.upload_csv,
            bg="#6366F1", fg="white", activebackground="#4F46E5",
            relief="flat", font=("Arial", 10, "bold"),
            padx=18, pady=8
        ).pack(side="right", padx=(0, 10), pady=14)

    def build_summary_cards(self):
        area = tk.Frame(self.root, bg="#F3F4F6")
        area.pack(fill="x", padx=20, pady=14)

        self.expense_value = self.summary_card(
            area, "TOTAL EXPENSES", "₹0.00", "#EEF2FF", "#4338CA"
        )
        self.income_value = self.summary_card(
            area, "TOTAL INCOME", "₹0.00", "#ECFDF5", "#047857"
        )
        self.count_value = self.summary_card(
            area, "TRANSACTIONS", "0", "#FFFFFF", "#374151"
        )

    def summary_card(self, parent, title, value, background, foreground):
        card = tk.Frame(parent, bg=background, padx=18, pady=12)
        card.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(
            card, text=title, bg=background, fg=foreground,
            font=("Arial", 9, "bold")
        ).pack(anchor="w")
        label = tk.Label(
            card, text=value, bg=background, fg=foreground,
            font=("Arial", 17, "bold")
        )
        label.pack(anchor="w", pady=(5, 0))
        return label

    def build_main_area(self):
        main = tk.Frame(self.root, bg="#F3F4F6")
        main.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        chart_panel = tk.Frame(main, bg="white", width=330)
        chart_panel.pack(side="left", fill="y", padx=(0, 14))
        chart_panel.pack_propagate(False)

        tk.Label(
            chart_panel, text="Expense Breakdown",
            bg="white", fg="#111827",
            font=("Arial", 13, "bold")
        ).pack(pady=(15, 4))
        tk.Label(
            chart_panel, text="Click a slice/category to filter",
            bg="white", fg="#6B7280", font=("Arial", 8)
        ).pack()

        self.chart = tk.Canvas(
            chart_panel, width=310, height=430,
            bg="white", highlightthickness=0
        )
        self.chart.pack(fill="both", expand=True, padx=8, pady=6)

        data_panel = tk.Frame(main, bg="white")
        data_panel.pack(side="right", fill="both", expand=True)

        self.notebook = ttk.Notebook(data_panel)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        expenses_tab = tk.Frame(self.notebook, bg="white")
        income_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(expenses_tab, text="  Expenses  ")
        self.notebook.add(income_tab, text="  Income  ")

        self.build_expenses_tab(expenses_tab)
        self.build_income_tab(income_tab)

    def build_expenses_tab(self, parent):
        controls = tk.Frame(parent, bg="white")
        controls.pack(fill="x", padx=10, pady=10)

        tk.Label(controls, text="Category:", bg="white").pack(side="left")
        self.category_filter = ttk.Combobox(
            controls, values=["All"], state="readonly", width=15
        )
        self.category_filter.set("All")
        self.category_filter.pack(side="left", padx=(6, 12))
        self.category_filter.bind(
            "<<ComboboxSelected>>", self.filter_expenses
        )

        tk.Label(controls, text="Search:", bg="white").pack(side="left")
        ttk.Entry(
            controls, textvariable=self.expense_search, width=24
        ).pack(side="left", padx=6)
        self.expense_search.trace_add(
            "write", lambda *_: self.filter_expenses()
        )

        self.expense_tree = self.make_transaction_table(parent)

    def build_income_tab(self, parent):
        controls = tk.Frame(parent, bg="white")
        controls.pack(fill="x", padx=10, pady=10)

        tk.Label(controls, text="Search income:", bg="white").pack(side="left")
        ttk.Entry(
            controls, textvariable=self.income_search, width=32
        ).pack(side="left", padx=8)
        self.income_search.trace_add(
            "write", lambda *_: self.filter_income()
        )

        self.income_tree = self.make_transaction_table(parent)

    def make_transaction_table(self, parent):
        table_area = tk.Frame(parent, bg="white")
        table_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("Date", "Narration", "Category", "Amount")
        tree = ttk.Treeview(
            table_area, columns=columns, show="headings", height=17
        )
        for column in columns:
            tree.heading(column, text=column)

        tree.column("Date", width=100, anchor="center")
        tree.column("Narration", width=245)
        tree.column("Category", width=115, anchor="center")
        tree.column("Amount", width=115, anchor="e")

        scrollbar = ttk.Scrollbar(
            table_area, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def build_footer(self):
        footer = tk.Frame(self.root, bg="#F3F4F6")
        footer.pack(side="bottom", fill="x", padx=20, pady=(0, 14))

        self.status_label = tk.Label(
            footer, text="Upload a bank CSV to get started.",
            bg="#F3F4F6", fg="#6B7280", font=("Arial", 9)
        )
        self.status_label.pack(side="left")

    def upload_csv(self):
        path = filedialog.askopenfilename(
            title="Choose bank statement",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        try:
            transactions, category_totals = process_csv(path)
            self.transactions = transactions
            self.category_totals = category_totals
            self.refresh_dashboard()
            messagebox.showinfo(
                "Import complete",
                f"Imported {len(transactions)} transactions."
            )
        except Exception as exc:
            messagebox.showerror("CSV import failed", str(exc))

    def refresh_dashboard(self):
        expenses = [
            item for item in self.transactions
            if item.get("type", "Expense") == "Expense"
        ]
        income = [
            item for item in self.transactions
            if item.get("type") == "Income"
        ]
        expense_total = sum(float(item["amount"]) for item in expenses)
        income_total = sum(float(item["amount"]) for item in income)

        self.expense_value.config(text=f"₹{expense_total:,.2f}")
        self.income_value.config(text=f"₹{income_total:,.2f}")
        self.count_value.config(text=str(len(self.transactions)))

        categories = sorted({item.get("category", "Other") for item in expenses})
        self.category_filter["values"] = ["All"] + categories
        self.category_filter.set("All")

        self.filter_expenses()
        self.filter_income()
        self.draw_expense_chart()

    def add_row(self, tree, transaction):
        tree.insert(
            "", "end",
            values=(
                transaction.get("date", ""),
                transaction.get("description", ""),
                transaction.get("category", ""),
                f"₹{float(transaction.get('amount', 0)):,.2f}"
            )
        )

    def filter_expenses(self, event=None):
        if not hasattr(self, "expense_tree"):
            return
        category = self.category_filter.get() or "All"
        query = self.expense_search.get().strip().lower()
        self.expense_tree.delete(*self.expense_tree.get_children())

        for transaction in self.transactions:
            if transaction.get("type", "Expense") != "Expense":
                continue
            current_category = transaction.get("category", "Other")
            searchable = (
                f"{transaction.get('date', '')} "
                f"{transaction.get('description', '')} {current_category}"
            ).lower()

            if category != "All" and current_category != category:
                continue
            if query and query not in searchable:
                continue
            self.add_row(self.expense_tree, transaction)

    def filter_income(self):
        if not hasattr(self, "income_tree"):
            return
        query = self.income_search.get().strip().lower()
        self.income_tree.delete(*self.income_tree.get_children())

        for transaction in self.transactions:
            if transaction.get("type") != "Income":
                continue
            searchable = (
                f"{transaction.get('date', '')} "
                f"{transaction.get('description', '')} "
                f"{transaction.get('category', '')}"
            ).lower()
            if query and query not in searchable:
                continue
            self.add_row(self.income_tree, transaction)

    def draw_expense_chart(self):
        self.chart.delete("all")
        expense_totals = {}
        for transaction in self.transactions:
            if transaction.get("type", "Expense") != "Expense":
                continue
            category = transaction.get("category", "Other")
            expense_totals[category] = expense_totals.get(category, 0) + float(
                transaction["amount"]
            )

        total = sum(expense_totals.values())
        if total <= 0:
            self.chart.create_text(
                155, 180, text="Upload a CSV statement",
                fill="#6B7280", font=("Arial", 11)
            )
            return

        sorted_items = sorted(
            expense_totals.items(), key=lambda pair: pair[1], reverse=True
        )
        angle = 0
        for index, (category, amount) in enumerate(sorted_items):
            extent = amount / total * 360
            color = CHART_COLORS[index % len(CHART_COLORS)]
            arc_id = self.chart.create_arc(
                42, 25, 268, 251,
                start=angle, extent=extent,
                style=tk.PIESLICE, fill=color,
                outline="white", width=2
            )
            self.chart.tag_bind(
                arc_id, "<Button-1>",
                lambda event, name=category, value=amount:
                    self.chart_category_clicked(name, value)
            )
            angle += extent

            y = 275 + index * 22
            if y > 410:
                break
            legend_tag = f"legend_{index}"
            self.chart.create_rectangle(
                18, y, 32, y + 14, fill=color, outline="",
                tags=(legend_tag,)
            )
            self.chart.create_text(
                40, y + 7, anchor="w",
                text=f"{category}: ₹{amount:,.0f}",
                fill="#374151", font=("Arial", 9),
                tags=(legend_tag,)
            )
            self.chart.tag_bind(
                legend_tag, "<Button-1>",
                lambda event, name=category, value=amount:
                    self.chart_category_clicked(name, value)
            )

        self.status_label.config(text=f"Expenses shown: ₹{total:,.2f}")

    def chart_category_clicked(self, category, amount):
        self.notebook.select(0)
        self.category_filter.set(category)
        self.filter_expenses()
        self.status_label.config(
            text=f"{category} expenses: ₹{amount:,.2f} — filtered"
        )

    def export_report(self):
        if not self.transactions:
            messagebox.showwarning("No transactions", "Upload a CSV first.")
            return

        path = filedialog.asksaveasfilename(
            title="Save report", defaultextension=".txt",
            filetypes=[("Text report", "*.txt")]
        )
        if not path:
            return

        expenses = [
            item for item in self.transactions
            if item.get("type", "Expense") == "Expense"
        ]
        incomes = [
            item for item in self.transactions
            if item.get("type") == "Income"
        ]
        expense_total = sum(float(item["amount"]) for item in expenses)
        income_total = sum(float(item["amount"]) for item in incomes)

        with open(path, "w", encoding="utf-8") as report:
            report.write("EXPENSE VISUALIZER REPORT\n")
            report.write("=" * 28 + "\n\n")
            report.write(f"Total expenses: ₹{expense_total:,.2f}\n")
            report.write(f"Total income: ₹{income_total:,.2f}\n")
            report.write(f"Transaction count: {len(self.transactions)}\n\n")
            report.write("EXPENSE CATEGORY TOTALS\n")
            report.write("-" * 23 + "\n")
            for category, amount in sorted(
                self.category_totals.items(), key=lambda pair: pair[1], reverse=True
            ):
                report.write(f"{category}: ₹{amount:,.2f}\n")
            report.write("\nINCOME TRANSACTIONS\n")
            report.write("-" * 19 + "\n")
            for item in incomes:
                report.write(
                    f"{item.get('date', '')} | {item.get('description', '')} | "
                    f"₹{float(item['amount']):,.2f}\n"
                )

        messagebox.showinfo("Export successful", "Report saved successfully.")


if __name__ == "__main__":
    window = tk.Tk()
    app = ExpenseApp(window)
    window.mainloop()