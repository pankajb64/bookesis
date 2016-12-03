extract_files=`ls data/*/*extract.txt`
for extract_file in $extract_files
do
summary_file=`echo $extract_file | sed "s/extract.txt/summary.txt/g"`
ref_tok_file=`echo $extract_file | sed "s/extract.txt/ref_tok.txt/g"`
ref_tok_wc=`cat $ref_tok_file | wc -l`
python summarize.py $extract_file $summary_file $ref_tok_wc
done