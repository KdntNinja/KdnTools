from flask import Flask, render_template, request


class Calculator:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/calculate", methods=["POST"])
        def calculate():
            number1 = float(request.form["number1"])
            number2 = float(request.form["number2"])
            operation = request.form["operation"]

            operations = {
                "add": ("+", lambda: number1 + number2),
                "subtract": ("-", lambda: number1 - number2),
                "multiply": ("*", lambda: number1 * number2),
                "divide": ("/", lambda: number1 / number2),
            }

            operation_symbol, result_func = operations.get(operation, ("", lambda: "Invalid operation"))
            result = result_func()

            return render_template("index.html", result=result, number1=number1, number2=number2,
                                   operation=operation_symbol)

    def run_website(self):
        self.app.run(debug=True)
