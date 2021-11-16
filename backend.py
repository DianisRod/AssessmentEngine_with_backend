'''
Created on 11.11.2021

@author: fasp
'''
import json
import HtmlBuilder
import re
from os import listdir
from os.path import isfile, join
from flask import request
from flask import jsonify
from flask import render_template
from flask import Markup
from flask import Flask, session
from flask_session import Session
app = Flask(__name__)
app.config["DEBUG"] = True
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

ASSESSMENT_FOLDER = "assessments/"
ASSESSMENT_JSON = "assessments/assessments.json"

@app.route('/', methods=['GET'])
def index():    
    assessments=dict((f[:-5], ASSESSMENT_FOLDER+f ) for f in listdir("assessments") if isfile(join("assessments", f)) and f.endswith('.json'))
    session["assessments"]=assessments
    assessments_html = ''.join([''+join('<a href="'+k+'">'+k+'</a><br>\n') for k,v in assessments.items()])
    return render_template("index.html",
                           assessments_html = Markup(assessments_html)
                           )

@app.route('/assessmentScript.js', methods=['GET'])
def assessmentscript():
    return render_template('assessmentScript.js', encoding="utf8")
 
@app.route('/<path:path>')
def static_file(path):
    if re.match("assessment\d+", path):
        return getAssessmentHtml(path)
    else:
        return render_template(path)

@app.route('/getAssessmentFromWeb',methods = ['POST'])
def getAssessmentFromWeb():
    assessments=session["assessments"]
    assessment = request.form['src']
    if assessment.startswith("/"):
        assessment=assessment[1:]
    assessment_json=assessments[assessment]
    return getAssessmentJson(assessment_json)

def getAssessmentHtml(path):
    assessments=session["assessments"]
    assessment_json=assessments[path]
    formHtml = HtmlBuilder.getFormHtml(getAssessmentJson(assessment_json))
    return render_template("assessment.html",
                        formhtml = Markup(formHtml))

def getAssessmentJson(file):
    f = open(file, encoding='utf-8')
    data = json.load(f)
    return data

app.run()
