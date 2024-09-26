from flask import Flask
from src.api.routes.events import events_bp

app = Flask(__name__)
app.register_blueprint(events_bp)

@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)