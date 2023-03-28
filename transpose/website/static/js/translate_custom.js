/* checks if user has entered the code already */
$(document).ready(function(){

  if(Cookies.get('passed')){
    $("#codeInput").attr("data-bs-content", "You don't need to input the code again in this session!")
    $("#codeInput").attr("data-bs-title", "Code already entered")
    $("#codeInput").attr("placeholder", "Just click 'OK!', we're good!")
    $("#codeInput").prop("readonly", true)
  }
})
/* instructions modal popover */
//enables popover on keycode input
$(document).ready(function(){
  $('[data-bs-toggle="popover"]').popover();
});

/* modals */
// instruction modal
$(document).ready(function () {
  $("#instructions").modal('show');
});
$("#instructions_btn").on('click', function(){
  $("#instructions").modal('show');
})

// table modal
$("#table_btn").on('click', function(){
  $("#table").modal('show');
})

/* fixed bottom button dropdown */
$(document).ready(function(){
  $('[data-bs-second-toggle="popover"]').popover();
});
$("#dropdown_bottom a").on('click', function(){
  $("#dropdown_bottom_btn").dropdown('toggle');
})

/* animations */
// #instructions on close animation
$("#instructions_close").on('click', function(){
  //if codeInput is invalid
  if($("#codeInput").val() != "ITJMDBRL" && Cookies.get('passed') != "true"){
    animateCSS('#codeInput', 'headShake');
    $("#codeInput").css('border', '2px solid red');
    Cookies.set('passed', true);
  }
  
  else{
    $("#codeInput").prop('disabled', true);
    $("#codeInput").css('border', '2px solid green');
    $("#instructions").modal('hide');

    //animation on modal close
    $("#dropdown_bottom_btn").addClass("border border-4 border-danger bigger animate__slow")
    animateCSS('#dropdown_bottom_btn', 'headShake').then(function(){
      $("#dropdown_bottom_btn").removeClass("border border-3 border-danger bigger animate__slow")
    })
  }
});

/* dropdown example picking */
$("li.phrases").click(function(e){
  $("#example").attr("value",$(this).attr("value"))
  console.log($(this).attr("value"))
  $("#sentence").html($(this).attr("value"))
  $("#sentence").val($(this).attr("value"))
})

/* form submit */
$(document).on('submit','#sentence_form',function(e){
  $("#output").css("background", "white");
  $("#output").html("loading....");

  e.preventDefault();
  $.ajax({
    url: '/_submit_sentence',
    type:'POST',
    data:{
      sentence:$("#sentence").val()
    }
  })
  .done(function(response){
    $("#output").html(response);
      MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
  })
  .fail(function(){
    $("#output").html("<h6 class='text-danger'>Browser failed to execute the server script</h6>");
  });
});


/* textarea submit on enter */
$(document).ready(function() {
  $('textarea').keypress(function(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        $("#sentence_form").submit();
    }
  });
});
/* textcomplete custom js */
$('textarea').textcomplete([{
  match: /(^|\b)(\w{2,})$/,
  search: function (term, callback) {
    var words = [
      'less than', 'fewer than',
      'more than', 'greater than', 
      'is less than', 'is fewer than',
      "is less than or equal to", "is at least",
      "is greater than or equal to", "is at most",
      "is equals to","equal", "yields",
      "is not equal to",
      "plus", "add", "increase", "exceed", "more",
      "take away", "subtract", "minus", "decrease", "less", "diminish", "reduce", "lost",
      "times", "multiplied by", 
      "divide", "divided by",
      "sum of","total of",
      "difference of",
      "product of",
      "quotient of", "ratio of", 
      "the sum of","the total of",
      "the difference of",
      "the product of",
      "the quotient of", "the ratio of",
      "the square root of", 
      "square root of", "twice of", "thrice of"
      ];

    term = term.toLowerCase();
    callback($.map(words, function (word) {
      temp_word = word.toLowerCase().indexOf(term);
      return temp_word === 0 ? word : null;
    }));
  },
  replace: function (word) {
      return word + ' ';
  }
}]);