// Require modules
var express     = require('express');
var compression = require('compression');
var spawn       = require('child_process').spawn;

/*==================================
 *             Setup
 *==================================*/

var app = express();

app.use(compression());
app.use(express.static(__dirname + '/public', {
    maxAge: 24 * 60 * 60 * 1000 // 1 day
}));

var reqCounter = 0;

app.get('/generate', function (req, res) {
    var reqCount = reqCounter++;
    var generateLength = Math.max(0, req.query.length) || 500;
    generateLength = Math.min(req.query.length, 5000);

    console.log('> [' + reqCount + '] text length: "' + generateLength + '"');

    // call the Python Markov script
    var process = spawn('python', ['../worm-markov.py', generateLength, '--no-save']);
    var output = ''

    process.stdout.on('data', function (data) {
        output += data;
    });

    process.on('close', function (code) {
        if (code !== 0) {
            var msg = 'ERROR: Please file an issue on '
                    + '<a href="https://github.com/ConnorKrammer/worm-serial-markov/issues">GitHub</a> '
                    + 'or contact the administrator.';
            res.status(500).send(msg);
        } else {
            res.status(200).send(output);
        }
    });

    console.log('> [' + reqCount + '] request response sent');
});

app.listen(8001);
console.log('> server ready');
