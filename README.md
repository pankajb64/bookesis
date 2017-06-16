Bookesis - Automated Extractive Book summarization using Back-Index (based on NLTK and sumy). CS 585 NLP Project - https://www.researchgate.net/project/Book-Content-Summarization-using-Index, final Report [here](reports/Report%20-%20Content%20Summarization%20of%20a%20Book%20using%20its%20Index.pdf)

Generating coherent summaries of long documents such as books is a relatively untouched field, with most of the research work being focused on short documents. In this Project, we looked at summarization of books which have a back-index as a novel technique for generating good summaries. We provided a new dataset for the evaluation of such summarization systems. We focused on extractive summarization using LexRank, an unsupervised learning algorithm based on eigenvector sentence centrality and compared it with the current state-of-the-art methods. The results were promising and merit future research.

Summarized using Lex Rank Summarizer - See https://github.com/miso-belica/sumy/blob/dev/sumy/summarizers/lex_rank.py

To summarize data using index words, run `summarize.sh` from the `code`directory (give paths to your data folder just like in the script).
