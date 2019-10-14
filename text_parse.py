from catalog.models import Book
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer


def deconjugate_test():
    text = Book.objects.filter(pk=10).first().text
    print(deconjugate(text))


def deconjugate(text):
    # from nltk.corpus import stopwords
    # stop_words = set(stopwords.words('french'))
    words = word_tokenize(text)
    lemmatizer = FrenchLefffLemmatizer()
    words_parsed = []
    id = 0

    def span(wd, wd_id, disp):
        return f'<span style="display:{disp};" id="{wd_id}">{wd}</span>'
    for word in words:
        id += 1
        a_word = False
        words_parsed.append(span(word, id, 'inline'))
        lemma = lemmatizer.lemmatize(word.upper(), 'v')
        if lemma == lemma.upper():
            lemma = lemmatizer.lemmatize(word.upper())
        if lemma != lemma.upper():
            a_word = True
        if a_word:
            id += 1
            words_parsed.append(span(lemma, id, 'none'))
    return TreebankWordDetokenizer().detokenize(words_parsed)

# import text_parse
# from importlib import reload
# from text_parse import *
# reload(text_parse).deconjugate_test()
