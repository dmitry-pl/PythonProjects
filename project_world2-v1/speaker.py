import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
engine.setProperty('voice', ru_voice_id)


def talk(text):
    engine.say(text)
    engine.runAndWait()