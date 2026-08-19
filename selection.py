import customtkinter as ctk

from excel_reader import get_animals_by_letter
from excel_reader import get_fruits_by_letter

from viewer import Viewer
from firebase import update_admin


class Selection:

    def __init__(self, letter, mode):

        self.letter = letter
        self.mode = mode
        ctk.set_appearance_mode("dark")

        self.window = ctk.CTk()
        self.window.title(f"Interactive Learning Mat - {mode}s ('{letter}')")
        self.window.geometry("540x680")
        self.window.resizable(False, False)

        accent_color = "#F59E0B" if mode == "Animal" else "#10B981"
        hover_color = "#D97706" if mode == "Animal" else "#059669"

        # Main decorative card
        self.card = ctk.CTkFrame(
            self.window,
            width=480,
            height=620,
            corner_radius=22,
            fg_color="#1E232F",
            border_width=2,
            border_color=accent_color
        )
        self.card.pack(pady=30, padx=30, fill="both", expand=True)
        self.card.pack_propagate(False)

        # Title & Subtitle
        title = ctk.CTkLabel(
            self.card,
            text=f"📂 {mode}s Starting With '{letter}'",
            font=("Segoe UI", 22, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(pady=(20, 4))

        subtitle = ctk.CTkLabel(
            self.card,
            text="Select an item below to view 3D AR Model & Facts",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        )
        subtitle.pack(pady=(0, 15))

        # Get data
        if mode == "Animal":
            data = get_animals_by_letter(letter)
        else:
            data = get_fruits_by_letter(letter)

        # Scrollable Frame inside card
        frame = ctk.CTkScrollableFrame(
            self.card,
            width=410,
            height=410,
            corner_radius=14,
            fg_color="#0F172A",
            border_width=1,
            border_color="#334155"
        )
        frame.pack(pady=5)

        # Buttons inside scrollable frame
        if len(data) == 0:

            ctk.CTkLabel(
                frame,
                text=f"No {mode}s Found for '{letter}'",
                font=("Segoe UI", 16),
                text_color="#94A3B8"
            ).pack(pady=40)

        else:

            for _, row in data.iterrows():

                btn = ctk.CTkButton(
                    frame,
                    text=f"✨   {row['Name']}",
                    width=360,
                    height=48,
                    font=("Segoe UI", 16, "bold"),
                    corner_radius=12,
                    fg_color=accent_color,
                    hover_color=hover_color,
                    command=lambda r=row: self.open_viewer(r)
                )

                btn.pack(pady=8, padx=10)

        # Back Button (Remains in alphabet choice)
        back = ctk.CTkButton(
            self.card,
            text="⬅ Back to Alphabet Choice A-F",
            width=260,
            height=42,
            font=("Segoe UI", 14, "bold"),
            corner_radius=12,
            fg_color="#475569",
            hover_color="#334155",
            command=self.go_back
        )
        back.pack(pady=(18, 10))

        self.window.mainloop()

    # ---------------- OPEN VIEWER ---------------- #

    def open_viewer(self, row):

        update_admin(
            row["Alphabet"],
            self.mode,
            row["Name"]
        )

        self.window.destroy()

        Viewer(row, self.mode)

    # ---------------- BACK ---------------- #

    def go_back(self):

        self.window.destroy()

        from letter import Letter

        Letter(self.mode)