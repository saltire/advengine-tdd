$(function() {
	$('body').on('click', 'h3', function() {
		$(this).next().slideToggle();
	});
});
