$(function(){
    function adjustInputWidth($input) {
        var newWidth = $input.parent().innerWidth();
        $input.width(newWidth);
    }

    function adjustInputWidths() {
        $('.hidden-file-input').each(function() {
            adjustInputWidth($(this));
        })
    }

    adjustInputWidths();
});