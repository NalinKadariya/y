import tkinter
import customtkinter as ctk
from PIL import Image
import openai
import whisper
import pyaudio
import threading
import wave
import pygame
from pydub import AudioSegment
import io
from info import *

class VoiceAssistantApp:
    def __init__(self, root, key, age, username):
        self.root = root
        self.key = key
        self.recording = False
        self.frames = []
        self.start_recording_button = None
        self.stop_recording_button = None
        self.init_ui()
        self.age = age
        self.username = username

    def init_ui(self):
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.title("Y - Voice Mode")
        self.root.wm_iconbitmap(logo_path)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("dark-blue")
        self.main_menu()

    def generate_response(self, text_):
        try:
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f'You are a AI tutor. Help the student to understand, dont solve problems for them. Your name is Y. The students age is {self.age} years old. The students name is {self.username}.'},
                    {"role": "user", "content": text_}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error during response generation: {e}")
            return "Invalid API key."

    def update_gui_during_recording(self):
        while self.recording:
            self.root.update()

    def start_recording(self):
        print("Recording started")
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.frames = []
        self.recording = True
        gui_update_thread = threading.Thread(target=self.update_gui_during_recording)
        gui_update_thread.start()
        self.start_recording_button.configure(state="disabled")
        self.stop_recording_button.configure(state="normal")
        while self.recording:
            data = stream.read(1024)
            self.frames.append(data)
            self.root.update()
        gui_update_thread.join()

    def text_to_speech(self, text):
        try:
            response = openai.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            audio_data = AudioSegment.from_file(io.BytesIO(response.content))
            pygame.mixer.music.load(io.BytesIO(response.content))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error during text-to-speech: {e}")

    def stop_recording(self):
        if self.recording:
            try:
                self.recording = False
                pyaudio.PyAudio().terminate()
                self.stop_recording_button.configure(state="disabled")
                wf = wave.open("recorded_audio.wav", 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                wf.setframerate(44100)
                wf.writeframes(b''.join(self.frames))
                wf.close()
                model = whisper.load_model("base")
                print("Transcribing the audio...")
                result = model.transcribe("recorded_audio.wav")
                transcription_text = result["text"]
                print(f"Transcription: {transcription_text}")
                self.frames = []
                answer = self.generate_response(transcription_text)
                if answer == "Invalid API key.":
                    self.error_screen("Invalid API key.", 0.5, 0.8, "red")
                else:
                    self.text_to_speech(answer)
                self.start_recording_button.configure(state="normal")
            except Exception as e:
                print(f"Error during recording termination: {e}")

    def main_menu(self):
        openai.api_key = self.key
        self.start_recording_button = ctk.CTkButton(master=self.root, width=50, height=30, border_width=0, corner_radius=8,
                                                     text="Start Recording", font=ctk.CTkFont(family='Cambria', size=20, weight='bold', underline=0, overstrike=0),
                                                     anchor='center', command=self.start_recording)
        self.start_recording_button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.stop_recording_button = ctk.CTkButton(master=self.root, width=50, height=30, border_width=0, corner_radius=8,
                                                    text="Stop Recording", font=ctk.CTkFont(family='Cambria', size=20, weight='bold', underline=0, overstrike=0),
                                                    anchor='center', command=self.stop_recording)
        self.stop_recording_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.stop_recording_button.configure(state="disabled")

    def error_screen(self, error_message, x, y, color):
        error_label = ctk.CTkLabel(self.root, text=error_message, font=ctk.CTkFont(family='Cambria', size=20, weight='bold'), fg_color=color)
        error_label.place(relx=x, rely=y, anchor=tkinter.CENTER)


def run_voice_mode(key, age, username):
    root = ctk.CTk()
    app = VoiceAssistantApp(root, key, age, username)
    root.mainloop()