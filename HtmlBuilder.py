'''
Created on 15.11.2021

@author: fasp
'''

def getFormHtml(assessmenJson):
    title=assessmenJson["name"]
    fragen=assessmenJson["Fragen"]
    formhtml='<form id="regForm" >\n'
    formhtml+='    <h1>'+title+':</h1>\n'
    for fi in range(len(fragen)):
        f=fragen[fi]
        formhtml+='    <div class="tab">'+f["Fragetext"]+'\n'
        if f["Typ"] == "freifeld":
            formhtml+='        <p><input placeholder="Antwort..." oninput="this.className = ''" name="frage'+str(fi)+'" maxlength="20"></p>\n'
        elif f["Typ"] =="singlechoice":
            antworten=f["Antworten"]
            for i in range(len(antworten)):
                antwort=antworten[i]["val"]
                formhtml+="      <div>\n"
                formhtml+='         <input type="radio" id="'+antwort.lower()+' " name="frage'+str(fi)+'" value='+str(i)
                if i==0:
                    formhtml+=' checked'
                formhtml+=' >\n'
                formhtml+='        <label for="'+antwort.lower()+'">'+antwort+'</label>\n'
                formhtml+="      </div>\n"
        elif f["Typ"] == "Multichoice":
            antworten=f["Antworten"]
            for i in range(len(antworten)):
                antwort=antworten[i]["val"]
                formhtml+='      <input type="checkbox" id='+antwort.lower()+' name="frage'+str(fi)+'" value="'+str(i)+'"/>'+antwort+'<br>\n'
        formhtml+="    </div>\n"
    formhtml+="""
    <div style="overflow:auto;">
      <div style="float:right;">
        <button type="button" id="nextBtn" onclick="nextPrev(1)">weiter</button>
      </div>
    </div>
    <!-- Circles which indicates the steps of the form: -->
    <div style="text-align:center;margin-top:40px;">
    """
    for f in fragen:
        formhtml+='    <span class="step"></span>\n'
    formhtml+= '  </div>\n</form>'
    
    return formhtml
