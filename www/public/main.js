document.addEventListener("DOMContentLoaded", function() {
    'use strict';

    var textLocation = document.querySelectorAll('#generated p')[0]
    var button = document.getElementById('generate-button');
    var lengthField = document.getElementById('generate-length');

    textLocation.textContent = '';

    // Only allow numbers in length input
    lengthField.addEventListener('input', function (event) {
        var text = this.value;

        text = text.replace(/[^0-9]/g, '');

        if (parseInt(text, 10) > 5000) {
            text = 5000
        }

        this.value = text + ' chars';
    });

    lengthField.addEventListener('keypress', function (event) {
        if (event.which === 13) generate();
    });

    // Send an HTTP request asking for the text, then fill the box
    function generate(event) {
        if (event) event.preventDefault();
        textLocation.parentElement.classList.add('loading');

        var xmlhttp = new XMLHttpRequest();
        var genLength = lengthField.value.replace(/[^0-9]/g, '');

        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
                if (xmlhttp.status == 200) {
                    textLocation.textContent = xmlhttp.responseText;
                } else {
                    textLocation.textContent = "Whoops, an error occurred."
                }
                textLocation.parentElement.classList.remove('loading');
            }
        };

        xmlhttp.open("GET", './generate?length=' + genLength);
        xmlhttp.send();
    }

    button.addEventListener('click', generate);

    generate();
});
