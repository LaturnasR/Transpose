$(document).on('submit','#sentence_form',function(e){
	$("#output").html("loading....");

	e.preventDefault();
	$.ajax({
		url: $SCRIPT_ROOT + '/_submit_sentence',
		type:'POST',
		data:{
			sentence:$("#sentence").val()
		}
	})
	.done(function(response){
		$("#output").html(response);
	})
	.fail(function(){
		$("#output").html("<h6 class='text-danger'>Browser failed to execute the server script</h6>");
	});
});
