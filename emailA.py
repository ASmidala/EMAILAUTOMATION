import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage

# --- Configuration & Tools ---
listener = sr.Recognizer()
engine = pyttsx3.init()

# Update this dictionary with unique names
email_list = {
    "dude": 'saiduabubakarmidala1@gmail.com',
    "abubakar": 'abubakarsaeedmidala6@gmail.com',
    "office": 'work_example@gmail.com'
}


def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def get_info():
    try:
        with sr.Microphone() as source:
            # Adjusts for background noise for 1 second
            listener.adjust_for_ambient_noise(source, duration=1)
            print('Listening...')
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            # Use the free Google API
            info = listener.recognize_google(voice)
            print(f"User said: {info}")
            return info.lower()
    except Exception as e:
        print(f"Skipping... (Error: {e})")
        return None


# --- Core Email Logic ---
def send_email(receiver, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # IMPORTANT: Use an 'App Password', not your main Gmail password
        server.login('saiduabubakarmidala1@gmail.com', 'Midala5224')

        email = EmailMessage()
        email['From'] = 'saiduabubakarmidala1@gmail.com'
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(message)

        server.send_message(email)
        server.quit()
        talk('Your email was sent successfully.')
    except Exception as e:
        print(f"Failed to send email: {e}")
        talk("I couldn't send the email. Check your login credentials.")


def get_email_info():
    talk('To whom do you want to send an email?')
    name = get_info()

    # Crucial Fix: Check if name is None OR not in the list
    if name and name in email_list:
        receiver = email_list[name]

        talk('What is the subject of your email?')
        subject = get_info() or "No Subject"

        talk('What is the message?')
        message = get_info() or "Empty message."

        send_email(receiver, subject, message)

        # Ask to repeat
        talk('Do you want to send another one?')
        response = get_info()
        if response and 'yes' in response:
            get_email_info()
    else:
        talk("I didn't recognize that name in your contact list.")


# --- The "Safe" Execution Block ---
if __name__ == "__main__":
    get_email_info()