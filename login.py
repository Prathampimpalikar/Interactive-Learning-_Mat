import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

class LoginPage:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("AlphaMat - Login")
        self.window.geometry("520x580")
        self.window.resizable(False, False)

        # Center window
        self.center_window(520, 580)

        # Main decorative card frame
        self.card = ctk.CTkFrame(
            self.window,
            width=460,
            height=520,
            corner_radius=22,
            fg_color="#1E232F",
            border_width=2,
            border_color="#3B82F6"
        )
        self.card.pack(pady=25, padx=25, fill="both", expand=True)
        self.card.pack_propagate(False)

        # Logo display
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "images", "alphamat_logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(base_dir, "images", "logo.jpg")

        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                self.logo_img = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(75, 75)
                )
                self.logo_label = ctk.CTkLabel(self.card, image=self.logo_img, text="")
                self.logo_label.pack(pady=(18, 4))
            except Exception:
                pass

        # Title & Subtitle
        title = ctk.CTkLabel(
            self.card,
            text="✨ alphaMat ✨",
            font=("Segoe UI", 24, "bold"),
            text_color="#60A5FA"
        )
        title.pack(pady=(0, 2))

        subtitle = ctk.CTkLabel(
            self.card,
            text="3D Educational Experience for Kids & Students",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        )
        subtitle.pack(pady=(0, 16))

        # Username Field
        username_label = ctk.CTkLabel(
            self.card,
            text="👤 Username",
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        )
        username_label.pack(anchor="w", padx=65, pady=(0, 3))

        self.username = ctk.CTkEntry(
            self.card,
            width=330,
            height=40,
            placeholder_text="Enter username (e.g. admin)",
            font=("Segoe UI", 13),
            corner_radius=12,
            border_color="#475569",
            fg_color="#0F172A"
        )
        self.username.pack(pady=(0, 12))

        # Password Field
        password_label = ctk.CTkLabel(
            self.card,
            text="🔒 Password",
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        )
        password_label.pack(anchor="w", padx=65, pady=(0, 3))

        self.password = ctk.CTkEntry(
            self.card,
            width=330,
            height=40,
            placeholder_text="Enter password (e.g. admin123)",
            show="*",
            font=("Segoe UI", 13),
            corner_radius=12,
            border_color="#475569",
            fg_color="#0F172A"
        )
        self.password.pack(pady=(0, 18))

        # Login Button
        login_btn = ctk.CTkButton(
            self.card,
            text="🚀 LOGIN TO EXPLORE",
            width=330,
            height=44,
            font=("Segoe UI", 15, "bold"),
            corner_radius=14,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.login
        )
        login_btn.pack(pady=(0, 14))

        # Hint Badge
        hint_frame = ctk.CTkFrame(self.card, fg_color="#0F172A", corner_radius=10)
        hint_frame.pack(pady=(0, 10))
        hint_label = ctk.CTkLabel(
            hint_frame,
            text="💡 Default Login: admin / admin123",
            font=("Segoe UI", 11),
            text_color="#F59E0B"
        )
        hint_label.pack(padx=14, pady=5)

        # Allow pressing Enter key to login
        self.window.bind("<Return>", lambda event: self.login())

        self.window.mainloop()

    def center_window(self, width, height):
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

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

if __name__ == "__main__":
    LoginPage()