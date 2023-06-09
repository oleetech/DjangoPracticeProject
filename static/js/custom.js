// Hide Bootstrap Alert After 5 Second
$(".alert").delay(4000).slideUp(200, function() {
    $(this).alert('close');
});