'''
Created on 11.11.2021

@author: fasp
'''
from flask import jsonify
from flask import Flask
from flask import render_template
import json
from flask import Markup
import HtmlBuilder

app = Flask(__name__)
app.config["DEBUG"] = True
#app.config['JSON_AS_ASCII'] = False

ASSESSMENT_JSON = "templates/assessments.json"

@app.route('/getassessments', methods=['GET'])
def getassessments():
    return jsonify(getAssessmentJson(ASSESSMENT_JSON))

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/assessmentScript.js', methods=['GET'])
def assessmentscript():
    return render_template('assessmentScript.js', encoding="utf8")

@app.route('/assessment1.html', methods=['GET'])
def getAssessment():
    formHtml = HtmlBuilder.getFormHtml(getAssessmentJson(ASSESSMENT_JSON))
    return render_template("assessment1.html",
                           formhtml = Markup(formHtml)
                           )

@app.route('/<path:path>')
def static_file(path):
    return render_template(path)

def getAssessmentJson(file):
    f = open(file, encoding='utf-8')
    data = json.load(f)
    return data

app.run()
