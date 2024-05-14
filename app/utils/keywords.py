import pke 
def search_keyphrases(path:str) -> list[str]:
    """ Extracts keywords from the text using TextRank algorithm.
    Args:
        path (str): Path to the text file.
    Returns:
        keyphrases (list): List of keyphrases extracted from the text.
        keywords (list): List of keywords extracted from the text.
        """
        
    open_file = open(path, "r")
    text = open_file.read()
        
        
    part_of_speech_tags: set = {'NOUN', 'PROPN', 'ADJ'}

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
                                pos=part_of_speech_tags,
                                top_percent=0.33)

    # 4. get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=6)
    return [keyword for keyword, score in keyphrases]

if __name__ == "__main__":
    path_to_file ="examples/summ_text.txt"
    print(search_keyphrases(path_to_file))
