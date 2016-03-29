document.addEventListener("DOMContentLoaded", function() {
    'use strict';

    var textLocation = document.querySelectorAll('#generated p')[0]
    var container = textLocation.parentElement;
    var button = document.getElementById('generate-button');
    var lengthField = document.getElementById('generate-length');

    textLocation.textContent = '';

    // Only allow numbers in length input
    function validateLengthField() {
        var text = lengthField.value;

        text = text.replace(/[^0-9]/g, '');

        if (parseInt(text, 10) > 5000) {
            text = 5000
        }

        lengthField.value = text + ' chars';
    }

    // Send an HTTP request asking for the text, then fill the box
    function generate(event) {
        if (event) event.preventDefault();

        if (container.classList.contains('loading')) return;
        container.classList.add('loading');

        var xmlhttp = new XMLHttpRequest();
        var genLength = lengthField.value.replace(/[^0-9]/g, '');

        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
                // add a bit more visual delay
                window.setTimeout(function() {
                    if (xmlhttp.status == 200) {
                        textLocation.textContent = xmlhttp.responseText;
                    } else {
                        textLocation.textContent = "Whoops, an error occurred."
                    }

                    container.classList.remove('loading');
                }, 200);
            }
        };

        xmlhttp.open("GET", 'http://159.203.4.7:8081?length=' + genLength);
        xmlhttp.send();
    }

    button.addEventListener('click', generate);

    lengthField.addEventListener('blur', validateLengthField);

    lengthField.addEventListener('keypress', function (event) {
        if (event.which === 13) {
            validateLengthField();
	    generate();
	}
    });


    generate();
});
