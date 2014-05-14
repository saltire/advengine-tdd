$(function() {
	$('body')
	.on('click', '.objects li', function() {
		$('.details', this).slideToggle();
	})
	.on('click', '.details', function(e) {
		e.stopPropagation();
	})
	
	// expand/collapse controls
	.on('click', '.control-header', function() {
		$(this).next().children().children().slideToggle();
	});
});
