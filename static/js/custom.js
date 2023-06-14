// Hide Bootstrap Alert After 5 Second
$(".alert").delay(4000).slideUp(200, function() {
    $(this).alert('close');
});

// Select2
$(document).ready(function() {
    $('.django-select2').select2();
});