from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {
            'name': 'Adamnite',
            'version': '0.1.0'
        }
    )


# Main Entry Point
if __name__ == '__main__':
    app.run()
