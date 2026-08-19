import customtkinter as ctk
from tkinter import messagebox

class LoginPage:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Interactive Learning Mat - Login")
        self.window.geometry("520x520")
        self.window.resizable(False, False)

        # Main decorative card frame
        self.card = ctk.CTkFrame(
            self.window,
            width=460,
            height=460,
            corner_radius=22,
            fg_color="#1E232F",
            border_width=2,
            border_color="#3B82F6"
        )
        self.card.pack(pady=30, padx=30, fill="both", expand=True)
        self.card.pack_propagate(False)

        # Title & Subtitle
        title = ctk.CTkLabel(
            self.card,
            text="✨ Interactive Learning Mat ✨",
            font=("Segoe UI", 24, "bold"),
            text_color="#60A5FA"
        )
        title.pack(pady=(30, 6))

        subtitle = ctk.CTkLabel(
            self.card,
            text="3D Educational Experience for Kids & Students",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )
        subtitle.pack(pady=(0, 25))

        # Username Field
        username_label = ctk.CTkLabel(
            self.card,
            text="👤 Username",
            font=("Segoe UI", 14, "bold"),
            text_color="#E2E8F0"
        )
        username_label.pack(anchor="w", padx=65, pady=(5, 4))

        self.username = ctk.CTkEntry(
            self.card,
            width=330,
            height=42,
            placeholder_text="Enter username (e.g. admin)",
            font=("Segoe UI", 14),
            corner_radius=12,
            border_color="#475569",
            fg_color="#0F172A"
        )
        self.username.pack(pady=(0, 15))

        # Password Field
        password_label = ctk.CTkLabel(
            self.card,
            text="🔒 Password",
            font=("Segoe UI", 14, "bold"),
            text_color="#E2E8F0"
        )
        password_label.pack(anchor="w", padx=65, pady=(5, 4))

        self.password = ctk.CTkEntry(
            self.card,
            width=330,
            height=42,
            placeholder_text="Enter password (e.g. admin123)",
            show="*",
            font=("Segoe UI", 14),
            corner_radius=12,
            border_color="#475569",
            fg_color="#0F172A"
        )
        self.password.pack(pady=(0, 25))

        # Login Button
        login_btn = ctk.CTkButton(
            self.card,
            text="🚀 LOGIN TO EXPLORE",
            width=330,
            height=46,
            font=("Segoe UI", 16, "bold"),
            corner_radius=14,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.login
        )
        login_btn.pack(pady=(0, 20))

        # Hint Badge
        hint_frame = ctk.CTkFrame(self.card, fg_color="#0F172A", corner_radius=10)
        hint_frame.pack(pady=(0, 15))
        hint_label = ctk.CTkLabel(
            hint_frame,
            text="💡 Default Login: admin / admin123",
            font=("Segoe UI", 12),
            text_color="#F59E0B"
        )
        hint_label.pack(padx=16, pady=6)

        # Allow pressing Enter key to login
        self.window.bind("<Return>", lambda event: self.login())

        self.window.mainloop()

    def login(self):

        user = self.username.get().strip()
        pwd = self.password.get().strip()

        if user == "admin" and pwd == "admin123":

            self.window.destroy()

            from dashboard import Dashboard

            Dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password!\nPlease check credentials and try again."
            )