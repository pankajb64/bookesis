import sys
import os

index_file = sys.argv[1].strip()
content_file = sys.argv[2].strip()
out_file = sys.argv[3].strip()

f1 = open(os.path.join(index_file))
f2 = open(os.path.join(content_file))

indices = f1.readlines()
sentences = f2.readlines()

f1.close()
f2.close()

result = []
for sentence in sentences:
    sentence = sentence.strip()
    for index in indices:
        index = index.strip()
        if index in sentence:
            result.append(sentence.strip())
            break


f3 = open(os.path.join(out_file), 'w')
for sentence in result:
    f3.write(sentence + "\n")

f3.close()
