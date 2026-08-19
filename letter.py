import customtkinter as ctk


class Letter:

    def __init__(self, mode):

        self.mode = mode
        ctk.set_appearance_mode("dark")

        self.window = ctk.CTk()
        self.window.title(f"Interactive Learning Mat - {mode} Alphabet Choice")
        self.window.geometry("520x640")
        self.window.resizable(False, False)

        accent_color = "#F59E0B" if mode == "Animal" else "#10B981"
        hover_color = "#D97706" if mode == "Animal" else "#059669"

        # Card frame
        self.card = ctk.CTkFrame(
            self.window,
            width=460,
            height=580,
            corner_radius=22,
            fg_color="#1E232F",
            border_width=2,
            border_color=accent_color
        )
        self.card.pack(pady=30, padx=30, fill="both", expand=True)
        self.card.pack_propagate(False)

        title = ctk.CTkLabel(
            self.card,
            text=f"🔤 {mode} - Choose Letter",
            font=("Segoe UI", 24, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(pady=(25, 4))

        subtitle = ctk.CTkLabel(
            self.card,
            text="Select a starting alphabet to view items",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )
        subtitle.pack(pady=(0, 20))

        letters = ["A", "B", "C", "D", "E", "F"]

        for letter in letters:

            btn = ctk.CTkButton(
                self.card,
                text=f"Letter   {letter}",
                width=280,
                height=45,
                font=("Segoe UI", 16, "bold"),
                corner_radius=14,
                fg_color=accent_color,
                hover_color=hover_color,
                command=lambda l=letter: self.open_selection(l)
            )

            btn.pack(pady=7)

        back = ctk.CTkButton(
            self.card,
            text="⬅ Back to Category",
            width=200,
            height=40,
            font=("Segoe UI", 14),
            corner_radius=12,
            fg_color="#475569",
            hover_color="#334155",
            command=self.go_back
        )

        back.pack(pady=(20, 10))

        # Register hardware serial listener
        from hardware_listener import listener
        listener.register(self.window, self.handle_hardware_input)

        self.window.mainloop()

    # -----------------------------------------

    def handle_hardware_input(self, data):
        val = data.strip().upper()
        if val in ["A", "B", "C", "D", "E", "F"]:
            self.open_selection(val)

    # -----------------------------------------

    def open_selection(self, letter):
        from hardware_listener import listener
        listener.deregister()
        self.window.destroy()

        from selection import Selection

        Selection(letter, self.mode)

    # -----------------------------------------

    def go_back(self):
        from hardware_listener import listener
        listener.deregister()
        self.window.destroy()

        from category import Category

        Category()