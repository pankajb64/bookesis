sys_files=`ls rouge/rouge_project/system/*.txt`
for sfile in $sys_files
do
base_name=`basename $sfile`
ref_name=`echo $base_name | sed -E"s/system(\d).txt/reference1.txt/g"`
ref_file="rouge/rouge_project/reference/$ref_name"
echo "Comparing $sfile with $ref_file"
done
