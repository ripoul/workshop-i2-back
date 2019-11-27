def extract_keywords(raw_text):
    """
    :raw_text: (str) raw text
    :return: (list of str)
    """
    raw_keywords = raw_text.split(" ")
    unique_keywords = list(set(raw_keywords))
    return raw_keywords