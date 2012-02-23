$(document).ready(function(){  
	$("#btn-play").click(function(event) {  
		$.ajax({url: "/start"});  
		event.stopPropagation();
	});
	
	$("#btn-stop").click(function(event) {  
		$.ajax({url: "/stop"});  
		event.stopPropagation();
	});
	
	$(".pawn").draggable();
});
