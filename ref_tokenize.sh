ref_files=`ls data/*/*_ref.txt`
for ref_file in $ref_files
do
ref_tok_file=`echo $ref_file | sed "s/ref.txt/ref_tok.txt/g"`
#echo "Tokenizing $ref_file, output will be written to $ref_tok_file"
python nltk_tokenize.py $ref_file $ref_tok_file "false"
done
