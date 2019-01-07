from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import subprocess
import os
from IPython import embed
from text_diff import diff, parse
import platform


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
    base = "After configuration is complete, take note of the client ID that was created. You will need the client's \"ID\" to complete the next steps."
    para = back_translate(base)

    embed()
    


def extract(httpcurl):
    raw_response = subprocess.check_output(httpcurl, shell=True)
    
    translation = json.loads(raw_response.decode('utf-8'))['data']['translations'][0]['translatedText']
    return translation

def escape(text):
    text = text.replace("\"", "\\\"")
    text = text.replace("'", "\\'")
    return text

def back_translate(text, mid='fr'):
    text = escape(text)
    forward = curl.replace("SOURCE", "en").replace("TARGET", mid).replace("QUERY", text)
    translation = escape(extract(forward))
    

    backward = curl.replace("SOURCE", mid).replace("TARGET", "en").replace("QUERY", translation)
    
    paraphrased = extract(backward)


    tracked = diff(parse(text), parse(paraphrased))[0]
    print(tracked)
    return {"paraphrased":paraphrased, "tracked":tracked}


#test()


@app.route("/")
def index():
	return render_template('index.html')
 
@app.route("/paraphrase")
def paraphrase():
    text = request.values.get('text')
    para = back_translate(text)["paraphrased"]
    tracked = back_translate(text)["tracked"]
    return render_template('index.html',text = text, modified = para, tracked = tracked)

if __name__ == "__main__":
    app.run(host = 'localhost', port = 4000)
