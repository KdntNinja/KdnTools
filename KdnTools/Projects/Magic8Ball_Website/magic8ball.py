from flask import Flask, render_template, request
from random import randint

app = Flask(__name__)


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
        return f"Question: {question}\n\nAnswer: {self.shake()}"

    @staticmethod
    def run_website(self):
        app.run(debug=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        question = request.form.get('question')
        magic8ball = Magic8Ball()
        answer = magic8ball.ask(question)
        return render_template('result.html', question=question, answer=answer)
    return render_template('home.html')