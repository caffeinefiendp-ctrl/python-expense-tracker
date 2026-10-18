
import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime, timedelta
import csv
import os
import matplotlib.pyplot as plt

categories = ["Food & Drinks", "Shopping", "Bills & Maintenance", "Travel", "Healthcare"]

# ---------- Colors ----------
BG_COLOR = "#1e1e2f"
CARD_COLOR = "#2a2a3d"
ACCENT_COLOR = "#6c5ce7"
TEXT_COLOR = "#ffffff"
DANGER_COLOR = "#e74c3c"

# ---------- Functions ----------

def submit_expense():
    entered_date = date_entry.get()
    if entered_date == "":
        expense_date = str(date.today())
    else:
        expense_date = entered_date

    selected_category = category_var.get()
    product = product_entry.get()
    amount_text = amount_entry.get()

    if selected_category == "" or product == "" or amount_text == "":
        messagebox.showerror("Missing Info", "Please fill all fields!")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Amount must be a number!")
        return

    file_exists = os.path.exists("expenses.csv")
    file = open("expenses.csv", "a", newline="")
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["date", "category", "product", "amount"])
    writer.writerow([expense_date, selected_category, product, amount])
    file.close()

    messagebox.showinfo("Success", "Expense added successfully!")

    date_entry.delete(0, tk.END)
    product_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_var.set("")


def clear_all_data():
    confirm = messagebox.askyesno("Confirm", "This will delete ALL expense data permanently. Are you sure?")
    if confirm:
        if os.path.exists("expenses.csv"):
            os.remove("expenses.csv")
        messagebox.showinfo("Cleared", "All data has been cleared!")


def calculate_totals(filter_days=None, filter_month=False):
    result = {}
    for cat in categories:
        result[cat] = 0

    if not os.path.exists("expenses.csv"):
        return result

    file = open("expenses.csv", "r")
    reader = csv.reader(file)
    next(reader)

    today = date.today()

    for row in reader:
        row_date = datetime.strptime(row[0], "%Y-%m-%d").date()
        row_category = row[1]
        row_amount = float(row[3])

        if filter_days is not None:
            start_date = today - timedelta(days=filter_days)
            if row_date < start_date or row_date > today:
                continue
        elif filter_month:
            if row_date.month != today.month or row_date.year != today.year:
                continue

        result[row_category] = result[row_category] + row_amount

    file.close()
    return result


def show_graph(totals, title):
    plt.figure(facecolor=BG_COLOR)
    ax = plt.axes()
    ax.set_facecolor(BG_COLOR)
    bars = plt.bar(totals.keys(), totals.values(), color=ACCENT_COLOR)
    for i, (cat, amt) in enumerate(totals.items()):
        plt.text(i, amt, str(amt), ha='center', va='bottom', color=TEXT_COLOR)
    plt.xlabel("Category", color=TEXT_COLOR)
    plt.ylabel("Amount Spent", color=TEXT_COLOR)
    plt.title(title, color=TEXT_COLOR, fontsize=14, fontweight='bold')
    plt.xticks(rotation=20, color=TEXT_COLOR)
    plt.yticks(color=TEXT_COLOR)
    ax.spines['bottom'].set_color(TEXT_COLOR)
    ax.spines['left'].set_color(TEXT_COLOR)
    ax.spines['top'].set_color(BG_COLOR)
    ax.spines['right'].set_color(BG_COLOR)
    plt.tight_layout()
    plt.show()


def show_overall_graph():
    totals = calculate_totals()
    show_graph(totals, "Overall Spending")


def show_monthly_graph():
    totals = calculate_totals(filter_month=True)
    show_graph(totals, "This Month's Spending")


def show_weekly_graph():
    totals = calculate_totals(filter_days=7)
    show_graph(totals, "This Week's Spending")


def show_today_graph():
    totals = calculate_totals(filter_days=0)
    show_graph(totals, "Today's Spending")


def show_total_label():
    totals = calculate_totals()
    total = sum(totals.values())
    messagebox.showinfo("Total Spending", f"Total spending so far: {total}")


# ---------- GUI Layout ----------

window = tk.Tk()
window.title("My Expense Tracker")
window.geometry("420x680")
window.configure(bg=BG_COLOR)

title_label = tk.Label(window, text="💰 Expense Tracker", font=("Segoe UI", 22, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(pady=20)

form_frame = tk.Frame(window, bg=CARD_COLOR, padx=20, pady=20)
form_frame.pack(padx=20, pady=10, fill="x")

tk.Label(form_frame, text="Date (YYYY-MM-DD) or leave blank:", bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w")
date_entry = tk.Entry(form_frame)
date_entry.pack(pady=(0, 10), fill="x")

tk.Label(form_frame, text="Category:", bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w")
category_var = tk.StringVar()
category_menu = tk.OptionMenu(form_frame, category_var, *categories)
category_menu.pack(pady=(0, 10), fill="x")

tk.Label(form_frame, text="Product/Description:", bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w")
product_entry = tk.Entry(form_frame)
product_entry.pack(pady=(0, 10), fill="x")

tk.Label(form_frame, text="Amount:", bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w")
amount_entry = tk.Entry(form_frame)
amount_entry.pack(pady=(0, 10), fill="x")

submit_button = tk.Button(form_frame, text="Add Expense", command=submit_expense, bg=ACCENT_COLOR, fg="white", font=("Segoe UI", 11, "bold"), relief="flat", pady=8)
submit_button.pack(fill="x", pady=(5, 0))

tk.Label(window, text="Reports", font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(20, 10))

report_frame = tk.Frame(window, bg=BG_COLOR)
report_frame.pack(padx=20, fill="x")

def styled_button(parent, text, command):
    return tk.Button(parent, text=text, command=command, bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10), relief="flat", pady=8)

styled_button(report_frame, "Show Total Spending", show_total_label).pack(fill="x", pady=4)
styled_button(report_frame, "Today's Graph", show_today_graph).pack(fill="x", pady=4)
styled_button(report_frame, "This Week's Graph", show_weekly_graph).pack(fill="x", pady=4)
styled_button(report_frame, "This Month's Graph", show_monthly_graph).pack(fill="x", pady=4)
styled_button(report_frame, "Overall Category Graph", show_overall_graph).pack(fill="x", pady=4)

clear_button = tk.Button(window, text="🗑 Clear All Data", command=clear_all_data, bg=DANGER_COLOR, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", pady=8)
clear_button.pack(padx=20, pady=(20, 20), fill="x")

window.mainloop()