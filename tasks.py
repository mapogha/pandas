# modules/tasks.py
import os
import webbrowser
import config
import speech  # Import the speech module for centralized speaking

# Dictionary of translated responses
RESPONSES = {
    "application_not_recognized": {
        "en": "Application {app_name} not recognized.",
        "sw": "Programu {app_name} haitambuliwi."
    },
    "error_opening_application": {
        "en": "Error opening {app_name}: {error}",
        "sw": "Kosa wakati wa kufungua {app_name}: {error}"
    },
    "searching_web": {
        "en": "Searching the web for {search_query}",
        "sw": "Ninatafuta mtandaoni kuhusu {search_query}."
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

def open_application(app_name):
    try:
        # Centralize getting app path to one line for readability
        app_path = config.APPLICATION_PATHS.get(app_name.lower())

        if app_path:
            os.startfile(app_path)
        else:
            error_message = get_localized_response("application_not_recognized", config.TTS_LANGUAGE, app_name=app_name)
            print(error_message)
            speech.speak(error_message)
    except Exception as e:
        error_message = get_localized_response("error_opening_application", config.TTS_LANGUAGE, app_name=app_name, error=str(e))
        print(error_message)
        speech.speak(error_message)


def search_web(search_query):
    try:
        speech_message = get_localized_response("searching_web", config.TTS_LANGUAGE, search_query=search_query) #moved up
        speech.speak(speech_message)
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    except Exception as e:
        print(f"Error searching the web: {e}")
        speech.speak("Sorry, I encountered an error while searching the web.") #speak the error