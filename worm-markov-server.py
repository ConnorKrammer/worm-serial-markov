#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
from pymarkovchain import MarkovChain
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Change these as you like.
BASE        = os.path.dirname(os.path.abspath(__file__))
DB_FILE     = os.path.join(BASE, 'worm-markov-db')
SOURCE_FILE = os.path.join(BASE, 'worm-full-text.txt')
OUTPUT_FILE = os.path.join(BASE, 'generated-text.txt')
GENERATED_STRING_LENGTH = 500

# Allow command line argument override
if len(sys.argv) >= 2 and sys.argv[1].isdigit():
    GENERATED_STRING_LENGTH = int(sys.argv[1])

if not os.path.isfile(DB_FILE):
    # Handle common user errors
    if not os.path.isfile(SOURCE_FILE):
        if os.path.isfile(DB_FILE + '.7z'):
            sys.exit("NOTICE: Please extract the archive containing the Markov database before use.")
        sys.exit("NOTICE: You can't regenerate the Markov database without the source text.");

    # Moving this in here avoids an annoying warning message if either of the
    # above two sys.exit() calls would be triggered
    mc = MarkovChain(DB_FILE)

    # Generate the database
    with open(SOURCE_FILE, 'r') as f:
        mc.generateDatabase(f.read(), sentenceSep='[.!?"\n]', n=2)
    mc.dumpdb()
else:
    mc = MarkovChain(DB_FILE)

def generate_string(max_length):
    # Generate the string
    # We could be a bit smarter about this, but it works fairly well
    gen_string = ''
    short_counter = 0
    while len(gen_string) < max_length:
        new_str = mc.generateString().strip()
        new_str = re.sub(r' , ?', ', ', new_str)
    
        # Too short or too long to be meaningful
        if len(new_str) < 4 or len(new_str) > 100:
            continue
    
        # Don't allow too many very short phrases.
        if len(new_str) < 30:
            if short_counter > 3:
                continue
            short_counter += 1
    
        # Handle punctuation
        if gen_string.endswith(','):
            new_str = ' ' + new_str[0].lower() + new_str[1:]
    
        if not new_str.endswith(','):
            if (gen_string.endswith('. ') or gen_string.endswith('? ')) and re.search(r'^(are|who|what|when|where|why|how)', new_str.lower()):
                new_str += '? '
            else:
                new_str += '. '
        elif len(gen_string) + len(new_str) >= GENERATED_STRING_LENGTH:
            new_str = new_str[:-1] + '.'
    
        gen_string += new_str

    return gen_string
 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/plaintext')
        self.send_header('Access-Control-Allow-Origin', 'http://159.203.4.7:8001')
        self.end_headers()
 
        # Send message back to client
        query = urlparse(self.path).query
        params = parse_qs(query)
        max_length = int(params["length"][0])

        message = generate_string(max_length)
        print(max_length, message)

        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return
 
try:
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('', 8081)
    server = HTTPServer(server_address, testHTTPServer_RequestHandler)

    print('running server...')
    server.serve_forever()
except KeyboardInterrupt:
    print('shutting down the web server')
    server.socket.close()
