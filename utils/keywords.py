import pke 
def search_keywords(text):
    """ Extracts keywords from the text using TextRank algorithm.
    Args:
        text (str): Text from which keywords are to be extracted.
        Returns:
        keyphrases (list): List of keyphrases extracted from the text.
        keywords (list): List of keywords extracted from the text.
        """
    # define the set of valid Part-of-Speeches
    pos = {'NOUN', 'PROPN', 'ADJ'}

    # 1. create a TextRank extractor.
    extractor = pke.unsupervised.TextRank()

    # 2. load the content of the document.
    extractor.load_document(input=text,
                            language='en',
                            normalization=None)

    # 3. build the graph representation of the document and rank the words.
    #    Keyphrase candidates are composed from the 33-percent
    #    highest-ranked words.
    extractor.candidate_weighting(window=2,
                                pos=pos,
                                top_percent=0.33)

    # 4. get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=10)
    keywords = [keyphrase for keyphrase, score in keyphrases]
    return keyphrases,keywords
text = """
Graph-based ranking algorithms are essentially a
way of deciding the importance of a vertex within
a graph, based on global information recursively
drawn from the entire graph. The basic idea implemented by a graph-based ranking model is that
of “voting” or “recommendation”. When one vertex links to another one, it is basically casting a vote
for that other vertex. The higher the number of votes
that are cast for a vertex, the higher the importance
of the vertex. Moreover, the importance of the vertex
casting the vote determines how important the vote
itself is, and this information is also taken into account by the ranking model. Hence, the score associated with a vertex is determined based on the votes
that are cast for it, and the score of the vertices casting these votes.
"""
print(search_keywords(text))