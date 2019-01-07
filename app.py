from flask import Flask, flash, redirect, render_template, request, session, abort
import os
app = Flask(__name__)
 
@app.route("/")
def index():
	return render_template('index.html')
 
@app.route("/translate")
def translate():
	text = request.values.get('text')
	return render_template('index.html',text = text, modified = text )




if __name__ == "__main__":
	app.run(host = 'localhost', port = 80)