# -*- coding: utf-8 -*-
 
"""BLEU.
 
Usage:
  bleu.py --reference FILE --translation FILE [--weights STR] [--smooth STR] [--smooth-epsilon STR] [--smooth-alpha STR] [--smooth-k STR] [--segment-level]
  bleu.py -r FILE -t FILE [-w STR] [--smooth STR] [--segment-level]
   
Options:
  -h --help              Show this screen.
  -r --reference FILE    reference file (Complusory)
  -t --translation FILE  hypothesis file (Complusory)
  -w --weights STR       weights [default: 0.25 0.25 0.25 0.25]
  --segment-level        prints segment level scores
  --smooth STR           smoothens segment level scores
  --smooth-epsilon STR   empirical smoothing parameter for method 1 [default: 0.1]
  --smooth-k STR         empirical smoothing parameter for method 4 [default: 5]
  --smooth-alpha STR     empirical smoothing parameter for method 6 [default: 5]
    
    
"""
 
from __future__ import division, print_function
 
import io
import math
import sys
from fractions import Fraction
from collections import Counter
from functools import reduce
from operator import or_
 
from docopt import docopt # pip install docopt # or wget https://raw.githubusercontent.com/docopt/docopt/master/docopt.py
 
try:
    from nltk import ngrams
except:
    def ngrams(sequence, n):
        sequence = iter(sequence)
        history = []
        while n > 1:
            history.append(next(sequence))
            n -= 1
        for item in sequence:
            history.append(item)
            yield tuple(history)
            del history[0]
 
 
def modified_precision(references, hypothesis, n):
    # Extracts all ngrams in hypothesis.
    counts = Counter(ngrams(hypothesis, n)) 
    if not counts:
        return Fraction(0)
    # Extract a union of references' counts.
    max_counts = reduce(or_, [Counter(ngrams(ref, n)) for ref in references])
    # Assigns the intersection between hypothesis and references' counts.
    clipped_counts = {ngram: min(count, max_counts[ngram]) for ngram, count in counts.items()}
    return Fraction(sum(clipped_counts.values()), sum(counts.values())) 
     
     
def corpus_bleu(list_of_references, hypotheses, weights=(0.25, 0.25, 0.25, 0.25),
                segment_level=False, smoothing=0, epsilon=1, alpha=1, 
                k=5):
    # Initialize the numbers.
    p_numerators = Counter() # Key = ngram order, and value = no. of ngram matches.
    p_denominators = Counter() # Key = ngram order, and value = no. of ngram in ref.
    hyp_lengths, ref_lengths = 0, 0
    # Iterate through each hypothesis and their corresponding references.
    for references, hypothesis in zip(list_of_references, hypotheses):
        # Calculate the hypothesis length and the closest reference length.
        # Adds them to the corpus-level hypothesis and reference counts.
        hyp_len =  len(hypothesis)
        hyp_lengths += hyp_len
        ref_lens = (len(reference) for reference in references)
        closest_ref_len = min(ref_lens, key=lambda ref_len: (abs(ref_len - hyp_len), ref_len))
        ref_lengths += closest_ref_len
        # Calculates the modified precision for each order of ngram.
        segment_level_precision = []
        for i, _ in enumerate(weights, start=1): 
            p_i = modified_precision(references, hypothesis, i)
            p_numerators[i] += p_i.numerator
            p_denominators[i] += p_i.denominator
            segment_level_precision.append(p_i)
         
        # Optionally, outputs segment level scores.
        if segment_level:
            _bp = min(math.exp(1 - closest_ref_len / hyp_len), 1.0)
            segment_level_precision = chen_and_cherry(references, hypothesis, 
                                                      segment_level_precision,
                                                      hyp_len, smoothing, epsilon,
                                                      alpha)
            segment_pn = [w*math.log(p_i) if p_i != 0 else 0 for p_i, w in
                          zip(segment_level_precision, weights)]
            print (_bp * math.exp(math.fsum(segment_pn)))
     
    # Calculate corpus-level brevity penalty.
    bp = min(math.exp(1 - ref_lengths / hyp_lengths), 1.0)
 
    # Calculate corpus-level modified precision.
    p_n = []
    p_n_str = []
    for i, w in enumerate(weights, start=1):
        p_i = Fraction(p_numerators[i] / p_denominators[i])
        p_n_str.append(p_i)
        try:
            p_n.append(w* math.log(p_i))
        except ValueError:
            p_n.append(0)
     
    # Final bleu score. 
    score = bp * math.exp(math.fsum(p_n))
    bleu_output = ("BLEU = {}, {} (BP={}, ratio={}, hyp_len={}, ref_len={})".format(
                  round(score*100, 2), '/'.join(map(str, [round(p_i*100, 1) for p_i in p_n_str])),
                  round(bp,3), round(hyp_lengths/ref_lengths, 3), hyp_lengths, ref_lengths))
    #print(bleu_output, file=sys.stderr)
    return score, p_n_str, hyp_lengths, ref_lengths
 
