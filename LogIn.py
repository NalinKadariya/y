import tkinter
import customtkinter
from PIL import ImageTk, Image
import requests
from info import IP, PORT, logo_path
from menu import Menu

#from menu import create_menu_window

def create_login_window():
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # creating custom tkinter window
    app.title('Login - Y')
    app.resizable(False, False)  # Disable resizing

    # Get screen dimensions
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Center the window
    window_width = 600
    window_height = 440
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))


    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

    def button_function():
        # Get the entered username and password
        username = entry1.get()
        password = entry2.get()
        
        # Send login request to server
        response = login_to_server(username.lower(), password)
        username = response.get('alias')
        age = response.get('age')
        openai_key = response.get('openai_api_key')

        # Check response for success
        if 'message' in response:
            # Show success message
            message_label.configure(text=response['message'], text_color=("green", "green"))
            app.destroy()
            app_ = Menu()
            app_.UpdateInfo(username, age, openai_key)
            app_.mainloop()

        else:
            # Show failure message
            message_label.configure(text=response['error'], text_color=("red", "red"))

    def login_to_server(username, password):
        url = f'http://{IP}:{PORT}/login'
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)
        return response.json()

    bg_image = Image.open("Images/Bg_Frame.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    l1 = customtkinter.CTkLabel(master=app, image=bg_image)
    l1.pack()

    # creating custom frame
    frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic',20))
    l2.place(x=50, y=45)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=110)

    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry2.place(x=50, y=165)

    # Create custom button - Login
    button_login = customtkinter.CTkButton(master=frame, width=220, text="Login", command=button_function, corner_radius=6)
    button_login.place(x=50, y=240)

    # Message label
    message_label = customtkinter.CTkLabel(master=frame, text="", text_color=("black", "black"))
    message_label.place(x=50, y=290)

    app.wm_iconbitmap(logo_path)
    app.mainloop()

create_login_window()