$(function(){
    function adjustInputSize($input) {
        var newWidth = $input.parent().innerWidth(),
            newHeight = $input.parent().innerHeight();
        $input.width(newWidth);
        $input.height(newHeight);
    }

    function adjustInputSizes() {
        $('.hidden-file-input').each(function() {
            adjustInputSize($(this));
        })
    }

    // Handle events with resizing to allow the choose file buttons
    // to keep the input tag within the button
    adjustInputSizes();
    $(window).resize(adjustInputSizes);
    $('.btn.file-input-btn').resize(adjustInputSizes);

    $('#newBtn').click(createNewFileInput);

    function handler_updateInputText() {
        var filepath = $(this).val().split('\\'),
            filename = filepath[filepath.length - 1],
            $span = $(this).siblings('.filename');
        if (filename == '') {
            filename = 'Chose a file...';
        }
        $span.text(filename);
        adjustInputSize($(this));
    }
    $('.hidden-file-input').change(handler_updateInputText);

    function createElement(tag, elementClass) {
        var $newElem = $(document.createElement(tag));
        if (elementClass)
            $newElem.addClass(elementClass);
        return $newElem
    }
    function createNewFileInput() {
        var $container = createElement('div', 'btn btn-default input-file-btn'),
            $text = createElement('span', 'filename'),
            $input = createElement('input', 'hidden-file-input');

        $text.text('Choose a file...');
        $input.attr('accept', '.cpp,.h').attr('type', 'file');
        $container.append($text).append($input);
        $('#input-files').append($container);
        adjustInputSize($input);
        $input.change(handler_updateInputText)
    }
});