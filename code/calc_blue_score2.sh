sys_files=`ls rouge/rouge_project/system/*.txt`
for sfile in $sys_files
do
base_name=`basename $sfile`
ref_name=`echo $base_name | sed -E "s/system[0-9].txt/reference1.txt/g"`
ref_file="rouge/rouge_project/reference/$ref_name"
bleu_score=`python calc_blue_score.py $ref_file $sfile`
echo "$sfile - $bleu_score"
done

