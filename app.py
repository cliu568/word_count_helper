from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import subprocess
import os
from IPython import embed

import platform
from text_diff import parse, diff

app = Flask(__name__)

if(platform.system() =='Windows'):
    with open("CURL_windows.txt") as f:
        curl = f.readline()

else:
    with open("CURL.txt") as f:
        curl = f.readline()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Translation-a3cfdf2016a1.json"


def test():
    print(curl)
    base = "Fujisaki Station is a station on the Gonō line, 144.7 km from the terminus of the Higashi-Noshiro Line."
    para = back_translate(base)

    embed()
    



def extract(httpcurl):
    raw_response = subprocess.check_output(httpcurl, shell=True)
    
    translation = json.loads(raw_response.decode('utf-8'))['data']['translations'][0]['translatedText']
    return translation

def back_translate(text, mid='fr'):
    forward = curl.replace("SOURCE", "en").replace("TARGET", mid).replace("QUERY", text)
    translation = extract(forward)
    
    print(translation)
    backward = curl.replace("SOURCE", mid).replace("TARGET", "en").replace("QUERY", translation)
    embed()
    paraphrased = extract(backward)
    print(paraphrased)
    changes = diff(parse(text),parse(paraphrased))[0]

    return {"paraphrased":paraphrased, "changes":changes}




@app.route("/")
def index():
	return render_template('index.html')
 
@app.route("/paraphrase")
def paraphrase():
    text = request.values.get('text')
    modified = back_translate(text)
    para = modified["paraphrased"]
    changes = modified["changes"]
    return render_template('index.html',text = text, modified = para, changes = changes)

if __name__ == "__main__":
    app.run(host = 'localhost', port = 4000)
