from prompt_toolkit import PromptSession
from prompt_toolkit.validation import Validator, ValidationError
import requests
from info import IP, PORT


class UsernameValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message='Username cannot be empty!')
        
        if len(text) < 6:
            raise ValidationError(message='Username must be at least 6 characters long')


class PasswordValidator(Validator):
    def validate(self, document):
        text = document.text
        if len(text) < 6:
            raise ValidationError(message='Password must be at least 6 characters long')


class PasswordConfirmationValidator(Validator):
    def __init__(self, password):
        self.password = password

    def validate(self, document):
        text = document.text
        if text != self.password:
            raise ValidationError(message='Passwords do not match')


class GmailValidator(Validator):
    def validate(self, document):
        email = document.text
        if not email:
            raise ValidationError(message="Email cannot be empty")
        elif not email.endswith("@gmail.com"):
            raise ValidationError(message="Email must be a Gmail account.")


class AgeValidator(Validator):
    def validate(self, document):
        age = document.text
        if not age:
            raise ValidationError(message="Age cannot be empty")
        try:
            int(age)
        except ValueError:
            raise ValidationError(message="Age must be an integer")


class NonEmptyInputValidator(Validator):
    def validate(self, document):
        if not document.text.strip():
            raise ValidationError(message="Input cannot be empty")


def create_user():
    session = PromptSession()

    try:
        username = session.prompt("Username: ", validator=UsernameValidator())
        password = session.prompt("Password: ", validator=PasswordValidator(), is_password=True)
        confirm_password = session.prompt("Confirm Password: ", validator=PasswordConfirmationValidator(password), is_password=True)
        alias = session.prompt("Alias: ", validator=NonEmptyInputValidator())
        gmail = session.prompt("Gmail: ", validator=GmailValidator())
        openai_api_key = session.prompt("OpenAI API Key: ", validator=NonEmptyInputValidator())
        age = session.prompt("Age: ", validator=AgeValidator())

        # Send the user data to the server
        url = f'http://{IP}:{PORT}/signup'
        data = {
            'alias': alias,
            'username': username.lower(),  # Convert username to lowercase
            'password': password,
            'gmail': gmail,
            'openai_api_key': openai_api_key,
            'age': age
        }
        response = requests.post(url, json=data)
        response_data = response.json()

        if 'error' in response_data:
            print("Error:", response_data['error'])
        else:
            print("User created successfully:", response_data['message'])

    except KeyboardInterrupt:
        print("\nUser cancelled.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    print("Welcome to Y panel")
    create_user()
