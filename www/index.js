// Require modules
var express     = require('express');
var compression = require('compression');
var process     = require('child_process');

/*==================================
 *             Setup
 *==================================*/

var app = express();

app.use(compression());
app.use(express.static(__dirname + '/public', {
    maxAge: 24 * 60 * 60 * 1000 // 1 day
}));

app.listen(8001);
