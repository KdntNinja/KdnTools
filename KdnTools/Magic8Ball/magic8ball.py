from random import randint
from time import sleep
from tqdm import tqdm


class Magic8Ball:
    def __init__(self):
        self.answers = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]

    def shake(self):
        return self.answers[randint(0, len(self.answers) - 1)]

    def ask(self, question):
        return f"Question: {question}\nAnswer: {self.shake()}"

    @staticmethod
    def thinking():
        for _ in tqdm(range(100), desc="Thinking", ascii=False, ncols=75):
            sleep(0.01)

    def run(self):
        while True:
            question = input("What is your question? ")
            if question == "exit":
                break
            self.thinking()
            print("\n")
            print(self.ask(question))
            print("\n")
