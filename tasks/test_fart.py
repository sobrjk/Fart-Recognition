import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import librosa

# Загрузка модели YAMNet
MODEL_URL = "https://tfhub.dev/google/yamnet/1"
yamnet_model = hub.load(MODEL_URL)

# Загрузка карты классов
class_map_path = tf.keras.utils.get_file(
    'yamnet_class_map.csv',
    'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
)
class_map = np.loadtxt(class_map_path, delimiter=",", dtype="str", skiprows=1, usecols=(0, 1, 2))


# Функция для обработки MP3-файла
def preprocess_audio_from_mp3(file_path):
    """Загрузка и обработка MP3-файла."""
    audio, sample_rate = librosa.load(file_path, sr=16000, mono=True)  # Преобразование в моно, 16 кГц
    return audio, sample_rate


# Функция классификации аудио
def classify_audio(audio):
    """Классификация аудио с использованием модели YAMNet."""
    scores, embeddings, spectrogram = yamnet_model(audio)
    top_class_index = tf.argmax(scores, axis=1).numpy()[0]
    class_name = class_map[top_class_index][2]  # Название класса
    return class_name


# Основная функция
def test_fart_detect(mp3_file_path):
    # Предварительная обработка MP3-файла
    audio, sample_rate = preprocess_audio_from_mp3(mp3_file_path)

    # Классификация аудио
    detected_class = classify_audio(audio)

    # Проверка на класс "Fart"
    if "Fart" in detected_class:
        print("Fart sound detected!")
        return True
    else:
        print(f"Detected: {detected_class}")
