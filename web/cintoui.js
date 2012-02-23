$(document).ready(function(){  
	$("#btn-play").click(function(event) {  
		$.ajax({url: "/start"});  
		event.stopPropagation();
	});
	
	$("#btn-stop").click(function(event) {  
		$.ajax({url: "/stop"});  
		event.stopPropagation();
	});
	
	function updatePawn(name, position) {
		var pawnId = name.replace(/[^\d]/g, '');
		var left = position.left / $('.playground-board').width();
		var top = position.top / $('.playground-board').height();
		$.ajax({
			type: "POST",
			url: "/pawn/" + pawnId, 
			data: {
				x: left,
				y: top
			}
		});  
	}
	
	$(".pawn").draggable({
		containment: 'parent',
		drag: function(event, ui) {
			updatePawn(this.className, ui.position)
		},
		stop: function(event, ui) {
			updatePawn(this.className, ui.position)
		}
	});
});
