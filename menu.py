import customtkinter as ctk
from info import logo_path
from PIL import Image, ImageTk
from datetime import datetime
import openai
import threading
import pygame
import io
from voice_mode import run_voice_mode


class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Y - Artificial Intelligence")
        self.resizable(False, False)
        self.configure_window()
        self._set_appearance_mode("dark")
        self.wm_iconbitmap(logo_path)
        self.SendMessageEnabled = True
        self.username = ""
        self.age = 0
        self.openai_api_key = ""
        self.mode = "text"
        pygame.init()

    def UpdateInfo(self, username, age, openai_api_key):
        self.username = username
        self.age = age
        self.openai_api_key = openai_api_key    
        # Activate the OpenAI API
        openai.api_key = self.openai_api_key


    def configure_window(self):
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the geometry of the window to fullscreen
        self.geometry("{0}x{1}+0+0".format(screen_width, screen_height))
        threading.Thread(target=self.create_text_box).start()
        threading.Thread(target=self.buttons_change_mode).start()


    def create_text_box(self):
        # Create a custom font
        custom_font = ctk.CTkFont(family="Century Gothic", size=16, weight="bold")

        # Create the text box
        self.text_box = ctk.CTkTextbox(
            self,
            border_color="#818181",
            border_width=1.5,
            font=custom_font,
            fg_color="#242525",
            border_spacing=5,
            width=1200,
            height=10,  # Adjust height as needed
            wrap="char",  # Wrap text at word boundaries
            scrollbar_button_color="#000000",
        )
        self.text_box.pack(padx=90, pady=(0, 20), side="bottom", anchor="se")
        self.text_box.insert("1.0", "Message Y...")  # Insert placeholder text
        self.text_box.configure(text_color="#818181")  # Change text color to placeholder color
        self.text_box.bind("<FocusIn>", self.on_textbox_focus)
        self.text_box.bind("<Key>", self.on_key_pressed)
        self.text_box.bind("<Return>", self.on_enter_pressed)  # Bind Enter key event

        # Create the scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            scrollbar_button_color="black",  # Set the scrollbar color to black
            width=1180,  # Adjust width as needed
            height=1000,  # Adjust height as needed
            fg_color="transparent"  # Set background color to transparent
        )
        self.scroll_frame.pack(padx=(250,80), pady=(10, 10))
        self.put_message(f'Hi! I am Y, your personal AI assistant. How can I assist you today?', "Y - AI")



    def on_textbox_focus(self, event):
            # Check if textbox is empty
            if self.text_box.get("1.0", "end-1c") == "":
                self.text_box.insert("1.0", "Message Y...")  # Insert placeholder text
                self.text_box.configure(text_color="#818181")  # Change text color to placeholder color
    def on_key_pressed(self, event):
        # Check if the placeholder text is present when a key is pressed
        if self.text_box.get("1.0", "end-1c") == "Message Y...":
            self.text_box.delete("1.0", "end")  # Remove placeholder text
            self.text_box.configure(text_color="white")  # Change text color to white

        # Get the current text in the text box
        text = self.text_box.get("1.0", "end-1c")

        # Calculate the number of lines based on the number of characters
        num_chars = len(text)
        line_height = 25  # Adjust this value as needed
        max_char_per_line = 111  # Maximum characters per line
        # Manual switch statements to adjust the number of lines
        if num_chars <= max_char_per_line:
            num_lines = 1
        elif max_char_per_line < num_chars <= max_char_per_line*2:
            num_lines = 2
        elif max_char_per_line*2 < num_chars <= max_char_per_line*3:
            num_lines = 3
        elif max_char_per_line*3 < num_chars <= max_char_per_line*4:
            num_lines = 4
        else:
            num_lines = 5

        # Calculate the new height of the text box based on the number of lines
        max_height = 20  # Maximum number of lines
        new_height = min(num_lines, max_height) * line_height

        # Adjust the height of the text box
        self.text_box.configure(height=new_height)
    
    # Eneter pressed
    def on_enter_pressed(self, event):
        if self.SendMessageEnabled == True:
            self.SendMessageEnabled = False
            text = self.text_box.get("1.0", "end-1c")
            self.text_box.delete(0.0, "end")
            self.text_box.mark_set("insert", "1.0")
            self.text_box.configure(height=20) 
            threading.Thread(target=self.put_message, args=(text, self.username)).start()
            threading.Thread(target=self.openAIResponse, args=(text,)).start()
        
    def put_message(self, message, username):
        # Get the current time
        current_time = datetime.now().strftime("%H:%M:%S")

        # Format the message to display including username and timestamp
        message_text = f'{username} \t {current_time}\n'

        # Limit the length of each line of the message
        max_line_length = 60
        for i in range(0, len(message), max_line_length):
            message_text += message[i:i+max_line_length] + "\n"

        # Create the message label inside the scrollable frame's inner frame
        message_label = ctk.CTkLabel(
            self.scroll_frame,
            text=message_text,
            fg_color="transparent",
            font=ctk.CTkFont(family="Century Gothic", size=16),
            justify="left"
        )
        message_label.pack(pady=(0, 5), side="top", anchor="sw")
    
    def openAIResponse(self, message):
        if self.mode == "text":
            try:
                self.response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f'You are a AI tutor. Help the student to understand, dont solve problems for them. Your name is Y. The students age is {self.age}. and the students name is {self.username}'},
                    {"role": "user", "content": message}
                ])
                self.put_message(self.response.choices[0].message.content, "Y - AI")
                self.SendMessageEnabled = True
            except Exception as e:
                self.put_message("Sorry, Something went wrong.", "Y - AI")
                self.SendMessageEnabled = True
        elif self.mode == "image":
            try:
                self.image_response = openai.images.generate(
                    model="dall-e-3",
                    prompt=message,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )

                self.put_message(self.image_response.output.url, "Y - AI")
                self.SendMessageEnabled = True
            except Exception as e:
                self.put_message("Sorry, Something went wrong.", "Y - AI")
                self.SendMessageEnabled = True
        elif self.mode == "text_to_speech":
            try:
                self.response_speech = openai.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=message
                )

                # Play the generated audio
                pygame.mixer.music.load(io.BytesIO(self.audio.content))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                self.put_message("Playing audio...", "Y - AI")
                self.SendMessageEnabled = True
            except Exception as e:
                self.put_message("Sorry, Something went wrong.", "Y - AI")
                self.SendMessageEnabled = True
        elif self.mode == "voice":
            run_voice_mode(self.openai_api_key, self.age, self.username)
            self.destroy()
            self.SendMessageEnabled = True
        else:
            self.put_message("Sorry, Something went wrong.", "Y - AI")
            self.SendMessageEnabled = True

    # Modes
    def mode_btn_text_pressed(self):
        self.mode = "text"
        self.mode_btn_text._state = "disabled"
        self.mode_btn_image._state = "normal"
        self.mode_btn_tts._state = "normal"
        self.mode_bth_call._state = "normal"


        self.mode_btn_text.configure(fg_color="gray")
        self.mode_btn_image.configure(fg_color="black")
        self.mode_btn_tts.configure(fg_color="black")
        self.mode_bth_call.configure(fg_color="black")
    
    def mode_btn_image_pressed(self):
        self.mode = "image"
        self.mode_btn_text._state = "normal"
        self.mode_btn_image._state = "disabled"
        self.mode_btn_tts._state = "normal"
        self.mode_bth_call._state = "normal"


        self.mode_btn_text.configure(fg_color="black")
        self.mode_btn_image.configure(fg_color="gray")
        self.mode_btn_tts.configure(fg_color="black")
        self.mode_bth_call.configure(fg_color="black")

    def mode_btn_tts_pressed(self):
        self.mode = "text_to_speech"
        self.mode_btn_text._state = "normal"
        self.mode_btn_image._state = "normal"
        self.mode_btn_tts._state = "disabled"
        self.mode_bth_call._state = "normal"

        self.mode_btn_text.configure(fg_color="black")
        self.mode_btn_image.configure(fg_color="black")
        self.mode_btn_tts.configure(fg_color="gray")
        self.mode_bth_call.configure(fg_color="black")
    
    def mode_btn_call_pressed(self):
        self.mode = "voice"
        self.mode_btn_text._state = "normal"
        self.mode_btn_image._state = "normal"
        self.mode_btn_tts._state = "normal"
        self.mode_bth_call._state = "disabled"

        self.mode_btn_text.configure(fg_color="black")
        self.mode_btn_image.configure(fg_color="black")
        self.mode_btn_tts.configure(fg_color="black")
        self.mode_bth_call.configure(fg_color="gray")

    # Change mode button
    def buttons_change_mode(self):
        # Text Mode
        self.mode_btn_text = ctk.CTkButton(
            self,
            text="Text Mode",
            fg_color="black",
            border_color="gray",
            border_width=1,
            width=10,
            height=1,
            font=ctk.CTkFont(family="Century Gothic", size=12),
            command=self.mode_btn_text_pressed
        )
        self.mode_btn_text.pack(pady=(50, 0), padx=(60, 10), side="top", anchor="nw")

        # Image Mode Button
        self.mode_btn_image = ctk.CTkButton(
            self,
            text="Image Mode",
            fg_color="black",
            border_color="gray",
            border_width=1,
            width=10,
            height=1,
            font=ctk.CTkFont(family="Century Gothic", size=12),
            command=self.mode_btn_image_pressed
        )
        self.mode_btn_image.pack(padx=(60, 10), side="top", anchor="nw")
    
    
        # Text-To-Speech Mode Button
        self.mode_btn_tts = ctk.CTkButton(
            self,
            text="TTS Mode",
            fg_color="black",
            border_color="gray",
            border_width=1,
            width=10,
            height=1,
            font=ctk.CTkFont(family="Century Gothic", size=12),
            command=self.mode_btn_tts_pressed
        )
        self.mode_btn_tts.pack(padx=(60, 0), side="top", anchor="nw")

        # Voice-mode
        self.mode_bth_call = ctk.CTkButton(
            self,
            text="Call Mode",
            fg_color="black",
            border_color="gray",
            border_width=1,
            width=10,
            height=1,
            font=ctk.CTkFont(family="Century Gothic", size=12),
            command=self.mode_btn_call_pressed
        )
        self.mode_bth_call.pack(padx=(60, 0), side="top", anchor="nw")