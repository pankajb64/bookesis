content_files=`ls data/*/*content_tok.txt`
for content_file in $content_files
do
index_word_file=`echo $content_file | sed "s/content_tok.txt/index_words.txt/g"`
extract_file=`echo $content_file | sed "s/content_tok.txt/extract.txt/g"`
python extract_sentence.py $index_word_file $content_file $extract_file
done
