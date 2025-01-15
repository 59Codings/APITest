from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "api on"

if __name__ == "__main__":
    app.run(debug=True)
