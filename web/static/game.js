$(function() {
	$('body').on('click', '.objects li', function() {
		$('.details', this).slideToggle();
	}).on('click', '.details', function(e) {
		e.stopPropagation();
	});
});
