import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

class LoginPage:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("AlphaMat — Smart Interactive Learning System")
        self.window.geometry("560x660")
        self.window.resizable(False, False)

        # Center window
        self.center_window(560, 660)

        # Main decorative card frame with purple gradient theme
        self.card = ctk.CTkFrame(
            self.window,
            width=500,
            height=610,
            corner_radius=26,
            fg_color="#180C34",
            border_width=2,
            border_color="#8B5CF6"
        )
        self.card.pack(pady=25, padx=25, fill="both", expand=True)
        self.card.pack_propagate(False)

        # 3D Boy Character Avatar Display
        base_dir = os.path.dirname(os.path.abspath(__file__))
        boy_path = os.path.join(base_dir, "images", "boy_character.png")
        if not os.path.exists(boy_path):
            boy_path = os.path.join(base_dir, "images", "alphamat_logo.png")

        if os.path.exists(boy_path):
            try:
                pil_img = Image.open(boy_path)
                self.boy_img = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(120, 120)
                )
                self.boy_label = ctk.CTkLabel(self.card, image=self.boy_img, text="")
                self.boy_label.pack(pady=(16, 2))
            except Exception:
                pass

        # Title & Subtitle
        title = ctk.CTkLabel(
            self.card,
            text="Welcome Back!",
            font=("Segoe UI", 24, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(pady=(0, 2))

        subtitle = ctk.CTkLabel(
            self.card,
            text="Let's continue your learning journey with AlphaMat.",
            font=("Segoe UI", 12),
            text_color="#C084FC"
        )
        subtitle.pack(pady=(0, 16))

        # Username Field
        username_label = ctk.CTkLabel(
            self.card,
            text="👤 Email / Username",
            font=("Segoe UI", 13, "bold"),
            text_color="#EDE9FE"
        )
        username_label.pack(anchor="w", padx=65, pady=(0, 3))

        self.username = ctk.CTkEntry(
            self.card,
            width=360,
            height=42,
            placeholder_text="Enter username (e.g. admin)",
            font=("Segoe UI", 13),
            corner_radius=14,
            border_color="#A855F7",
            fg_color="#0F0624"
        )
        self.username.pack(pady=(0, 12))

        # Password Field
        password_label = ctk.CTkLabel(
            self.card,
            text="🔒 Password",
            font=("Segoe UI", 13, "bold"),
            text_color="#EDE9FE"
        )
        password_label.pack(anchor="w", padx=65, pady=(0, 3))

        self.password = ctk.CTkEntry(
            self.card,
            width=360,
            height=42,
            placeholder_text="Enter password (e.g. admin123)",
            show="*",
            font=("Segoe UI", 13),
            corner_radius=14,
            border_color="#A855F7",
            fg_color="#0F0624"
        )
        self.password.pack(pady=(0, 18))

        # Login Button
        login_btn = ctk.CTkButton(
            self.card,
            text="Login to AlphaMat →",
            width=360,
            height=46,
            font=("Segoe UI", 15, "bold"),
            corner_radius=14,
            fg_color="#7C3AED",
            hover_color="#9333EA",
            command=self.login
        )
        login_btn.pack(pady=(0, 14))

        # Hint Badge & Subtext
        hint_frame = ctk.CTkFrame(self.card, fg_color="#0F0624", corner_radius=10)
        hint_frame.pack(pady=(0, 8))
        hint_label = ctk.CTkLabel(
            hint_frame,
            text="💡 Demo Login: admin / admin123",
            font=("Segoe UI", 11),
            text_color="#F59E0B"
        )
        hint_label.pack(padx=14, pady=5)

        footer_label = ctk.CTkLabel(
            self.card,
            text="Smart Interactive Learning System",
            font=("Segoe UI", 10),
            text_color="#8B5CF6"
        )
        footer_label.pack(pady=(4, 0))

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