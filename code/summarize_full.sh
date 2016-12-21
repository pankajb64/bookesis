extract_files=`ls data/*/*content_tok.txt`
for extract_file in $extract_files
do
summary_file=`echo $extract_file | sed "s/content_tok.txt/summary_full.txt/g"`
ref_tok_file=`echo $extract_file | sed "s/content_tok.txt/ref_tok.txt/g"`
ref_tok_wc=`cat $ref_tok_file | wc -l`
python summarize.py $extract_file $summary_file $ref_tok_wc
done
