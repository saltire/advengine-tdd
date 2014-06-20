$(function() {
	$('body')
	
	// expand/collapse controls
	.on('click', '.control-header', function() {
		$(this).next().children().children().slideToggle();
	});
});
