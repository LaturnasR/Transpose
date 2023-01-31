$(document).on('submit','#sentence_form',function(e){
	e.preventDefault();
	$.ajax({
	  type:'POST',
	  url: $SCRIPT_ROOT + '/_submit_sentence',
	  data:{
	    sentence:$("#sentence").val()
	  },
	  success:function(response){
	    $("#output").html(response)
	  }
	})
});
