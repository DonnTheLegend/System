import customtkinter as ctk
from tkinter import messagebox
from main import InventoryDashboard
from cashier import CashierApp
import json
import os

USERS_FILE = "users.json" 


def ensure_users_file():
    """Create users.json with default admin if missing."""
    if not os.path.exists(USERS_FILE):
        default_users = {
            "admin": {
                "password": "admin123",
                "role": "Admin",
                "question": "What is your mother's maiden name?",
                "answer": "bocalbos"
            }
        }
        with open(USERS_FILE, "w") as f:
            json.dump(default_users, f, indent=4)
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        if "admin" in users:
            users["admin"]["answer"] = "bocalbos"
            users["admin"]["question"] = "What is your mother's maiden name?"
            users["admin"]["role"] = "Admin"
            if "password" not in users["admin"]:
                users["admin"]["password"] = "admin123"
        else:
            users["admin"] = {
                "password": "admin123",
                "role": "Admin",
                "question": "What is your mother's maiden name?",
                "answer": "bocalbos"
            }

        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)


def load_users():
    ensure_users_file()
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users_dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users_dict, f, indent=4)


window = ctk.CTk()
window.title("HardTrack Login")
window.geometry("400x470")
window.resizable(False, False)

label = ctk.CTkLabel(window, text="Welcome!", font=("Arial", 25, "bold"))
label.pack(pady=(40, 30))

ctk.CTkLabel(window, text="Enter Username", font=("Arial", 18, "bold")).pack(anchor="w", padx=10)
username_entry = ctk.CTkEntry(window, width=380, height=35, corner_radius=10,
                              placeholder_text="Type your username")
username_entry.pack(anchor="w", padx=10, pady=(5, 20))

ctk.CTkLabel(window, text="Enter Password", font=("Arial", 18, "bold")).pack(anchor="w", padx=10)
pass_entry = ctk.CTkEntry(window, width=380, height=35, corner_radius=10,
                          placeholder_text="Type your password", show="*")
pass_entry.pack(anchor="w", padx=10, pady=(5, 10))

show_pass_var = ctk.BooleanVar()


def toggle_password():
    pass_entry.configure(show="" if show_pass_var.get() else "*")


pass_frame = ctk.CTkFrame(window, fg_color="transparent")
pass_frame.pack(anchor="w", padx=10, pady=(0, 20), fill="x")

ctk.CTkCheckBox(pass_frame, text="Show Password",
                variable=show_pass_var,
                command=toggle_password).pack(side="left")


