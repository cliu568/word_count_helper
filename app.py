from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import subprocess
import os
from IPython import embed

app = Flask(__name__)

with open("CURL.txt") as f:
    curl = f.readline()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Translation-a3cfdf2016a1.json"

def extract(httpcurl):
    raw_response = subprocess.check_output(httpcurl, shell=True)
    translation = json.loads(raw_response)['data']['translations'][0]['translatedText']
    return translation

def back_translate(text, mid='fr'):
    forward = curl.replace("SOURCE", "en").replace("TARGET", mid).replace("QUERY", text)
    translation = extract(forward)
    backward = curl.replace("SOURCE", mid).replace("TARGET", "en").replace("QUERY", translation)
    paraphrased = extract(backward)
    return paraphrased

def test():
    base = "Fujisaki Station is a station on the Gonō line, 144.7 km from the terminus of the Higashi-Noshiro Line."
    para = back_translate(base)
    embed()
    
@app.route("/")
def index():
	return render_template('index.html')
 
@app.route("/paraphrase")
def paraphrase():
    text = request.values.get('text')
    para = back_translate(text)
    return render_template('index.html',text = text, modified = para)

if __name__ == "__main__":
    app.run(host = 'localhost', port = 4000)
