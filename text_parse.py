from catalog.models import Book
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer


def deconjugate_test():
    text =  Book.objects.filter(pk=10).first().text
    print(deconjugate(text))


def deconjugate(text):
    # from nltk.corpus import stopwords
    # stop_words = set(stopwords.words('french'))
    words = word_tokenize(text)[:1000]
    lemmatizer = FrenchLefffLemmatizer()
    words_filtered = []
    words_parsed = []
    for word in words:
        a_word = False
        words_parsed.append(word)
        lemma = lemmatizer.lemmatize(word.upper(), 'v')
        if lemma == lemma.upper():
            lemma = lemmatizer.lemmatize(word.upper())
        if lemma != lemma.upper():
            a_word = True
        if a_word:
            words_parsed.append(f'({lemma})')
            words_filtered.append(word)
    # return words_filtered[:1000]
    return TreebankWordDetokenizer().detokenize(words_parsed) #result

# import text_parse
# from importlib import reload
# from text_parse import *
# reload(text_parse).deconjugate_test()
