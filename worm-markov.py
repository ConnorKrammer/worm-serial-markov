# -*- coding: utf-8 -*-

import sys, os, re
from pymarkovchain import MarkovChain

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

# Generate the string
# We could be a bit smarter about this, but it works fairly well
gen_string = ''
short_counter = 0
while len(gen_string) < GENERATED_STRING_LENGTH:
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

# Print output. We do this for users of the command line, as well
# as for the node.js script that calls this from www/
print(gen_string)
sys.stdout.flush()

# Save to file, unless --no-save was passed
if len(sys.argv) < 3 or sys.argv[2] != '--no-save':
    with open(OUTPUT_FILE, 'w') as f:
        f.write(gen_string)
