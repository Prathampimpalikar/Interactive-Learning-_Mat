import customtkinter as ctk


class Category:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        self.window = ctk.CTk()
        self.window.title("Interactive Learning Mat - Choose Category")
        self.window.geometry("520x540")
        self.window.resizable(False, False)

        from hardware_listener import listener
        listener.deregister()

        # Main card frame
        self.card = ctk.CTkFrame(
            self.window,
            width=460,
            height=480,
            corner_radius=22,
            fg_color="#1E232F",
            border_width=2,
            border_color="#F59E0B"
        )
        self.card.pack(pady=30, padx=30, fill="both", expand=True)
        self.card.pack_propagate(False)

        title = ctk.CTkLabel(
            self.card,
            text="🎯 Choose Category",
            font=("Segoe UI", 26, "bold"),
            text_color="#FBBF24"
        )
        title.pack(pady=(35, 6))

        subtitle = ctk.CTkLabel(
            self.card,
            text="Select what you would like to learn today",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        )
        subtitle.pack(pady=(0, 35))

        animal_btn = ctk.CTkButton(
            self.card,
            text="🐯 Animals (A - F)",
            width=290,
            height=56,
            font=("Segoe UI", 18, "bold"),
            corner_radius=16,
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=lambda: self.open_letter("Animal")
        )
        animal_btn.pack(pady=(0, 18))

        fruit_btn = ctk.CTkButton(
            self.card,
            text="🍎 Fruits (A - F)",
            width=290,
            height=56,
            font=("Segoe UI", 18, "bold"),
            corner_radius=16,
            fg_color="#10B981",
            hover_color="#059669",
            command=lambda: self.open_letter("Fruit")
        )
        fruit_btn.pack(pady=(0, 30))

        back_btn = ctk.CTkButton(
            self.card,
            text="⬅ Back to Dashboard",
            width=200,
            height=42,
            font=("Segoe UI", 14),
            corner_radius=12,
            fg_color="#475569",
            hover_color="#334155",
            command=self.go_back
        )
        back_btn.pack()

        self.window.mainloop()

    def open_letter(self, mode):

        self.window.destroy()

        from letter import Letter

        Letter(mode)

    def go_back(self):

        self.window.destroy()

        from dashboard import Dashboard

        Dashboard()