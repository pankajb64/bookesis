from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import sys
import os

file = sys.argv[1].strip()
out_file = sys.argv[2].strip()
line_count = sys.argv[3].strip()

parser = PlaintextParser.from_file(file, Tokenizer("english"))
summarizer = TextRankSummarizer()

summary = summarizer(parser.document, line_count)

f = open(os.path.join(out_file), 'w')
for sentence in summary:
	f.write(str(sentence)+"\n")
	
f.close()
