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
    $($questions.get(currentQuestion)).fadeOut(function(){
      currentQuestion = currentQuestion + 1;
      if(currentQuestion == totalQuestions){
        var result = sum_values()

        //do stuff with the result
        alert(result);
      } else {
        $($questions.get(currentQuestion)).fadeIn();
      }
    });
  });
});


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

function getSelectedRadioValue(name) {
  var radios = document.getElementByName(name);
}