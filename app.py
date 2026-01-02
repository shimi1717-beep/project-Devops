from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def hello():
    return "Hello, World! Phase3 is online.", 200

@app.get("/healthz")
def health():
    return jsonify(status="ok"), 200


@app.get("/version")
def version():
    return jsonify(version="1.0.0", author="shimi"), 200

if __name__ == "__main__":
    # Bind to 0.0.0.0 so it works inside Docker
    app.run(host="0.0.0.0", port=80)
