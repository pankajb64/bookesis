index_file = "data/hoi_index.txt"
content_file = "data/hoi_content.txt"

f1 = open(index_file)
f2 = open(content_file)

indices = f1.readlines()
sentences = f2.readlines()

result = []
for sentence in sentences:
    sentence = sentence.strip()
    for index in indices:
        index = index.strip()
        if index in sentence:
            result.append(sentence.strip())
            break


for sentence in result:
    print sentence

f1.close()
f2.close()