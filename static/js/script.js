$(document).ready(function() {
	$(".photo").on('click', function() {
		var url = $(this).attr('src');
		$("#modal-image").attr('src', url);
		$("#myModal").modal("show");
	});

});