def chen_and_cherry(references, hypothesis, p_n, hyp_len, 
                    smoothing=0, epsilon=0.1, alpha=5, k=5):
    """
    Boxing Chen and Collin Cherry (2014) A Systematic Comparison of Smoothing 
    Techniques for Sentence-Level BLEU. In WMT14. 
    """
    # No smoothing.
    if smoothing == 0:
        return p_n
    # Smoothing method 1: Add *epsilon* counts to precision with 0 counts.
    if smoothing == 1:
        return [Fraction(p_i.numerator + epsilon, p_i.denominator) 
                if p_i.numerator == 0 else p_i for p_i in p_n]
    # Smoothing method 2: Add 1 to both numerator and denominator (Lin and Och 2004)
    if smoothing == 2:
        return [Fraction(p_i.numerator + 1, p_i.denominator + 1)
                for p_i in p_n]
    # Smoothing method 3: NIST geometric sequence smoothing 
    # The smoothing is computed by taking 1 / ( 2^k ), instead of 0, for each 
    # precision score whose matching n-gram count is null.
    # k is 1 for the first 'n' value for which the n-gram match count is null/
    # For example, if the text contains:
    #   - one 2-gram match
    #   - and (consequently) two 1-gram matches
    # the n-gram count for each individual precision score would be:
    #   - n=1  =>  prec_count = 2     (two unigrams)
    #   - n=2  =>  prec_count = 1     (one bigram)
    #   - n=3  =>  prec_count = 1/2   (no trigram,  taking 'smoothed' value of 1 / ( 2^k ), with k=1)
    #   - n=4  =>  prec_count = 1/4   (no fourgram, taking 'smoothed' value of 1 / ( 2^k ), with k=2)
    if smoothing == 3:
        incvnt = 1 # From the mteval-v13a.pl, it's referred to as k.
        for i, p_i in enumerate(p_n):
            if p_i == 0:
                p_n[i] = 1 / 2**incvnt
                incvnt+=1
        return p_n
    # Smoothing method 4: 
    # Shorter translations may have inflated precision values due to having 
    # smaller denominators; therefore, we give them proportionally
    # smaller smoothed counts. Instead of scaling to 1/(2^k), Chen and Cherry 
    # suggests dividing by 1/ln(len(T), where T is the length of the translation.
    if smoothing == 4:
        incvnt = 1
        for i, p_i in enumerate(p_n):
            if p_i == 0:
                p_n[i] = incvnt * k / log(hyp_len) # Note that this K is different from the K from NIST.
                incvnt+=1
        return p_n
    # Smoothing method 5:
    # The matched counts for similar values of n should be similar. To a 
    # calculate the n-gram matched count, it averages the n−1, n and n+1 gram 
    # matched counts.
    if smoothing == 5:
        m = {}
        # Requires an precision value for an addition ngram order.
        p_n_plus5 = p_n + [modified_precision(references, hypothesis, 5)]
        m[-1] = p_n[0] + 1
        for i, p_i in enumerate(p_n):
            p_n[i] = (m[i-1] + p_i + p_n_plus5[i+1]) / 3
            m[i] = p_n[i] 
        return p_n
    # Smoothing method 6:
    # Interpolates the maximum likelihood estimate of the precision *p_n* with 
    # a prior estimate *pi0*. The prior is estimated by assuming that the ratio 
    # between pn and pn−1 will be the same as that between pn−1 and pn−2.
    if smoothing == 6:
        for i, p_i in enumerate(p_n):
            if i in [1,2]: # Skips the first 2 orders of ngrams.
                continue
            else:
                pi0 = p_n[i-1]**2 / p_n[i-2]
                # No. of ngrams in translation.
                l = sum(1 for _ in ngrams(hypothesis, i+1))
                p_n[i] = (p_i + alpha * pi0) / (l + alpha)
        return p_n
    # Smoothing method
    if smoothing == 7:
        p_n = chen_and_cherry(references, hypothesis, p_n, hyp_len, smoothing=4)
        p_n = chen_and_cherry(references, hypothesis, p_n, hyp_len, smoothing=5)
        return p_n
 
 
