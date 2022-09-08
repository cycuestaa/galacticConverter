from flask import render_template, request
from main import app


@app.route('/basic-template')
def main():
    return render_template('basic-template.html')

@app.route('/')
@app.route('/instructions')
def firstPage():
    return render_template('part-one.html')

@app.route('/tool')
def secondPage():
    return render_template('part-two.html')

