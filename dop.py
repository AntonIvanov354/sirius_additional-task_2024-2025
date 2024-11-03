import requests
from moviepy.editor import VideoFileClip
import speech_recognition as sr

disk_url = 'https://cloud-api.yandex.net/v1/disk'  
access_token = 'ff65e2c4918f40cd8a67447822b6618f'  # токен доступа к Диску
video_files = []  # Список для хранения видео файлов

def get_video_files(folder_path): #Получаем список видео файлов из папки на Яндекс.Диске
    headers = {'Authorization': f'OAuth {access_token}'}
    params = {'path': folder_path}
    response = requests.get(f'{disk_url}/resources', headers=headers, params=params)

    if response.status_code == 200:
        items = response.json().get('items', [])
        for item in items:
            if item['name'].endswith(('.mp4', '.avi', '.mov')):  # Поддерживаемые форматы
                video_files.append(item['public_url'])
    else:
        print("Ошибка при получении файлов с Яндекс.Диска:", response.content)

def extract_audio_from_video(video_path, audio_path): # Извлекает аудио из видеофайла и сохраняет его.
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio(audio_path):# Преобразует аудио в текст с использованием Google Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language='ru-RU')
        except sr.RequestError as e:
            print("Ошибка API:", e)
            return None
        except sr.UnknownValueError:
            print("Не удалось распознать аудио")
            return None

def summarize_video(video_path):# функция для получения транскрипции видеофайла.
    audio_path = 'temp_audio.wav'
    extract_audio_from_video(video_path, audio_path)  # Извлекаем аудио
    transcription = transcribe_audio(audio_path)  # Транскрибируем аудио
    return transcription

# Пример использования функций
if __name__ == '__main__':
    folder_path = '/apids'  # Укажите путь к папке на Яндекс.Диске
    get_video_files(folder_path)
    
    for video_url in video_files:
        transcription = summarize_video(video_url)  # Получаем транскрипцию для каждого видео
        print(f"Транскрипция для {video_url}:\n{transcription}") 