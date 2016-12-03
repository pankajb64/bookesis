import nltk.data
import sys
import os
def remove_non_ASCII(content):
    content_printable_list=[c for c in content if (32 <= ord(c) and ord(c) <= 126)]
    return ''.join(content_printable_list)

def collect_all_sentences(text_lines,sentence_splitter):
	print "num lines:", len(text_lines)
	sentences_tok=[]
	line_count=0
	for content in text_lines:
		line_count+=1
		if(line_count%1000==0):
			print float(line_count)/len(text_lines)
		content_printable=remove_non_ASCII(content)
		#print content_printable
		content_printable=content_printable.replace("Mr .","Mr")
		sentences_raw = sentence_splitter.tokenize(content_printable)
		#print sentences_raw
		
		for sent in sentences_raw:
			sentences_tok.append(sent)
		#	sentences_tok.append([x for x in sent.split()])

	#sentences_toks = [[w.lower() for w in sent_toks if w not in filter_tokens_set] for sent_toks in sentences_toks_origcase]

	return sentences_tok

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
filename = sys.argv[1].strip()
outfile = sys.argv[2].strip()
f = open(os.path.join(filename))
data = f.read()
f.close()
decode_arg = sys.argv[3].strip()
decode = True if decode_arg == "true" else False
#if decode:
#data = data.decode('utf-8')
data = unicode(data, errors='replace')
sentences = sent_detector.tokenize(data.strip())
f1 = open(os.path.join(outfile), 'w')
for sentence in sentences:
	f1.write(remove_non_ASCII(sentence)+"\n")	
	#f1.write((sentence).encode('utf-8'))
f1.close()
