import moviepy.editor as mp
import speech_recognition as sr
import os
import logging

# Constantes
VIDEO_PATH = "video/wok2.mp4"
SEGMENT_DURATION = 45
AUDIO_FOLDER = "segments_audio"
GLOBAL_TEXT_FILE = 'global_text.txt'

logging.basicConfig(level=logging.INFO)

def cut_video(video, total_duration):
    for i in range(0, int(total_duration), SEGMENT_DURATION):
        start_time = i
        end_time = min(i + SEGMENT_DURATION, total_duration)

        video_segment = video.subclip(start_time, end_time)
        audio_segment = video_segment.audio
        audio_file_path = os.path.join(AUDIO_FOLDER, f"segment_{i // SEGMENT_DURATION + 1}.wav")

        audio_segment.write_audiofile(audio_file_path, codec='pcm_s16le')

def analyze_audio(total_duration):
    text_video = ""
    
    for i in range(0, int(total_duration), SEGMENT_DURATION):
        audio_file_path = os.path.join(AUDIO_FOLDER, f"segment_{i // SEGMENT_DURATION + 1}.wav")

        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = sr.Recognizer().record(source)
            text = sr.Recognizer().recognize_google(audio_data, language="fr-FR")
            logging.info(f"\nRésultat pour le segment {i // SEGMENT_DURATION + 1} :\n{text}")
            text_video = f"{text_video}\n{text}\n"
        except sr.UnknownValueError:
            logging.info(f"\nAucune parole détectée dans le segment {i // SEGMENT_DURATION + 1}.")
        except sr.RequestError as e:
            logging.error(f"\nErreur lors de la demande de reconnaissance vocale : {e}")
        finally:
            try:
                os.remove(audio_file_path)
            except FileNotFoundError:
                pass
            except Exception as e:
                logging.error(f"Erreur lors de la suppression du fichier : {e}")
    
    return text_video

def create_global_text_file(text):
    if not os.path.exists(GLOBAL_TEXT_FILE):
        logging.info("Le fichier n'existe pas. Création du fichier...")
        with open(GLOBAL_TEXT_FILE, 'w') as fichier:
            fichier.write(text)
        logging.info(f"Le fichier {GLOBAL_TEXT_FILE} a été créé avec succès.")
    else:
        logging.info(f"Le fichier {GLOBAL_TEXT_FILE} existe déjà.")

if __name__ == "__main__":
    with mp.VideoFileClip(VIDEO_PATH) as video:
        total_duration = video.duration
        os.makedirs(AUDIO_FOLDER, exist_ok=True)

        logging.info(f"\nDécoupage de la vidéo en segments audio de {SEGMENT_DURATION} secondes...")
        cut_video(video, total_duration)

        logging.info("\nAnalyse des segments audio...\n")
        text_video = analyze_audio(total_duration)

    create_global_text_file(text_video)
    logging.info("\nFin du programme.")