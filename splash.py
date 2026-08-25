import customtkinter as ctk
from PIL import Image
import os
import sys

class SplashScreen:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("AlphaMat - Smart Interactive Learning Mat")
        self.window.geometry("580x680")
        self.window.resizable(False, False)

        # Center the window on screen
        self.center_window(580, 680)

        # Main Card Frame
        self.card = ctk.CTkFrame(
            self.window,
            width=520,
            height=620,
            corner_radius=24,
            fg_color="#131B2E",
            border_width=2,
            border_color="#38BDF8"
        )
        self.card.pack(pady=30, padx=30, fill="both", expand=True)
        self.card.pack_propagate(False)

        # Top Badge
        badge_frame = ctk.CTkFrame(self.card, fg_color="#1E293B", corner_radius=20)
        badge_frame.pack(pady=(22, 10))
        badge_label = ctk.CTkLabel(
            badge_frame,
            text="✨ NEXT-GEN SMART LEARNING ✨",
            font=("Segoe UI", 11, "bold"),
            text_color="#38BDF8"
        )
        badge_label.pack(padx=16, pady=4)

        # Logo Image Display
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
                    size=(180, 180)
                )
                self.logo_label = ctk.CTkLabel(self.card, image=self.logo_img, text="")
                self.logo_label.pack(pady=(5, 10))
            except Exception as e:
                self.logo_label = ctk.CTkLabel(
                    self.card,
                    text="🎨",
                    font=("Segoe UI", 64)
                )
                self.logo_label.pack(pady=(5, 10))
        else:
            self.logo_label = ctk.CTkLabel(
                self.card,
                text="🎨",
                font=("Segoe UI", 64)
            )
            self.logo_label.pack(pady=(5, 10))

        # Title
        title = ctk.CTkLabel(
            self.card,
            text="alphaMat",
            font=("Segoe UI", 32, "bold"),
            text_color="#60A5FA"
        )
        title.pack(pady=(0, 2))

        # Subtitle / Tagline
        subtitle = ctk.CTkLabel(
            self.card,
            text="Smart Interactive 3D Learning Mat for Kids",
            font=("Segoe UI", 13, "bold"),
            text_color="#FBBF24"
        )
        subtitle.pack(pady=(0, 12))

        # Product Description Card
        desc_frame = ctk.CTkFrame(
            self.card,
            fg_color="#0F172A",
            corner_radius=14,
            border_width=1,
            border_color="#334155"
        )
        desc_frame.pack(padx=25, pady=(0, 18), fill="x")

        desc_text = (
            "🚀 Step onto the mat & explore the world of 3D AR learning!\n\n"
            "AlphaMat bridges physical step sensors with interactive 3D visual "
            "and audio feedback, making letters, animals & fruits discovery fun, "
            "engaging, and unforgettable."
        )
        desc_label = ctk.CTkLabel(
            desc_frame,
            text=desc_text,
            font=("Segoe UI", 12),
            text_color="#CBD5E1",
            justify="center",
            wraplength=430
        )
        desc_label.pack(padx=16, pady=12)

        # Status Text
        self.status_label = ctk.CTkLabel(
            self.card,
            text="⚡ Initializing AlphaMat system...",
            font=("Segoe UI", 12, "italic"),
            text_color="#94A3B8"
        )
        self.status_label.pack(pady=(0, 6))

        # Progress Bar
        self.progress = ctk.CTkProgressBar(
            self.card,
            width=380,
            height=10,
            corner_radius=5,
            progress_color="#38BDF8",
            fg_color="#1E293B"
        )
        self.progress.pack(pady=(0, 15))
        self.progress.set(0)

        # Skip Button
        self.skip_btn = ctk.CTkButton(
            self.card,
            text="Enter Login ➔",
            width=140,
            height=32,
            font=("Segoe UI", 12, "bold"),
            corner_radius=10,
            fg_color="#334155",
            hover_color="#475569",
            text_color="#F8FAFC",
            command=self.open_login
        )
        self.skip_btn.pack(pady=(0, 10))

        # Animation state
        self.progress_value = 0.0
        self.step_count = 0
        self.is_closing = False

        # Start animation sequence
        self.window.after(100, self.animate_progress)
        self.window.mainloop()

    def center_window(self, width, height):
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def animate_progress(self):
        if self.is_closing:
            return

        self.step_count += 1
        self.progress_value += 0.02
        self.progress.set(min(self.progress_value, 1.0))

        # Dynamic status updates
        if self.step_count == 8:
            self.status_label.configure(text="📚 Loading 3D models & educational dataset...")
        elif self.step_count == 22:
            self.status_label.configure(text="📡 Syncing interactive mat touch sensors...")
        elif self.step_count == 36:
            self.status_label.configure(text="✨ System ready! Welcome to AlphaMat...")

        if self.progress_value >= 1.0 or self.step_count >= 50:
            self.window.after(400, self.open_login)
        else:
            self.window.after(70, self.animate_progress)

    def open_login(self):
        if self.is_closing:
            return
        self.is_closing = True
        try:
            self.window.destroy()
        except Exception:
            pass

        from login import LoginPage
        LoginPage()

if __name__ == "__main__":
    SplashScreen()
