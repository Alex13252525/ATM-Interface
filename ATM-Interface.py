import tkinter as tk
from tkinter import messagebox
from datetime import datetime

correct_pin = "1234"
balance = 1000.0
pin_attempts = 0
max_attempts = 3
transaction_history = []

window = tk.Tk()
window.title("ATM Interface")
window.geometry("400x400")
window.resizable(False, False)

pin_frame = tk.Frame(window)
menu_frame = tk.Frame(window)
deposit_frame = tk.Frame(window)
withdraw_frame = tk.Frame(window)
history_frame = tk.Frame(window)

def show_pin_screen():
    pin_frame.pack(pady=50)
    tk.Label(pin_frame, text="Enter PIN", font=("Arial", 14)).pack()
    global pin_entry
    pin_entry = tk.Entry(pin_frame, show="*", font=("Arial", 14))
    pin_entry.pack(pady=10)
    tk.Button(pin_frame, text="Login", command=check_pin).pack(pady=5)
    tk.Button(pin_frame, text="Cancel", command=window.quit).pack(pady=5)

def check_pin():
    global pin_attempts
    if pin_entry.get() == correct_pin:
        pin_attempts = 0
        pin_frame.pack_forget()
        show_menu()
    else:
        pin_attempts += 1
        if pin_attempts >= max_attempts:
            messagebox.showerror("Error", "Too many attempts. Account locked.")
            window.quit()
        else:
            messagebox.showerror("Error", f"Incorrect PIN. {max_attempts - pin_attempts} attempts left.")
            pin_entry.delete(0, tk.END)

def show_menu():
    menu_frame.pack(pady=30)
    tk.Label(menu_frame, text="Welcome to ATM", font=("Arial", 16)).pack(pady=10)
    tk.Button(menu_frame, text="Check Balance", width=20, command=check_balance).pack(pady=5)
    tk.Button(menu_frame, text="Deposit", width=20, command=show_deposit).pack(pady=5)
    tk.Button(menu_frame, text="Withdraw", width=20, command=show_withdraw).pack(pady=5)
    tk.Button(menu_frame, text="Transaction History", width=20, command=show_history).pack(pady=5)
    tk.Button(menu_frame, text="Exit", width=20, command=window.quit).pack(pady=5)

def check_balance():
    messagebox.showinfo("Balance", f"Your current balance is ₹{balance:.2f}")

def show_deposit():
    menu_frame.pack_forget()
    deposit_frame.pack(pady=30)
    tk.Label(deposit_frame, text="Enter amount to deposit", font=("Arial", 14)).pack()
    global deposit_entry
    deposit_entry = tk.Entry(deposit_frame, font=("Arial", 14))
    deposit_entry.pack(pady=10)
    tk.Button(deposit_frame, text="Deposit", command=deposit_money).pack(pady=5)
    tk.Button(deposit_frame, text="Back", command=back_to_menu_from_deposit).pack()

def deposit_money():
    try:
        amount = float(deposit_entry.get())
        if amount <= 0:
            raise ValueError
        global balance
        balance += amount
        transaction_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Deposited ₹{amount:.2f}")
        messagebox.showinfo("Success", f"₹{amount:.2f} deposited. New balance: ₹{balance:.2f}")
        deposit_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount.")

def back_to_menu_from_deposit():
    deposit_frame.pack_forget()
    show_menu()

def show_withdraw():
    menu_frame.pack_forget()
    withdraw_frame.pack(pady=30)
    tk.Label(withdraw_frame, text="Enter amount to withdraw", font=("Arial", 14)).pack()
    global withdraw_entry
    withdraw_entry = tk.Entry(withdraw_frame, font=("Arial", 14))
    withdraw_entry.pack(pady=10)
    tk.Button(withdraw_frame, text="Withdraw", command=confirm_withdrawal).pack(pady=5)
    tk.Button(withdraw_frame, text="Back", command=back_to_menu_from_withdraw).pack()

def confirm_withdrawal():
    try:
        amount = float(withdraw_entry.get())
        if amount <= 0 or amount > balance:
            raise ValueError
        if messagebox.askyesno("Confirm", f"Withdraw ₹{amount:.2f}?"):
            withdraw_money(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount or insufficient balance.")

def withdraw_money(amount):
    global balance
    balance -= amount
    transaction_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Withdrew ₹{amount:.2f}")
    messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn. New balance: ₹{balance:.2f}")
    withdraw_entry.delete(0, tk.END)

def back_to_menu_from_withdraw():
    withdraw_frame.pack_forget()
    show_menu()

def show_history():
    menu_frame.pack_forget()
    history_frame.pack(pady=30)
    tk.Label(history_frame, text="Transaction History", font=("Arial", 16)).pack(pady=10)
    history_text = tk.Text(history_frame, height=10, width=40, font=("Arial", 12))
    history_text.pack(pady=5)
    for transaction in transaction_history:
        history_text.insert(tk.END, transaction + "\n")
    history_text.config(state="disabled")
    tk.Button(history_frame, text="Back", command=back_to_menu_from_history).pack(pady=5)

def back_to_menu_from_history():
    history_frame.pack_forget()
    show_menu()

show_pin_screen()
window.mainloop()
