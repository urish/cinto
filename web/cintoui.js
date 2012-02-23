$(document).ready(function(){
	var fieldSize = {
		width: $('.playground-board').width() - $('.pawn-1').width(),
		height: $('.playground-board').height() - $('.pawn-1').height(),
	};
	
	$("#btn-play").click(function(event) {  
		$.ajax({url: "/start"});  
		$.getJSON("/pawns", function(data) {
			data.pawns.map(function(pawn) {
				$(".pawn-" + pawn.id).css("left", pawn.x * fieldSize.width)
					.css("top", pawn.y * fieldSize.height);
			});
		});
		event.stopPropagation();
	});
	
	$("#btn-stop").click(function(event) {  
		$.ajax({url: "/stop"});  
		event.stopPropagation();
	});
	
	function updatePawn(name, position) {
		var pawnId = name.replace(/[^\d]/g, '');
		var left = position.left / fieldSize.width;
		var top = position.top / fieldSize.height;
		$.ajax({
			type: "POST",
			url: "/pawns/" + pawnId, 
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
