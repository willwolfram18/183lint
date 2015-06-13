$(function() {
    // Adjust a single hidden file input to match the height and width of its parent
    function adjustInputSize($input) {
        var newWidth = $input.parent().innerWidth(),
            newHeight = $input.parent().innerHeight();
        $input.width(newWidth);
        $input.height(newHeight);
    }

    // Adjust all hidden file inputs to match each individual's parent's height and width
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

    // Change text of button when a file is selected
    function handler_updateInputText() {
        var filepath = $(this).val().split('\\'),
            filename = filepath[filepath.length - 1],
            $span = $(this).siblings('.filename');
        if (filename == '') {
            filename = 'Chose a file...';
        }
        $span.text(filename);
        // Button's auto wrap the $span, therefore adjust the size of the input field
        adjustInputSize($(this));
    }
    $('.hidden-file-input').change(handler_updateInputText);

    // elementClass is a space separated list of classes for the created tag
    function createElement(tag, elementClass) {
        var $newElem = $(document.createElement(tag));
        if (elementClass)
            $newElem.addClass(elementClass);
        return $newElem
    }
    function createNewFileInput() {
        var $container = createElement('div', 'btn btn-default file-input-btn'),
            $text = createElement('span', 'filename'),
            $input = createElement('input', 'hidden-file-input');

        $text.text('Choose a file...');
        $input.attr('accept', '.cpp,.h').attr('type', 'file');
        $container.append($text).append($input);
        $('#newBtn').before($container).before('<br>');
        adjustInputSize($input);
        // Apply the handlers to new elements that appear
        $input.change(handler_updateInputText).change(handler_activateSubmitButton);
    }

    // Toggle submit button whenever at least 1 input contains a file
    function handler_activateSubmitButton() {
        var isActive = false;
        $('.hidden-file-input').each(function() {
            if ($(this).val() != '') {
                isActive = true;
                $('#submit-btn').removeClass('disabled');
            }
        })

        if (!isActive) {
            $('#submit-btn').addClass('disabled');
        }
    }
    $('.hidden-file-input').change(handler_activateSubmitButton);


});