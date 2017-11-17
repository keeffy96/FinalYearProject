var score = 0;
  var total = 0;
  function submitAnswers() {
  total = 13;
  
  //Get user input
  var q1 = document.forms['quizForm']['q1'].value;
  var q2 = document.forms['quizForm']['q2'].value;
  var q3 = document.forms['quizForm']['q3'].value;
  var q4 = document.forms['quizForm']['q4'].value;
  var q5 = document.forms['quizForm']['q5'].value;
  var q6 = document.forms['quizForm']['q6'].value;
  var q7 = document.forms['quizForm']['q7'].value;
  var q8 = document.forms['quizForm']['q8'].value;
  var q9 = document.forms['quizForm']['q9'].value;
  var q10 = document.forms['quizForm']['q10'].value;
  var q11 = document.forms['quizForm']['q11'].value;
  var q12 = document.forms['quizForm']['q12'].value;
  var q13 = document.forms['quizForm']['q13'].value;

  
  // Validation  
  for(var i = 1; i <= total; i++) {
    if(eval('q' + i) === null || eval('q' + i) == '' ) {
      alert('You missed question ' + i);
      return false;
    }
  }
  
  // Set correct answers
  var a1 = "b";
  var a2 = "bdcae";
  var a3 = "6";
  var a4 = "C";
  var a5 = "4 8 3 + * 2";
  var a6 = "3";
  var a7 = "10:4";
  var a8 = "D";
  var a9 = "FLOOD";
  var a10 = "4";
  var a11 = "4";
  var a12 = "I";
  var a13 = "4";

  var answers = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13];
  
  for(var i = 1; i <= total; i++) {
    // Check answers
    if (eval('q' + i) == answers[i - 1]) {
      score++;
    }
  }
  
  return Math.round((score / 13) * 100);
}

function setValue() {
  $('input[name="grade"]').attr('value', submitAnswers());
}