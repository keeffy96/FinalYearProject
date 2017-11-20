var score = 0;
var total = 0;
function submitAnswersBebras2() {
  total = 13;

  var q1 = document.forms['bebras2Form']['q1'].value;
  var q2 = document.forms['bebras2Form']['q2'].value;
  var q3 = document.forms['bebras2Form']['q3'].value;
  var q4 = document.forms['bebras2Form']['q4'].value;
  var q5 = document.forms['bebras2Form']['q5'].value;
  var q6 = document.forms['bebras2Form']['q6'].value;
  var q7 = document.forms['bebras2Form']['q7'].value;
  var q8 = document.forms['bebras2Form']['q8'].value;
  var q9 = document.forms['bebras2Form']['q9'].value;
  var q10 = document.forms['bebras2Form']['q10'].value;
  var q11 = document.forms['bebras2Form']['q11'].value;
  var q12 = document.forms['bebras2Form']['q12'].value;
  var q13 = document.forms['bebras2Form']['q13'].value;

  
  // Validation  
  for(var i = 1; i <= total; i++) {
    if(eval('q' + i) === null || eval('q' + i) == '' ) {
      alert('You missed question ' + i);
      return false;
    }
  }
  
  // Set correct answers
  var a1 = "b";
  var a2 = "EDCBA";
  var a3 = "NotSure";
  var a4 = "3";
  var a5 = "D";
  var a6 = "N,E,E,S,E";
  var a7 = "OKIWILLBETHERE!";
  var a8 = "b";
  var a9 = "D";
  var a10 = "5.1";
  var a11 = "UOOOIP";
  var a12 = "NotSure";
  var a13 = "D";

  var answers = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13];
  
  for(var i = 1; i <= total; i++) {
    // Check answers
    if (eval('q' + i) == answers[i - 1]) {
      score++;
    }
  }
  
  return Math.round((score / 13) * 100);
}

function setValueBebras2() {
  $('input[name="grade"]').attr('value', submitAnswersBebras2());
}