# -*- coding: utf-8 -*-

import sys, os
from pymarkovchain import MarkovChain

# Change these as you like.
DB_FILE = './worm-markov-db'
SOURCE_FILE = './worm-full-text.txt'
OUTPUT_FILE = './generated-text.txt'
GENERATED_STRING_LENGTH = 500

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

# Generate the string
# We could be a bit smarter about this, but it works fairly well
gen_string = ''
while len(gen_string) < GENERATED_STRING_LENGTH:
    new_str = mc.generateString()

    if gen_string.endswith(','):
        new_str = new_str[0].lower() + new_str[1:]
    else:
        new_str += '. '

    gen_string += new_str

# Write the generated text to file and output in console.
print(gen_string)
with open(OUTPUT_FILE, 'w') as f:
    f.write(gen_string)
