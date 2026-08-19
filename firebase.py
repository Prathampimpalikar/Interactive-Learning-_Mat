from firebase_admin import credentials
from firebase_admin import db
import firebase_admin

# ======================================================
# FIREBASE INITIALIZATION
# ======================================================

if not firebase_admin._apps:

    cred = credentials.Certificate("firebase_key.json")

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://interactive-mat-b38b8-default-rtdb.firebaseio.com/"
        }
    )

# ======================================================
# UPDATE ALL VALUES
# ======================================================

def update_admin(letter, mode, item):
    try:
        ref = db.reference("admin")
        ref.update({
            "currentLetter": letter,
            "mode": mode,
            "selectedItem": item
        })
    except Exception as e:
        print("Firebase update_admin error:", e)

# ======================================================
# LETTER
# ======================================================

def update_current_letter(letter):
    try:
        ref = db.reference("admin")
        ref.update({
            "currentLetter": letter
        })
    except Exception as e:
        print("Firebase update_current_letter error:", e)


def get_current_letter():
    try:
        ref = db.reference("admin/currentLetter")
        return ref.get()
    except Exception as e:
        print("Firebase get_current_letter error:", e)
        return ""

# ======================================================
# MODE
# ======================================================

def update_mode(mode):
    try:
        ref = db.reference("admin")
        ref.update({
            "mode": mode
        })
    except Exception as e:
        print("Firebase update_mode error:", e)


def get_mode():
    try:
        ref = db.reference("admin/mode")
        return ref.get()
    except Exception as e:
        print("Firebase get_mode error:", e)
        return ""

# ======================================================
# SELECTED ITEM
# ======================================================

def update_selected_item(item):
    try:
        ref = db.reference("admin")
        ref.update({
            "selectedItem": item
        })
    except Exception as e:
        print("Firebase update_selected_item error:", e)


def get_selected_item():
    try:
        ref = db.reference("admin/selectedItem")
        return ref.get()
    except Exception as e:
        print("Firebase get_selected_item error:", e)
        return ""

# ======================================================
# RESET DATABASE
# ======================================================

def reset_admin():
    try:
        ref = db.reference("admin")
        ref.set({
            "currentLetter": "",
            "mode": "",
            "selectedItem": ""
        })
    except Exception as e:
        print("Firebase reset_admin error:", e)

# ======================================================
# CHECK CONNECTION
# ======================================================

def check_connection():
    try:
        db.reference("admin").get()
        return True
    except Exception:
        return False