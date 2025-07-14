from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask app is live! Use /run to execute logic."

@app.route("/run")
def run_script():
    subprocess.call(["python3", "your_script.py"])
    return "Script executed."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
