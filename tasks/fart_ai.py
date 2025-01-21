import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import sounddevice as sd
import librosa

# Load YAMNet model from TensorFlow Hub
MODEL_URL = "https://tfhub.dev/google/yamnet/1"
yamnet_model = hub.load(MODEL_URL)

# Load the YAMNet class map (labels)
class_map_path = tf.keras.utils.get_file(
    'yamnet_class_map.csv',
    'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
)
class_map = np.loadtxt(class_map_path, delimiter=",", dtype="str", skiprows=1, quotechar='"')


def record_audio(duration=1, sample_rate=16000):
    """Record audio from the microphone."""
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()  # Wait for recording to finish
    print("Recording complete.")
    return audio.flatten()


def preprocess_audio(audio, sample_rate):
    """Resample and normalize audio to match YAMNet requirements."""
    audio_resampled = librosa.resample(audio, orig_sr=sample_rate, target_sr=16000)
    return audio_resampled


def classify_audio(audio):
    """Classify the audio using the YAMNet model."""
    # Run the YAMNet model
    scores, embeddings, spectrogram = yamnet_model(audio)

    # Get the top class index
    top_class = tf.argmax(scores, axis=1).numpy()[0]

    # Get the class name
    class_name = class_map[top_class][2]
    return class_name


def fart_detect():
    sample_rate = 44100  # Original sample rate for recording
    duration = 2  # Record for 2 seconds

    while True:
        audio = record_audio(duration, sample_rate)
        processed_audio = preprocess_audio(audio, sample_rate)
        detected_class = classify_audio(processed_audio)

        if "fart" in detected_class.lower():  # Check if the detected sound is a fart
            print("Fart sound detected!")
            return True
        else:
            print(f"Detected: {detected_class}")
