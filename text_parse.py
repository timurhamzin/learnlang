from catalog.models import Book
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
from catalog.models import Language
import spacy


def deconjugate_test():
    book = Book.objects.filter(pk=10).first()
    text = book.text
    print(deconjugate(text, book.source_language))


def deconjugate_word(word, lang: Language):
    if lang.language_code == 'fr':
        lemmatizer = FrenchLefffLemmatizer()
        result = lemmatizer.lemmatize(word.upper(), 'v')
        if result == result.upper():
            result = lemmatizer.lemmatize(word.upper())
        if result != result.upper():
            return result
    elif lang.language_code == 'en':
        pass
    else:
        pass


def deconjugate(text, lang: Language):
    # from nltk.corpus import stopwords
    # stop_words = set(stopwords.words('french'))
    # words = word_tokenize(text)
    nlp = spacy.load(lang.language_code, disable=['parser', 'ner'])
    doc = nlp(text)

    def span(wd, wd_id, disp):
        return f'<span style="display:{disp};" id="{wd_id}">{wd}</span>'
    id = 0
    words_parsed = []
    for token in doc:
        id += 1
        words_parsed.append(span(token.text, id, 'inline'))
        id += 1
        words_parsed.append(span(token.lemma_, id, 'inline'))
    return TreebankWordDetokenizer().detokenize(words_parsed)

# import text_parse
# from importlib import reload
# from text_parse import *
# reload(text_parse).deconjugate_test()
