from datetime import datetime
from django.contrib.auth.models import User
from user.models import UserSettings
from catalog.models import Language, Book, Author, Genre
from django.test import TestCase, SimpleTestCase


def init_langs():
    Language.objects.create(name='Azerbaijani', language_code='az')
    Language.objects.create(name='Malayalam', language_code='ml')
    Language.objects.create(name='Albanian', language_code='sq')
    Language.objects.create(name='Maltese', language_code='mt')
    Language.objects.create(name='Amharic', language_code='am')
    Language.objects.create(name='Macedonian', language_code='mk')
    Language.objects.create(name='English', language_code='en')
    Language.objects.create(name='Maori', language_code='mi')
    Language.objects.create(name='Arab', language_code='ar')
    Language.objects.create(name='Marathi', language_code='mr')
    Language.objects.create(name='Armenian', language_code='hy')
    Language.objects.create(name='Mari', language_code='mhr')
    Language.objects.create(name='Afrikaans', language_code='af')
    Language.objects.create(name='Mongolian', language_code='mn')
    Language.objects.create(name='Basque', language_code='eu')
    Language.objects.create(name='German', language_code='de')
    Language.objects.create(name='Bashkir', language_code='ba')
    Language.objects.create(name='Nepali', language_code='ne')
    Language.objects.create(name='Belarusian', language_code='be')
    Language.objects.create(name='Norwegian', language_code='no')
    Language.objects.create(name='Bengali', language_code='bn')
    Language.objects.create(name='Punjabi', language_code='pa')
    Language.objects.create(name='Burmese', language_code='my')
    Language.objects.create(name='Papiamento', language_code='pap')
    Language.objects.create(name='Bulgarian', language_code='bg')
    Language.objects.create(name='Persian', language_code='fa')
    Language.objects.create(name='Bosnian', language_code='bs')
    Language.objects.create(name='Polish', language_code='pl')
    Language.objects.create(name='Welsh', language_code='cy')
    Language.objects.create(name='Portuguese', language_code='pt')
    Language.objects.create(name='Hungarian', language_code='hu')
    Language.objects.create(name='Romanian', language_code='ro')
    Language.objects.create(name='Vietnamese', language_code='vi')
    Language.objects.create(name='Russian', language_code='ru')
    Language.objects.create(name='Haitian (Creole)', language_code='ht')
    Language.objects.create(name='Cebuano', language_code='ceb')
    Language.objects.create(name='Galician', language_code='gl')
    Language.objects.create(name='Serbian', language_code='SK')
    Language.objects.create(name='Dutch', language_code='nl')
    Language.objects.create(name='Sinhala', language_code='si')
    Language.objects.create(name='Mari', language_code='mrj')
    Language.objects.create(name='Slovak', language_code='sk')
    Language.objects.create(name='Greek', language_code='el')
    Language.objects.create(name='Slovenian', language_code='sl')
    Language.objects.create(name='Georgian', language_code='ka')
    Language.objects.create(name='Swahili', language_code='sw')
    Language.objects.create(name='Gujarati', language_code='gu')
    Language.objects.create(name='Sundanese', language_code='su')
    Language.objects.create(name='Danish', language_code='da')
    Language.objects.create(name='Tajik', language_code='tg')
    Language.objects.create(name='Hebrew', language_code='he')
    Language.objects.create(name='Thai', language_code='th')
    Language.objects.create(name='Yiddish', language_code='yi')
    Language.objects.create(name='Tagalog', language_code='tl')
    Language.objects.create(name='Indonesian', language_code='id')
    Language.objects.create(name='Tamil', language_code='ta')
    Language.objects.create(name='Irish', language_code='ga')
    Language.objects.create(name='Tatar', language_code='tt')
    Language.objects.create(name='Italian', language_code='it')
    Language.objects.create(name='Telugu', language_code='te')
    Language.objects.create(name='Icelandic', language_code='is')
    Language.objects.create(name='Turkish', language_code='tr')
    Language.objects.create(name='Spanish', language_code='es')
    Language.objects.create(name='Udmurt', language_code='udm')
    Language.objects.create(name='Kazakh', language_code='kk')
    Language.objects.create(name='Uzbek', language_code='uz')
    Language.objects.create(name='Kannada', language_code='kn')
    Language.objects.create(name='Ukrainian', language_code='uk')
    Language.objects.create(name='Catalan', language_code='ca')
    Language.objects.create(name='Urdu', language_code='ur')
    Language.objects.create(name='Kirghiz', language_code='ky')
    Language.objects.create(name='Finnish', language_code='fi')
    Language.objects.create(name='Chinese', language_code='zh')
    Language.objects.create(name='French', language_code='fr')
    Language.objects.create(name='Korean', language_code='ko')
    Language.objects.create(name='Hindi', language_code='hi')
    Language.objects.create(name='Xhosa', language_code='xh')
    Language.objects.create(name='Croatian', language_code='hr')
    Language.objects.create(name='Khmer', language_code='km')
    Language.objects.create(name='Czech', language_code='cs')
    Language.objects.create(name='Lao', language_code='lo')
    Language.objects.create(name='Swedish', language_code='sv')
    Language.objects.create(name='Latin', language_code='la')
    Language.objects.create(name='Scottish', language_code='gd')
    Language.objects.create(name='Latvian', language_code='lv')
    Language.objects.create(name='Estonian', language_code='et')
    Language.objects.create(name='Lithuanian', language_code='lt')
    Language.objects.create(name='Esperanto', language_code='eo')
    Language.objects.create(name='Luxembourg', language_code='lb')
    Language.objects.create(name='Javanese', language_code='jv')
    Language.objects.create(name='Malagasy', language_code='mg')
    Language.objects.create(name='Japanese', language_code='ja')
    Language.objects.create(name='Malay', language_code='ms')


