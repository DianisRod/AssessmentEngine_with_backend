var currentTab = 0; // Current tab is set to be the first tab (0)

var questions;

var pathname = window.location.pathname;
var API = "http://127.0.0.1:5000/getAssessmentFromWeb";
$.post(API, {src:pathname}, function(response){ 
    questions = response;
});

function main() {
	showTab(currentTab); // Display the current tab
}

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  //if (n == 0) {
  //  document.getElementById("prevBtn").style.display = "none";
  //} else {
  //  document.getElementById("prevBtn").style.display = "inline";
  //}
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "absenden";
  } else {
    document.getElementById("nextBtn").innerHTML = "weiter";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
	let formData = document.getElementById("regForm")
	
	// Es gibt noch kein backend:
    //document.getElementById("regForm").submit();
	// stattdessen Daten lokal weiterreichen:
	showResults(formData);
	
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function showResults(form){
	var contentContainer = document.getElementById('content');
	
	let myForm = document.getElementById('regForm');
	let formData = new FormData(myForm);
	
	const formDataJson = {}
	formData.forEach((value, key) => (formDataJson[key] = formData.getAll(key)))
	
	var solutions = 'Ihre Lösungen werden uebermittelt:<br>'
	var table = '<table class="center">'
	for (var i = 0; i < Object.keys(formDataJson).length; i++) {
		var row ='<tr>';
		var currQuestion =questions.Fragen[i]
		var currAnswers = Object.values(formDataJson)[i]
		row+='<td>'+currQuestion.Fragetext+'</td>';
		columns = formDataJson[i];
		for (var colIndex = 0; colIndex < currAnswers.length; colIndex++) {
			var answer = currAnswers[colIndex];
			if(currQuestion.Typ != 'freifeld'){
				const answers=currQuestion.Antworten
				answer = answers[answer].val
			} else{	
				if (answer == null) answer = "";
			}
			row+='<td>'+answer+'</td>';
		}
		row+='</tr>'
    table+=row
	}
	table+='</table>'
	solutions += table;
	
	var output = [];
	output.push('<div id="regForm"">');
	output.push('<h1>Vielen Dank fuer Ihre Teilnahme!</h1>');
	output.push(solutions);
	output.push('<a href="index.html">Zurueck zur Startseite</a>');
	output.push('</div>');
	
	contentContainer.innerHTML = output.join('');
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}