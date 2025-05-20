# --- Activate your virtual environment using: THIS CODE ".\venv\Scripts\activate" BEFORE RUNNING AVA.PY
import speech
import tasks
import config
import speech_recognition as sr
import sys # Add Import

# --- Function for setting system volume ---
import os
# --- Function for setting system volume ---
def set_volume(percentage: int):
  import os

  # Normalize the percentage to be between 0 and 100
  percentage = max(0, min(percentage, 100))

  # Define the command for setting the volume based on the operating system
  if os.name == 'nt':  # Windows
      import comtypes
      from comtypes import CLSCTX_ALL
      from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

      devices = AudioUtilities.GetSpeakers()
      interface = devices.Activate(
          IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
      volume = comtypes.Cast(interface, IAudioEndpointVolume)

      # Set master volume level
      volume.SetMasterVolumeLevelScalar(percentage / 100, None)

  elif os.name == 'posix':  # Linux, macOS, or any other POSIX system
      # For Linux, you might use 'amixer' command or similar.
      # This is an example and might need adaptation based on the specific system
      # and installed audio management tools.
      os.system(f"amixer set Master {percentage}%")

  else:
      print("Unsupported operating system for volume control.")

# End set_volume


# --- Function for getting system volume ---
def get_volume() -> int:
  import os

  # Define the command for setting the volume based on the operating system
  if os.name == 'nt':  # Windows
      import comtypes
      from comtypes import CLSCTX_ALL
      from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

      devices = AudioUtilities.GetSpeakers()
      interface = devices.Activate(
          IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
      volume = comtypes.Cast(interface, IAudioEndpointVolume)

      # Get master volume level
      current_volume = volume.GetMasterVolumeLevelScalar() * 100
      return int(current_volume)

  elif os.name == 'posix':  # Linux, macOS, or any other POSIX system
      # For Linux, you might use 'amixer' command or similar.
      # This is an example and might need adaptation based on the specific system
      # and installed audio management tools.
      # os.system(f"amixer set Master {percentage}%")
      print("Volume retrieval not implemented for this OS.")
      return 50

  else:
      print("Unsupported operating system for volume retrieval.")
      return 50

# End get_volume

# Dictionary of translated responses (MOVED TO AVA.PY for main messages)
RESPONSES = {
    "greeting": {
        "en": "Hello, I am AIRLOOM. How can I help you?",
        "sw": "Halo, mimi ni AIRLOOM. Naweza kukusaidia vipi?"
    },
    "volume_level": {
        "en": "My volume is {volume}%.",
        "sw": "Sauti yangu ni {volume}%."
    },
    "goodbye": {
        "en": "Goodbye!",
        "sw": "Kwaheri!"
    },
    "not_sure": {
        "en": "I'm not sure I understand. Please try again.",
        "sw": "Sielewi. Tafadhali jaribu tena."
    },
    "setting_volume": {
      "en": "Setting volume to {volume}%.",
      "sw": "Ninaweka sauti hadi {volume}%."
    },
    "volume_error": {
        "en": "I don't understand that volume percentage.",
        "sw": "Sielewi asilimia hiyo ya sauti."
    },
    "volume_index_error": {
        "en": "What percentage of the volume do you want?",
        "sw": "Unataka asilimia gani ya sauti?"
    }
}


def get_localized_response(key, language, **kwargs):
    """Gets a localized response from the RESPONSES dictionary."""
    try:
        return RESPONSES[key][language].format(**kwargs)
    except KeyError:
        # Fallback to English if translation is missing
        print(f"Translation missing for key '{key}' in language '{language}'. Using English fallback.")
        return RESPONSES[key]["en"].format(**kwargs)
    except Exception as e:
        print(f"Error formatting response for key '{key}': {e}")
        return "Sorry, I encountered an error." #General Error Message

WAKE_WORD = "hey AIRLOOM"  # Choose your wake word

def main():
    # Get the volume percentage
    current_volume = config.get_volume()

    # Set up recognizer (moved here)
    r = sr.Recognizer()

    # Use a local alias instead of the module directly
    #speech.speak(get_localized_response("greeting", config.TTS_LANGUAGE) + " " + get_localized_response("volume_level", config.TTS_LANGUAGE, volume=current_volume))
    greeting_message = get_localized_response("greeting", config.TTS_LANGUAGE)
    volume_level_message = get_localized_response("volume_level", config.TTS_LANGUAGE, volume=current_volume)
    speech.speak(f"{greeting_message} {volume_level_message}")
    #Possible Keywords for a more robust NLP Engine
    open_keywords = ["open", "fungua"]
    search_keywords = ["search", "tafuta"]
    exit_keywords = ["exit", "quit", "toka", "close"] # Added close keyword
    volume_keywords = ["set volume", "weka sauti"]

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening for the wake word...")

        while True:
            try:
                audio = r.listen(source, phrase_time_limit=5, timeout=5)
            except sr.WaitTimeoutError:
                print("No speech detected. Listening for wake word...")
                continue

            try:
                text = r.recognize_google(audio).lower()  # Convert to lowercase
                print(f"You said: {text}")

                if WAKE_WORD in text:
                    print("Wake word detected!")
                    # Now listen for the command after the wake word
                    command = text.replace(WAKE_WORD, "").strip()
                    process_command(command)  # Function to handle the command
                else:
                    print("Wake word not detected.")

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

def process_command(command):
    # Here you would put your logic to understand and execute the command
    # Possible Keywords for a more robust NLP Engine
    open_keywords = ["open", "fungua"]
    search_keywords = ["search", "tafuta"]
    exit_keywords = ["exit", "quit", "toka", "close"] #Added close keyword
    volume_keywords = ["set volume", "weka sauti"]

    if any(keyword in command for keyword in open_keywords):
        app_name = command.replace("open", "").replace("fungua", "").strip()
        tasks.open_application(app_name)

    elif any(keyword in command for keyword in search_keywords):
        search_term = command.replace("search", "").replace("tafuta", "").strip()
        tasks.search_web(search_term)

    elif any(keyword in command for keyword in volume_keywords):
        parts = command.split()
        try:
            percentage = int(parts[-1])
            config.set_volume(percentage)
            # Centralize "set volume" responses
            setting_volume_message = get_localized_response("setting_volume", config.TTS_LANGUAGE, volume=percentage)
            speech.speak(setting_volume_message)
        except ValueError:
            volume_error_message = get_localized_response("volume_error", config.TTS_LANGUAGE)
            speech.speak(volume_error_message)

        except IndexError:
            volume_index_message = get_localized_response("volume_index_error", config.TTS_LANGUAGE)
            speech.speak(volume_index_message)


    elif any(keyword in command for keyword in exit_keywords):
        goodbye_message = get_localized_response("goodbye", config.TTS_LANGUAGE)
        speech.speak(goodbye_message)
        sys.exit()  # Modified call

    else:
        not_sure_message = get_localized_response("not_sure", config.TTS_LANGUAGE)
        speech.speak(not_sure_message)


if __name__ == "__main__":
    main()