def forgot_password_flow():
    """Forgot password flow for normal users: Confirm password only appears after Find Account."""
    fp = ctk.CTkToplevel()
    fp.title("Forgot Password")
    fp.geometry("380x470")
    fp.resizable(False, False)

    window.update_idletasks()
    fx = window.winfo_x() + (window.winfo_width() // 2 - 190)
    fy = window.winfo_y() + (window.winfo_height() // 2 - 205)
    fp.geometry(f"380x470+{fx}+{fy}")

    ctk.CTkLabel(fp, text="Forgot Password", font=("Arial", 18, "bold")).pack(pady=(14, 8))
    ctk.CTkLabel(fp, text="Enter your username:").pack(anchor="w", padx=20)

    uname_entry = ctk.CTkEntry(fp, width=320)
    uname_entry.pack(pady=6, padx=20)

    # placeholders for widgets that will be created only after Find Account
    question_label = ctk.CTkLabel(fp, text="", wraplength=340)
    answer_entry = ctk.CTkEntry(fp, width=320)
    new_pass_entry = ctk.CTkEntry(fp, width=320, show="*")

    # confirm_pass_entry and reset_button will be created only after the account is found
    confirm_pass_entry = None
    reset_button = None

    def reset_password(username):
        nonlocal confirm_pass_entry
        answer = answer_entry.get().strip()
        new_pass = new_pass_entry.get().strip()

        if confirm_pass_entry is None:
            messagebox.showerror("Error", "Confirm password field missing.")
            return
        confirm_pass = confirm_pass_entry.get().strip()

        if not answer or not new_pass or not confirm_pass:
            messagebox.showerror("Error", "Answer and both password fields are required.")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        users = load_users()
        stored = users.get(username)

        if not stored:
            messagebox.showerror("Error", "User not found (unexpected).")
            return

        if answer.lower() != stored.get("answer", "").lower():
            messagebox.showerror("Error", "Incorrect answer.")
            return

        users[username]["password"] = new_pass
        save_users(users)
        messagebox.showinfo("Success", "Password reset successfully!")
        fp.destroy()

    def check_username():
        nonlocal confirm_pass_entry, reset_button
        username = uname_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter your username.")
            return

        users = load_users()
        if username not in users:
            messagebox.showerror("Error", "Username not found.")
            return

        # disable the Find Account button to avoid duplicates
        find_btn.configure(state="disabled")

        # show security question
        q = users[username].get("question", "")
        question_label.configure(text=f"Security question: {q}")
        question_label.pack(padx=20, pady=(10, 4))

        # show answer entry
        ctk.CTkLabel(fp, text="Answer:").pack(anchor="w", padx=20)
        answer_entry.pack(padx=20, pady=(4, 8))

        # show new password entry
        ctk.CTkLabel(fp, text="New Password:").pack(anchor="w", padx=20)
        new_pass_entry.pack(padx=20, pady=(4, 8))

        # show confirm password entry (only now)
        ctk.CTkLabel(fp, text="Confirm Password:").pack(anchor="w", padx=20)
        confirm_pass_entry = ctk.CTkEntry(fp, width=320, show="*")
        confirm_pass_entry.pack(padx=20, pady=(4, 10))

        # show the reset button (captures current username via lambda)
        reset_button = ctk.CTkButton(fp, text="Reset Password", width=300,
                                     command=lambda: reset_password(username))
        reset_button.pack(pady=6)

    find_btn = ctk.CTkButton(fp, text="Find Account", width=300, command=check_username)
    find_btn.pack(pady=12)


forgot_label = ctk.CTkLabel(pass_frame, text="Forgot Password?",
                            font=("Arial", 13, "underline"),
                            cursor="hand2")
forgot_label.pack(side="left", padx=(152, 0))
forgot_label.bind("<Button-1>", lambda e: forgot_password_flow())


def login():
    username = username_entry.get().strip()
    password = pass_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password.")
        return

    users = load_users()
    user = users.get(username)

    if not user or user.get("password") != password:
        messagebox.showerror("Error", "Invalid login credentials!")
        return

    role = user.get("role", "User")
    messagebox.showinfo("Success", f"{role} Logged In!")

    if role == "Admin":
        window.destroy()
        app = InventoryDashboard()
        app.mainloop()

    elif role == "Cashier":
        window.withdraw()
        app = CashierApp()
        app.mainloop()
        window.deiconify()


ctk.CTkButton(window, text="Login", height=40, corner_radius=10,
              command=login).pack(fill="x", padx=10, pady=(10, 10))


def open_register_window():
    reg = ctk.CTkToplevel()
    reg.title("Register New User")
    reg.geometry("400x580")
    reg.resizable(False, False)
    reg.lift()
    reg.grab_set()
    reg.focus_force()

    window.update_idletasks()
    x = window.winfo_x() + (window.winfo_width() // 2 - 200)
    y = window.winfo_y() + (window.winfo_height() // 2 - 260)
    reg.geometry(f"400x550+{x}+{y}")

    ctk.CTkLabel(reg, text="Create New User", font=("Arial", 22, "bold")).pack(pady=12)

    ctk.CTkLabel(reg, text="Username:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)
    reg_user = ctk.CTkEntry(reg, width=360, height=38, placeholder_text="Enter new username")
    reg_user.pack(padx=20, pady=(6, 12))


    ctk.CTkLabel(reg, text="Password:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)
    reg_pass = ctk.CTkEntry(reg, width=360, height=38,
                            placeholder_text="Enter password", show="*")
    reg_pass.pack(padx=20, pady=(6, 8))

    ctk.CTkLabel(reg, text="Confirm Password:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)
    reg_confirm = ctk.CTkEntry(reg, width=360, height=38,
                               placeholder_text="Re-enter password", show="*")
    reg_confirm.pack(padx=20, pady=(6, 4))

    
    show_reg_pass_var = ctk.BooleanVar()

    def toggle_reg_password():
        ch = "" if show_reg_pass_var.get() else "*"
        reg_pass.configure(show=ch)
        reg_confirm.configure(show=ch)

    ctk.CTkCheckBox(
        reg,
        text="Show Password",
        variable=show_reg_pass_var,
        command=toggle_reg_password
    ).pack(anchor="w", padx=24, pady=(0, 10))

    questions = [
        "What is your mother's maiden name?",
        "What was the name of your first pet?",
        "What city were you born in?",
        "What is the name of your first school?",
        "What is your favorite movie?",
        "What is your father's middle name?",
        "What is the name of your childhood best friend?"
    ]

    ctk.CTkLabel(reg, text="Security Question:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)
    reg_question = ctk.CTkOptionMenu(reg, values=questions, width=360)
    reg_question.set(questions[0])
    reg_question.pack(padx=20, pady=(6, 12))

    ctk.CTkLabel(reg, text="Answer:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)
    reg_answer = ctk.CTkEntry(reg, width=360, height=38, placeholder_text="Enter answer")
    reg_answer.pack(padx=20, pady=(6, 12))

    def save_user():
        username = reg_user.get().strip()
        password = reg_pass.get().strip()
        confirm = reg_confirm.get().strip()
        question = reg_question.get().strip()
        answer = reg_answer.get().strip()
        role = "Cashier"  # Force every new registered account to be a Cashier

        if not username or not password or not confirm or not answer:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        users = load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists!")
            return

        users[username] = {
            "password": password,
            "question": question,
            "answer": answer,
            "role": role
        }

        save_users(users)
        messagebox.showinfo("Success", "User Registered Successfully!")
        reg.destroy()

    ctk.CTkButton(reg, text="Register Account", height=45,
                  command=save_user).pack(pady=8)


ctk.CTkButton(window, text="Register New User", height=40, corner_radius=10,
              command=open_register_window).pack(fill="x", padx=10, pady=(0, 20))


def cashier_login():
    if cashier_user.get().strip() == "" or cashier_pass.get().strip() == "":
        messagebox.showerror("Error", "Enter cashier credentials.")
        return

    users = load_users()
    u = users.get(cashier_user.get().strip())

    if not u or u.get("password") != cashier_pass.get().strip() or u.get("role") != "Cashier":
        messagebox.showerror("Error", "Invalid cashier credentials!")
        return

    messagebox.showinfo("Success", "Cashier Logged in!")
    window.withdraw()
    app = CashierApp()
    app.mainloop()
    window.deiconify()


def admin_login():
    if admin_user.get().strip() == "" or admin_pass.get().strip() == "":
        messagebox.showerror("Error", "Enter admin credentials.")
        return

    users = load_users()
    u = users.get(admin_user.get().strip())

    if not u or u.get("password") != admin_pass.get().strip() or u.get("role") != "Admin":
        messagebox.showerror("Error", "Invalid admin credentials!")
        return

    messagebox.showinfo("Success", "Admin logged in!")
    window.destroy()
    app = InventoryDashboard()
    app.mainloop()


def forgot_admin_password_flow():
    fp = ctk.CTkToplevel()
    fp.title("Admin Password Reset")
    fp.geometry("380x380")
    fp.resizable(False, False)
    fp.grab_set()
    fp.focus_force()

    window.update_idletasks()
    fx = window.winfo_x() + (window.winfo_width() // 2 - 190)
    fy = window.winfo_y() + (window.winfo_height() // 2 - 170)
    fp.geometry(f"380x380+{fx}+{fy}")

    ctk.CTkLabel(fp, text="Admin Password Reset",
                 font=("Arial", 18, "bold")).pack(pady=12)

    users = load_users()
    admin_data = users.get("admin")

    ctk.CTkLabel(
        fp,
        text=f"Security Question:\n{admin_data['question']}",
        wraplength=340
    ).pack(pady=10)

    ctk.CTkLabel(fp, text="Answer:").pack(anchor="w", padx=20)
    answer_entry = ctk.CTkEntry(fp, width=320)
    answer_entry.pack(pady=5)

    ctk.CTkLabel(fp, text="New Password:").pack(anchor="w", padx=20)
    new_pass_entry = ctk.CTkEntry(fp, width=320, show="*")
    new_pass_entry.pack(pady=5)

    # Confirm password entry for admin flow
    ctk.CTkLabel(fp, text="Confirm Password:").pack(anchor="w", padx=20)
    confirm_pass_entry = ctk.CTkEntry(fp, width=320, show="*")
    confirm_pass_entry.pack(pady=5)

    show_new_pass_var = ctk.BooleanVar()
    ctk.CTkCheckBox(
        fp,
        text="Show Password",
        variable=show_new_pass_var,
        command=lambda: new_pass_entry.configure(
            show="" if show_new_pass_var.get() else "*"
        )
    ).pack(anchor="w", padx=20, pady=(0, 10))

    def reset_admin_password():
        answer = answer_entry.get().strip()
        new_pass = new_pass_entry.get().strip()
        confirm_pass = confirm_pass_entry.get().strip()

        if not answer or not new_pass or not confirm_pass:
            messagebox.showerror("Error", "All fields are required.")
            return

        if answer.lower() != admin_data["answer"].lower():
            messagebox.showerror("Error", "Incorrect answer.")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        admin_data["password"] = new_pass
        save_users(users)
        messagebox.showinfo("Success", "Admin password updated!")
        fp.destroy()

    ctk.CTkButton(fp, text="Reset Password", width=320,
                  command=reset_admin_password).pack(pady=12)


def open_admin_window():
    admin_window = ctk.CTkToplevel()
    admin_window.title("Admin Login")
    admin_window.geometry("360x345")
    admin_window.resizable(False, False)
    admin_window.lift()
    admin_window.grab_set()
    admin_window.focus_force()

    window_x = window.winfo_x()
    window_y = window.winfo_y()
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    admin_width = 360
    admin_height = 345

    pos_x = window_x + (window_width // 2) - (admin_width // 2)
    pos_y = window_y + (window_height // 2) - (admin_height // 2)

    admin_window.geometry(f"{admin_width}x{admin_height}+{pos_x}+{pos_y}")

    ctk.CTkLabel(
        admin_window,
        text="Admin Login Only",
        font=("Arial", 20, "bold")
    ).pack(pady=(20, 10))

    global admin_user, admin_pass
    admin_user = ctk.CTkEntry(
        admin_window,
        width=320,
        height=35,
        corner_radius=10,
        placeholder_text="Admin Username"
    )
    admin_user.pack(pady=8)

    admin_pass = ctk.CTkEntry(
        admin_window,
        width=320,
        height=35,
        corner_radius=10,
        placeholder_text="Admin Password",
        show="*"
    )
    admin_pass.pack(pady=8)

    show_admin_var = ctk.BooleanVar()
    ctk.CTkCheckBox(
        admin_window,
        text="Show Password",
        variable=show_admin_var,
        command=lambda: admin_pass.configure(
            show="" if show_admin_var.get() else "*"
        )
    ).pack(anchor="w", padx=30, pady=(5, 10))

    forgot_admin = ctk.CTkLabel(
        admin_window,
        text="Forgot Admin Password?",
        font=("Arial", 12, "underline"),
        cursor="hand2"
    )
    forgot_admin.pack()
    forgot_admin.bind("<Button-1>", lambda e: forgot_admin_password_flow())

    ctk.CTkButton(
        admin_window,
        text="Login",
        width=320,
        height=45,
        command=admin_login
    ).pack(pady=10)


def open_cashier_window():
    cashier_window = ctk.CTkToplevel()
    cashier_window.title("Cashier Login")
    cashier_window.geometry("360x315")
    cashier_window.resizable(False, False)
    cashier_window.lift()
    cashier_window.grab_set()
    cashier_window.focus_force()

    window.update_idletasks()
    win_x = window.winfo_x()
    win_y = window.winfo_y()
    win_w = window.winfo_width()
    win_h = window.winfo_height()

    cw, ch = 360, 315
    pos_x = win_x + (win_w // 2) - (cw // 2)
    pos_y = win_y + (win_h // 2) - (ch // 2)

    cashier_window.geometry(f"{cw}x{ch}+{pos_x}+{pos_y}")

    global cashier_user, cashier_pass

    ctk.CTkLabel(
        cashier_window,
        text="Cashier Login Only",
        font=("Arial", 20, "bold")
    ).pack(pady=(20, 10))

    cashier_user = ctk.CTkEntry(
        cashier_window,
        placeholder_text="Cashier Username",
        width=320,
        height=45
    )
    cashier_user.pack(pady=8)

    cashier_pass = ctk.CTkEntry(
        cashier_window,
        placeholder_text="Cashier Password",
        show="*",
        width=320,
        height=45
    )
    cashier_pass.pack(pady=8)

    show_cashier_var = ctk.BooleanVar()
    ctk.CTkCheckBox(
        cashier_window,
        text="Show Password",
        variable=show_cashier_var,
        command=lambda: cashier_pass.configure(
            show="" if show_cashier_var.get() else "*"
        )
    ).pack(anchor="w", padx=30, pady=(10, 20))

    ctk.CTkButton(
        cashier_window,
        text="Login",
        width=320,
        height=45,
        command=cashier_login
    ).pack()


admin_label = ctk.CTkLabel(
    window,
    text="Login as Admin?",
    font=("Arial", 13, "underline"),
    cursor="hand2"
)
admin_label.pack(anchor="w", padx=145, pady=(0, 14))
admin_label.bind("<Button-1>", lambda e: open_admin_window())

ensure_users_file()
window.mainloop()