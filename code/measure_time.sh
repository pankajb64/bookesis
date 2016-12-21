ref_tok_len=`cat data/common_sense_economics/cse_ref_tok.txt | wc -l`
out_file="test/cse_test.txt"
out_full_file="test/cse_test_full.txt"
index_file="data/common_sense_economics/cse_extract.txt"
full_file="data/common_sense_economics/cse_content_tok.txt"

/usr/bin/time -f "Time taken to summarize extract - %e seconds" python summarize.py $index_file $out_file $ref_tok_len

/usr/bin/time -f "Time taken to summarize full text - %e seconds" python summarize.py $full_file $out_full_file $ref_tok_len
