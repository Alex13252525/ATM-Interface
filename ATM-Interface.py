import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- ATM Data ---
correct_pin = "1234"
balance = 1000.0
pin_attempts = 0
max_attempts = 3
transaction_history = []

# --- Window Setup ---
window = tk.Tk()
window.title("💳 ATM Interface")
window.geometry("420x450")
window.configure(bg="#f0f4f8")
window.resizable(False, False)

# --- Styling ---
style = ttk.Style()
style.theme_use('clam')

# Custom colors
primary_color = "#2c3e50"
accent_color = "#3498db"
bg_color = "#ecf0f1"
button_color = "#2980b9"
text_color = "#2c3e50"

style.configure('TFrame', background=bg_color)
style.configure('TLabel', background=bg_color, foreground=primary_color, font=('Segoe UI', 13))
style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground=accent_color)
style.configure('TEntry', font=('Segoe UI', 13))
style.configure('TButton', font=('Segoe UI', 11), padding=6, background=button_color, foreground='white')
style.map('TButton', background=[('active', accent_color)])

# --- Frames ---
frames = {
    "pin": ttk.Frame(window),
    "menu": ttk.Frame(window),
    "deposit": ttk.Frame(window),
    "withdraw": ttk.Frame(window),
    "history": ttk.Frame(window)
}

# --- Helper Functions ---
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def switch_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(pady=30)

def create_label(frame, text, style='TLabel'):
    ttk.Label(frame, text=text, style=style).pack(pady=5)

def create_entry(frame):
    entry = ttk.Entry(frame, width=25)
    entry.pack(pady=10)
    return entry

def create_buttons(frame, buttons):
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command).pack(pady=6)

# --- PIN Screen ---
def show_pin_screen():
    frame = frames["pin"]
    clear_frame(frame)
    switch_frame("pin")
    create_label(frame, "🔐 Enter Your PIN", style='Header.TLabel')
    global pin_entry
    pin_entry = create_entry(frame)
    create_buttons(frame, [
        ("Login", check_pin),
        ("Cancel", window.quit)
    ])

def check_pin():
    global pin_attempts
    if pin_entry.get() == correct_pin:
        pin_attempts = 0
        show_menu()
    else:
        pin_attempts += 1
        if pin_attempts >= max_attempts:
            messagebox.showerror("Error", "Too many attempts. Account locked.")
            window.quit()
        else:
            messagebox.showerror("Error", f"Incorrect PIN. {max_attempts - pin_attempts} attempts left.")
            pin_entry.delete(0, tk.END)

# --- Main Menu ---
def show_menu():
    frame = frames["menu"]
    clear_frame(frame)
    switch_frame("menu")
    create_label(frame, "🏦 Welcome to Your ATM", style='Header.TLabel')
    create_buttons(frame, [
        ("Check Balance", check_balance),
        ("Deposit", show_deposit),
        ("Withdraw", show_withdraw),
        ("Transaction History", show_history),
        ("Exit", window.quit)
    ])

def check_balance():
    messagebox.showinfo("Balance", f"Your current balance is ₹{balance:.2f}")

# --- Deposit ---
def show_deposit():
    frames["menu"].pack_forget()
    frame = frames["deposit"]
    clear_frame(frame)
    switch_frame("deposit")
    create_label(frame, "💰 Enter Amount to Deposit", style='Header.TLabel')
    global deposit_entry
    deposit_entry = create_entry(frame)
    create_buttons(frame, [
        ("Deposit", deposit_money),
        ("Back", show_menu)
    ])

def deposit_money():
    try:
        amount = float(deposit_entry.get())
        if amount <= 0:
            raise ValueError
        global balance
        balance += amount
        transaction_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Deposited ₹{amount:.2f}")
        messagebox.showinfo("Success", f"₹{amount:.2f} deposited.\nNew balance: ₹{balance:.2f}")
        deposit_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount.")

# --- Withdraw ---
def show_withdraw():
    frames["menu"].pack_forget()
    frame = frames["withdraw"]
    clear_frame(frame)
    switch_frame("withdraw")
    create_label(frame, "💸 Enter Amount to Withdraw", style='Header.TLabel')
    global withdraw_entry
    withdraw_entry = create_entry(frame)
    create_buttons(frame, [
        ("Withdraw", confirm_withdrawal),
        ("Back", show_menu)
    ])

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
    messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn.\nNew balance: ₹{balance:.2f}")
    withdraw_entry.delete(0, tk.END)

# --- Transaction History ---
def show_history():
    frames["menu"].pack_forget()
    frame = frames["history"]
    clear_frame(frame)
    switch_frame("history")
    create_label(frame, "📜 Transaction History", style='Header.TLabel')
    history_text = tk.Text(frame, height=10, width=40, font=("Segoe UI", 11), bg="#ffffff", fg="#2c3e50")
    history_text.pack(pady=5)
    for transaction in transaction_history:
        history_text.insert(tk.END, transaction + "\n")
    history_text.config(state="disabled")
    ttk.Button(frame, text="Back", command=show_menu).pack(pady=5)

# --- Start App ---
show_pin_screen()
window.mainloop()