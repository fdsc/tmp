$(document).ready(function () {
	var inc = true;

	heightOfshow = $("#show")[0].scrollHeight;
	if(heightOfshow <= 80) {
		$("#show_more").hide();
	}

	$("#show_more").click(function () {

		if(inc) {
			$("#show").animate({
				height: heightOfshow
			}, 500, "swing", function () {
				inc = false;
			});
			$('#show_more_text').text('свернуть');
		}
		else {
			over();
		}
	});

	function over() {
		heightOfshow = $("#show")[0].scrollHeight;
		inc = true;
		$("#show").animate({
			height: 80
		}, 500);
		$('#show_more_text').text('развернуть');
	}

	$(document).bind('click', function (e) {
		if($(e.target).closest('#addrblock').length) return;
		over();

	});
});