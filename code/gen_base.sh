content_tok_files=`ls data/*/*content_tok.txt`
for ctf in $content_tok_files
do
base_file=`echo $ctf | sed "s/content_tok.txt/base.txt/g"`
ref_tok_file=`echo $ctf | sed "s/content_tok.txt/ref_tok.txt/g"`
ref_tok_wc=`cat $ref_tok_file | wc -l`
head -n $ref_tok_wc $ctf > $base_file
done
