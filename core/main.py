from core.speach_recognition import listen
from skills_of_bot import speak, respond
from settings.commands import TRIGGERS

if __name__ == "__main__":
    print(f"{TRIGGERS[0]} стартанул! ")
    speak(f"Привет чумба, с тобой {TRIGGERS[0]}.")
    listen(respond)
