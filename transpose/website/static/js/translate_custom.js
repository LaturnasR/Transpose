/* dropdown example picking */
$("li.phrases").click(function(e){
  $("#example").html($(this).attr("value"))
  $("#example").attr("value",$(this).attr("value"))
  $("#sentence").html($(this).attr("value"))
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

/* textarea autoresize */
  $("textarea").each(function () {
    this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
  })
  .on("input", function () {
    this.style.height = 0;
    this.style.height = (this.scrollHeight) + "px";
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
      "sum of","total of","addition of",
      "difference of",
      "multiplication of", "product of",
      "quotient of", "ratio of",
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