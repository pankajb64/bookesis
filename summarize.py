from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import sys
import os

file = sys.argv[1].strip()
out_file = sys.argv[2].strip()
line_count = sys.argv[3].strip()

parser = PlaintextParser.from_file(file, Tokenizer("english"))
summarizer = LexRankSummarizer()

summary = summarizer(parser.document, line_count)

f = open(os.path.join(out_file), 'w')
for sentence in summary:
	f.write(str(sentence)+"\n")
	
f.close()
