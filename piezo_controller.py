from machine import Pin
import urequests
import time

# ---------------- FIREBASE URL ---------------- #

FIREBASE_URL = "https://interactive-learning-mat-default-rtdb.firebaseio.com"

# ---------------- PIEZO CONNECTIONS ---------------- #

piezoA = Pin(5, Pin.IN)      # D1 -> Letter A
piezoB = Pin(4, Pin.IN)      # D2 -> Letter B
piezoC = Pin(14, Pin.IN)     # D5 -> Letter C
piezoD = Pin(12, Pin.IN)     # D6 -> Letter D

# ---------------- SEND LETTER TO FIREBASE ---------------- #

def send_letter(letter):

    try:

        url = FIREBASE_URL + "/admin/currentLetter.json"

        response = urequests.put(url, json=letter)

        print("Letter Sent :", letter)

        response.close()

    except Exception as e:

        print("Firebase Error :", e)

# ---------------- MAIN LOOP ---------------- #

print("Piezo Controller Started...")

while True:

    if piezoA.value():

        send_letter("A")
        time.sleep(1)

    elif piezoB.value():

        send_letter("B")
        time.sleep(1)

    elif piezoC.value():

        send_letter("C")
        time.sleep(1)

    elif piezoD.value():

        send_letter("D")
        time.sleep(1)

    time.sleep(0.1)