import customtkinter as ctk


class Dashboard:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        self.window = ctk.CTk()
        self.window.title("Interactive Learning Mat - Dashboard")
        self.window.geometry("520x480")
        self.window.resizable(False, False)

        # Card frame
        self.card = ctk.CTkFrame(
            self.window,
            width=460,
            height=420,
            corner_radius=22,
            fg_color="#1E232F",
            border_width=2,
            border_color="#10B981"
        )
        self.card.pack(pady=30, padx=30, fill="both", expand=True)
        self.card.pack_propagate(False)

        title = ctk.CTkLabel(
            self.card,
            text="🌟 Interactive Learning Mat 🌟",
            font=("Segoe UI", 24, "bold"),
            text_color="#34D399"
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            self.card,
            text="Welcome! Explore 3D AR Models of Animals & Fruits",
            font=("Segoe UI", 14),
            text_color="#E2E8F0"
        )
        subtitle.pack(pady=(0, 40))

        start_btn = ctk.CTkButton(
            self.card,
            text="🚀 START ADVENTURE",
            width=260,
            height=52,
            font=("Segoe UI", 18, "bold"),
            corner_radius=16,
            fg_color="#10B981",
            hover_color="#059669",
            command=self.start
        )
        start_btn.pack(pady=(10, 20))

        logout_btn = ctk.CTkButton(
            self.card,
            text="🔒 Logout",
            width=180,
            height=40,
            font=("Segoe UI", 14),
            corner_radius=12,
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.logout
        )
        logout_btn.pack()

        self.window.mainloop()

    def start(self):

        self.window.destroy()

        from category import Category

        Category()

    def logout(self):

        self.window.destroy()

        from login import LoginPage

        LoginPage()