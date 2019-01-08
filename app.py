from flask import Flask, flash, redirect, render_template, request, session, abort
import datetime, time
import json
import subprocess
import threading
import threading
from unidecode import unidecode
import os
from IPython import embed
from text_diff import diff, parse, filter_sentences
import platform

languages = [ 'es','de','la','fr']
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
    base = "Below is one way to think about how a recurrent network operates: at each time step, it combines input from the present moment, as well as input from the memory layer, to make a decision about the data."
    para = back_translate(base, 'longer')

    embed()
    




def escape(text):
    text = text.replace("\"", "\\\"")
    text = text.replace("'", "\\'")
    return text

def extract(httpcurl, dictionary, lang, to_escape = True):
    before = time.clock()
    raw_response = subprocess.check_output(httpcurl, shell=True)
    after = time.clock()
    print(after - before)
    print(raw_response)
    decoded = raw_response.decode('utf-8')
    decoded = unidecode(decoded)
    decoded = decoded.strip()
    if(decoded[:2] == 'C:'):
        decoded = ('\n').join(decoded.split('\n')[1:])
    print(decoded)

    translation = json.loads(decoded)['data']['translations'][0]['translatedText']
    if(to_escape):
        dictionary[lang] = escape(translation)
    else:
        dictionary[lang] = translation

    print("{} done".format(lang))


def back_translate(text, sign):
    escaped_text = escape(text)
    candidates = {}
    intermediates = {}
    mythreads = []
    for language in languages:
        
        forward = curl.replace("SOURCE", "en").replace("TARGET", language).replace("QUERY", escaped_text)
        t = threading.Thread(target = extract, args = (forward, intermediates, language, True))
        t.start()
        mythreads.append(t)

    while any(t.isAlive() for t in mythreads):
        pass
    
    mythreads = []

    for language in intermediates.keys():
        backward = curl.replace("SOURCE", language).replace("TARGET", "en").replace("QUERY", intermediates[language])
        t = threading.Thread(target = extract, args = (backward, candidates, language, False))
        t.start()
        mythreads.append(t)
    
    while any(t.isAlive() for t in mythreads):
        pass
    
    current = text
    for language in candidates.keys():
        current = filter_sentences(current,candidates[language])[sign]
        


    tracked = diff(parse(text), parse(current))[0]
    print(tracked)
    return {"paraphrased":current, "tracked":tracked}


#test()


@app.route("/")
def index():
	return render_template('index.html')
 
@app.route("/paraphrase")
def paraphrase():
    text = request.values.get('text')
    sign = request.values.get('sign')
    translated = back_translate(text, sign)
    para = translated["paraphrased"]
    tracked = translated["tracked"]
    return render_template('index.html',text = text, modified = para, tracked = tracked)

if __name__ == "__main__":
    app.run(host = 'localhost', port = 4000)