def init_author():
    return  Author.objects.create(
        date_of_birth=datetime.strptime('01.01.2001', '%d.%m.%Y'),
        date_of_death=datetime.strptime('01.01.2021', '%d.%m.%Y'),
        first_name="Test",
        last_name="Author"
    )


def init_genre():
    return Genre.objects.create(
        name='Test genre',
    )


def init(delete_all):
    if delete_all:
        Language.objects.all().delete()
        init_langs()
        Book.objects.all().delete()
    if len(Book.objects.all()) > 0:
        book = Book.objects.all().first()
    else:
        book = Book.objects.create(
            title='My test book',
            author=init_author(),
            summary='test summary',
            isbn='1111111111111',
            text='My test text. Two sentences.'
        )
        book.genre.set((init_genre(),))
        book.save()
    user = User.objects.get(pk=1)
    book.text_with_translation, translate, book.translation_problems = translate_in_place(book, user, True)
    book.save()
    return book.text_with_translation, translate, book.translation_problems


def translate_in_place(book, user, set_book_langs_if_none: bool):
    from yandex_translate import YandexTranslate
    translate = YandexTranslate('trnsl.1.1.20181030T164747Z.50350640be185f5d.a9c2d0892171111c7027edd85669141908d3301a')
    # print('Languages:', translate.langs)
    # print('Translate directions:', translate.directions)
    # print('Detect language:', translate.detect('Привет, мир!'))
    # print('Translate:', translate.translate('Привет, мир!', 'ru-en'))  # or just 'en'
    if not book.source_language:
        from_lang = translate.detect(book.text)
        if set_book_langs_if_none:
            book.source_language = Language.objects.filter(language_code=from_lang).first()
            # book.save()
    else:
        from_lang = book.source_language.language_code

    if not book.translation_language:
        default_lang = UserSettings.objects.filter(user=user).first().default_translation_language
        if default_lang:
            to_lang = default_lang.language_code
        else:
            to_lang = 'fr'
        if set_book_langs_if_none:
            book.translation_language = Language.objects.filter(language_code=to_lang).first()
            # book.save()
    else:
        to_lang = book.translation_language.language_code

    sentences = split_text_by_sentences(book.text)
    text_with_translation = ''
    translation_problems = ''
    translate_directions = f'{from_lang}-{to_lang}'
    for sentence in sentences:
        translation_result = translate.translate(sentence, translate_directions)
        if translation_result['code'] != 200:
            translation_problems = '\n'.join([translation_problems, translation_result['code']])
            translation_problems = '\n'.join([translation_problems, sentence])
            translation_problems = '\n'.join([translation_problems, translation_result['text'][0], ''])
        text_with_translation = '\n'.join([text_with_translation, sentence])
        text_with_translation = '\n'.join([text_with_translation, translation_result['text'][0], ''])
    return text_with_translation, translate, translation_problems


def split_text_by_sentences(text):
    import re
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences


# import catalog.init_db
# from importlib import reload
# _, tr, _ = reload(catalog.init_db).init_books(True)
