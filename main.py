from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "App is live"

@app.route("/run")
def run():
    subprocess.call(["python3", "newPyFile.py"])
    return "Notebook executed"
