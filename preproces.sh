index_files=`ls data/*/*index_words.txt` #all files ending with index_words.txt
for file in $index_files
do
sed -i -E "s/[^a-zA-Z '-]//g" $file #remove anything thats not a letter, space, ' or -
sed -i -E "s/ +/ /g" $file  #replace multiple spaces with a single space
sed -i -E "s/ -+ / /g" $file #remove stray hyphens
sed -i -E "s/ -//g" $file #remove hyphens at beginning of the word
sed -i -E "s/- /-/g" $file #join word ending with hyphen with the next word
sed -i -E "s/ *- *$//g" $file #remove stray hyphens
sed -i -E "s/^ *- *//g" $file #remove stray hyphens
sed -i -E "s/^ +//g" $file #remove leading spaces
sed -i -E "s/ +$//g" $file #remove trailing spaces
sed -i -E "s/^(.){1,4}$//g" $file #remove small words (length 1-4)
sed -i -E "s/^ *index *$//gI" $file #remove line containing just the word "INDEX"
sed -i "/^ *$/d" $file #delete empty lines
sort -u $file -o $file #sort the file, removing duplicates
done
