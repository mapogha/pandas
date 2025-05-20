# config.py
import comtypes
from comtypes import POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Speech Recognition Settings
SPEECH_RECOGNITION_ENGINE = "google"  # Options: "google", "sphinx" (or None to disable)
SPEECH_LANGUAGE = "en-US"          # Language code for speech recognition (e.g., "en-US", "sw-KE")
SPEECH_API_KEY = "YOUR_GOOGLE_SPEECH_API_KEY" # If using Google Cloud Speech-to-Text

# Text-to-Speech Settings
TTS_ENGINE = "pyttsx3"          # Options: "pyttsx3", "gtts" (or None to disable)
TTS_VOICE = None               # Specific voice to use (optional, check pyttsx3 documentation)
TTS_LANGUAGE = "en"             # Two-letter language code for gTTS (e.g., "en", "sw")

# Default Volume Percentage
DEFAULT_VOLUME_PERCENTAGE = 70

# Paths
APPLICATION_PATHS = {
    "browser": "C:/Program Files/Google/Chrome/Application/chrome.exe",  # Example - adjust paths as necessary
    "notepad": "C:/Windows/System32/notepad.exe",
    # Add more application paths here
}

# Knowledge Base Settings (if using a separate knowledge base file)
KNOWLEDGE_BASE_PATH = "data/knowledge_base.json"  # Path to the knowledge base file

# API Keys (if using cloud services)
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"     # For OpenAI models (if using)
WEATHER_API_KEY = "YOUR_WEATHER_API_KEY"   # For weather API (if using)

# Logging Settings
LOG_LEVEL = "INFO"          # Options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
LOG_FILE = "ava.log"         # Path to the log file

# Default search engine for web searches
DEFAULT_SEARCH_ENGINE = "google" # Options: "google", "duckduckgo", etc.

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

      # Get a pointer to the interface
      # Use POINTER to create a pointer type to IAudioEndpointVolume
      AudioEndpointVolumePointer = POINTER(IAudioEndpointVolume)

      # Cast the interface to the pointer type
      volume = comtypes.cast(interface, AudioEndpointVolumePointer)

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