def sentence_bleu_nbest(reference, hypotheses, weights=(0.25, 0.25, 0.25, 0.25),
                        smoothing=0, epsilon=0.1, alpha=5, k=5):
    for hi, hypothesis in enumerate(hypotheses):
        print('Translation {}... '.format(hi), file=sys.stderr, end="")
        bleu_output  =  corpus_bleu([(reference,)], [hypothesis.translation], weights)
        bleu_score, p_n, hyp_len, ref_len = bleu_output
        p_n = chen_and_cherry(reference, hypotheses, p_n, hyp_len, smoothing, epsilon)
        segment_pn = [w*math.log(p_i) if p_i != 0 else 0 for p_i, w in
                          zip(p_n, weights)]
        _bp = min(math.exp(1 - ref_len / hyp_len), 1.0) 
        yield _bp * math.exp(math.fsum(segment_pn))

def calculate_bleu_score(reference_file, hypothesis_file):
    score = 0
    with io.open(reference_file, 'r', encoding='utf8') as reffin, \
    io.open(hypothesis_file, 'r', encoding='utf8') as hypfin:
        list_of_references = ((r.split(),) for r in reffin)
        hypotheses = (h.split() for h in hypfin)
        score = corpus_bleu(list_of_references, hypotheses, 
                    weights=(0.25, 0.25, 0.25, 0.25), segment_level=None, 
                    smoothing=0, epsilon=0.0, alpha=0.0, k=0.0)
    return round(score[0]*100, 2)
 
if __name__ == '__main__':
    arguments = docopt(__doc__, version='BLEU version 0.0.1')
    # Parse arguments.
    hypothesis_file = arguments['--translation']
    reference_file = arguments['--reference']
    weights = tuple(map(float, arguments['--weights'].split()))
    segment_level = arguments['--segment-level']
    smoothing_method = int(arguments['--smooth'])
    epsilon = float(arguments['--smooth-epsilon'])
    alpha = float(arguments['--smooth-alpha'])
    k = float(arguments['--smooth-k'])
    print(weights)
    # Calculate BLEU scores.  
    with io.open(reference_file, 'r', encoding='utf8') as reffin, \
    io.open(hypothesis_file, 'r', encoding='utf8') as hypfin:
        list_of_references = ((r.split(),) for r in reffin)
        hypotheses = (h.split() for h in hypfin)
        score = corpus_bleu(list_of_references, hypotheses, 
                    weights=weights, segment_level=segment_level, 
                    smoothing=smoothing_method, epsilon=epsilon, alpha=alpha, k=k) 
    #print("Score is %s" %round(score[0]*100, 2))
#else:
#    calculate_bleu_score(reference_file, hypothesis_file)
        