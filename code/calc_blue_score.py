from bleu import calculate_bleu_score
import sys

ref_path=sys.argv[1].strip()
sys_path=sys.argv[2].strip()

print(calculate_bleu_score(ref_path, sys_path))
