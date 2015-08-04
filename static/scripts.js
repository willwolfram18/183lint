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

    // Change text of button when a file is selected
    function handler_updateInputText() {
        var files = $(this)[0].files,
            $span = $(this).siblings('.filename'),
            filename;
        if (files.length == 0) {
            filename = "Choose a file..."
            $(this).tooltip('destroy');
        } else if (files.length == 1) {
            filename = files[0].name;
            $(this).tooltip('destroy');
        } else {
            filename = files.length + ' files';
            var strVal = files[0].name;
            for (var i = 1; i < files.length; i++) {
                strVal += '<br>' + files[i].name
            }
            $(this).tooltip({
                html: true,
                placement: 'bottom',
                title: strVal,
            });
            $(this).tooltip('hide')
                   .attr('data-original-title', strVal)
                   .tooltip('fixTitle');
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

    // Toggle submit button whenever at least 1 input contains a file
    function clearButtons() {
        $('#input-files')[0].reset();
        $('.hidden-file-input').trigger('change');
        handler_activateSubmitButton(); // deactivates button
    }
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


    var spinnerOpts = {
        radius: 30,
        length: 30,
        position: 'relative',
    };
    var $spinner = new Spinner(spinnerOpts);
    function showSpinner() {
        $('#results').addClass('hidden').text('');
        $spinner.spin($('#spinner')[0]);
    }
    function hideSpinner() {
        $spinner.stop();
    }
    function handler_parseResponse(data) {
        console.log('Success!');
        clearButtons();
        $('#results').removeClass('hidden');
        // var results = '';
        // for (key in data) {
        //     if (results != '') {
        //         results += '\n\n';
        //     }
        //     results += 'Results for ' + key + ':\n'
        //     if (data[key].length == 0) {
        //         results += '  No errors found! :D'
        //     } else {
        //         for (var i = 0; i < data[key].length; i++) {
        //             results += '  ' + data[key][i];
        //             if (i != data[key].length - 1) {
        //                 results += '\n';
        //             }
        //         }
        //     }
        // }
        // $('#results').text(results);
        for (key in data) {
            var $panel = createElement('div', 'panel panel-default'),
                $heading = createElement('div', 'panel-heading'),
                $headingText = createElement('a'),
                $headingTitle = createElement('h4', 'panel-title'),
                $collapse = createElement('div', 'panel-collapse collapse'),
                $content = createElement('div', 'panel-body');

            $headingText.text(key).attr('data-toggle', 'collapse')
                        .attr('data-target', '#results #results_' + key).attr('data-parent', '#results')
                        .attr('role', 'button');
            $headingTitle.append($headingText);
            $heading.append($headingTitle);

            $content.text('Results!');
            $collapse.attr('id', 'results_' + key).append($content);

            $panel.append($collapse).prepend($heading);
            $('#results').append($panel);
        }
    }
    function handler_uploadFiles() {
        var formData = new FormData($('#input-files')[0]);
        $.ajax('/upload_files', {
            type: 'POST',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            beforeSend: showSpinner,
            success: handler_parseResponse,
            error: function() {
                console.log('Error!');
            },
            complete: hideSpinner,
        });
    }
    $('#submit-btn').click(handler_uploadFiles);
});