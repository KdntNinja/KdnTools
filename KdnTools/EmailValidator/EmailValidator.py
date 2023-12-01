import re


class EmailValidator:
    def __init__(self):
        self.email = self.run

    @staticmethod
    def run():
        email = input("Enter your email address: ")
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email):
            print("Email is valid")
            return email
        else:
            print("Email is invalid")
            return None


if __name__ == "__main__":
    validator = EmailValidator()
    validator.run()
