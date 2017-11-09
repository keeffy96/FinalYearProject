$(document).ready(function() {
  answers = new Object();

  $('.option').change(function() {
    var answer = ($(this).attr('value'))
    var question = ($(this).attr('name'))
    answers[question] = answer
  })
  
  var item1 = document.getElementById('questions');

  var totalQuestions = $('.questions').size();
  var currentQuestion = 0;
  $questions = $('.questions');
  $questions.hide();
  $($questions.get(currentQuestion)).fadeIn();

  $('#next').click(function(){
    alert("Hello");
    $($questions.get(currentQuestion)).fadeOut(function(){
      currentQuestion = currentQuestion + 1;
      if(currentQuestion == totalQuestions){
        //do stuff with the result
        alert("Hello  ");
      } else {
        $($questions.get(currentQuestion)).fadeIn();
          console.log("Hello");
      }
    });
  });
});

function getAnswers() {
  var studentAnswer1 = document.getElementByName('answer1').value;
  var studentAnswer2 = document.getElementByName('answer2').value;
  var studentAnswer3 = document.getElementByName('answer3').value;
  var studentAnswer4 = document.getElementByName('answer4').value;
  var studentAnswer5 = document.getElementByName('answer5').value;

  var arraySA = [studentAnswer1, studentAnswer2, studentAnswer3, studentAnswer4, studentAnswer5];
}

function Answers() {
  var answer1 = 'B';
  var answer2 = 'B,D,C,A,E';
  var answer3 = '6';
  var answer4 = 'C';
  var answer5 = '4 8 3 + * 2 -';

  var arrayAnswers = [answer1, answer2, answer3, answer4, answer5];
}

function Compare() {
  var result=0;
  var studentAns = getAnswers();
  var actualAns = Answers();

  for(var i=0;i < studentAns.size;i++){
    if(studentAns[i]==actualAns[i]) result++;
  }
  return result;
}

function sum_values(){
  var the_sum = 0;
  for (questions in answers) {
    the_sum = the_sum + parseInt(answers[question])
  }
  return the_sum
}

function result() {
  var score = 0;
  score += parseInt() || 0;
  score += parseInt() || 0;

  alert("You scored: " + score + "out of 2");
}



/*
Answer 1 - B
Answer 2 - B D C A E
Answer 3 - 6
Answer 4 - C 
Answer 5 - 4 8 3 + * 2 - | 4 3 8 + * 2 - | 8 3 + 4 * 2 - | 3 8 + 4 * 2 -
Answer 6 - Image with 3 3 3 (Maybe add images as radios)
Answer 7 - 10:4
Answer 8 - Image D (Maybe add images as radios)
Answer 9 - Flood (Maybe radio button)
Answer 10 - 4
Answer 11 - 4 (Maybe radio buttons)
Answer 12 - Plate I (Maybe radio buttons)
Answer 13 - 4
An
*/