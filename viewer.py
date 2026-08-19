import customtkinter as ctk
from PIL import Image
import subprocess
import webbrowser
import os
import urllib.parse


def find_file_case_insensitive(directory, filename):
    if not filename or str(filename) == "nan":
        return None
    exact = os.path.join(directory, str(filename).strip())
    if os.path.exists(exact):
        return exact
    if os.path.exists(directory):
        for f in os.listdir(directory):
            if f.lower() == str(filename).strip().lower():
                return os.path.join(directory, f)
    return exact


class Viewer:

    def __init__(self, row, mode=None):

        self.row = row
        if mode is not None:
            self.mode = mode
        elif row.get("Category") == "Fruit":
            self.mode = "Fruit"
        else:
            self.mode = "Animal"
        self.letter = row["Alphabet"]

        ctk.set_appearance_mode("dark")
        self.window = ctk.CTk()
        self.window.title(f"Interactive Learning Mat - {self.row['Name']}")
        self.window.geometry("760x940")
        self.window.resizable(False, False)

        accent_color = "#F59E0B" if self.mode == "Animal" else "#10B981"
        hover_color = "#D97706" if self.mode == "Animal" else "#059669"

        # Main scrollable container
        main_frame = ctk.CTkScrollableFrame(
            self.window,
            width=720,
            height=900,
            corner_radius=20,
            fg_color="#1E232F",
            border_width=2,
            border_color=accent_color
        )
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text=f"🌟 {self.row['Name']} 🌟",
            font=("Segoe UI", 28, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(pady=(20, 15))

        # Image Frame
        image_path = find_file_case_insensitive("images", self.row["Image"])

        try:
            img = ctk.CTkImage(
                light_image=Image.open(image_path),
                size=(240, 240)
            )
            image_label = ctk.CTkLabel(
                main_frame,
                image=img,
                text=""
            )
            image_label.pack(pady=10)
        except Exception:
            placeholder_card = ctk.CTkFrame(
                main_frame,
                width=320,
                height=140,
                corner_radius=16,
                fg_color="#0F172A",
                border_width=2,
                border_color="#F87171"
            )
            placeholder_card.pack(pady=15)
            placeholder_card.pack_propagate(False)
            
            ctk.CTkLabel(
                placeholder_card,
                text="📷 Image Not Found Yet",
                font=("Segoe UI", 16, "bold"),
                text_color="#F87171"
            ).pack(pady=(20, 4))
            
            ctk.CTkLabel(
                placeholder_card,
                text=f"Please drop:  {self.row['Image']}\ninto the 'images/' folder.",
                font=("Segoe UI", 13),
                text_color="#E2E8F0",
                justify="center"
            ).pack()

        # View 360 AR Button (Prominent)
        view_btn = ctk.CTkButton(
            main_frame,
            text="🌐 VIEW 360° AR MODEL IN CHROME",
            width=380,
            height=54,
            font=("Segoe UI", 18, "bold"),
            corner_radius=16,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            command=self.open_model
        )
        view_btn.pack(pady=(15, 25))

        # Information Card
        card = ctk.CTkFrame(
            main_frame,
            width=660,
            corner_radius=16,
            fg_color="#0F172A",
            border_width=1,
            border_color="#334155"
        )
        card.pack(pady=5, padx=20, fill="x")

        heading = ctk.CTkLabel(
            card,
            text="📌 Information & Facts",
            font=("Segoe UI", 20, "bold"),
            text_color="#38BDF8"
        )
        heading.pack(pady=(15, 10))

        ignore = [
            "Alphabet",
            "Category",
            "Name",
            "Image",
            "Model",
            "Description"
        ]

        for column in self.row.index:
            if column in ignore:
                continue
            value = self.row[column]
            if str(value) == "nan":
                continue

            info_row = ctk.CTkFrame(card, fg_color="transparent")
            info_row.pack(fill="x", padx=25, pady=5)

            left = ctk.CTkLabel(
                info_row,
                text=f"{column}:",
                width=160,
                anchor="w",
                font=("Segoe UI", 15, "bold"),
                text_color="#CBD5E1"
            )
            left.pack(side="left")

            right = ctk.CTkLabel(
                info_row,
                text=str(value),
                anchor="w",
                font=("Segoe UI", 15),
                text_color="#F1F5F9"
            )
            right.pack(side="left")

        # Description
        desc_title = ctk.CTkLabel(
            card,
            text="\n📖 Description",
            font=("Segoe UI", 18, "bold"),
            text_color="#38BDF8"
        )
        desc_title.pack()

        desc = ctk.CTkLabel(
            card,
            text=str(self.row["Description"]),
            wraplength=580,
            justify="left",
            font=("Segoe UI", 15),
            text_color="#E2E8F0"
        )
        desc.pack(padx=25, pady=(8, 20))

        # Navigation Frame with two explicit buttons
        nav_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nav_frame.pack(pady=25)

        back_options_btn = ctk.CTkButton(
            nav_frame,
            text=f"⬅ Back to Options ('{self.letter}')",
            width=240,
            height=44,
            font=("Segoe UI", 14, "bold"),
            corner_radius=12,
            fg_color=accent_color,
            hover_color=hover_color,
            command=self.go_back
        )
        back_options_btn.pack(side="left", padx=10)

        back_alphabet_btn = ctk.CTkButton(
            nav_frame,
            text="🔤 Back to Alphabet Choice A-F",
            width=250,
            height=44,
            font=("Segoe UI", 14),
            corner_radius=12,
            fg_color="#475569",
            hover_color="#334155",
            command=self.go_to_alphabet
        )
        back_alphabet_btn.pack(side="left", padx=10)

        self.window.mainloop()

    # ---------------- OPEN MODEL ---------------- #

    def open_model(self):

        model_name = str(self.row["Model"]).strip()
        encoded_model = urllib.parse.quote(model_name)

        url = f"http://localhost:8001/html/viewer.html?model={encoded_model}"

        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
            r"C:\Users\pimpa\AppData\Local\Google\Chrome\Application\chrome.exe"
        ]

        chrome = None

        for path in chrome_paths:
            if os.path.exists(path):
                chrome = path
                break

        try:
            if chrome:
                subprocess.Popen([chrome, url])
            else:
                webbrowser.open(url)
        except Exception as e:
            print("Browser Error:", e)

    # ---------------- BACK TO OPTIONS ---------------- #

    def go_back(self):

        self.window.destroy()

        from selection import Selection

        Selection(
            self.letter,
            self.mode
        )

    # ---------------- BACK TO ALPHABET ---------------- #

    def go_to_alphabet(self):

        self.window.destroy()

        from letter import Letter

        Letter(self.mode)