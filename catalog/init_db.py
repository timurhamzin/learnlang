from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.models import User
from user.models import UserSettings
from catalog.models import Language, Book, Author, Genre
from os import path
from mutagen.mp3 import MP3
import datetime
import nltk.data
import glob
from zipfile import ZipFile
import re


# Zip the files from given directory that matches the filter
def zip_files_in_dir(dir_name, zip_file_name, file_filter=lambda x: re.search('.', x)):
    # create a ZipFile object
    with ZipFile(zip_file_name, 'w') as zip_obj:
        # Iterate over all the files in directory
        for folder_name, sub_folders, file_names in os.walk(dir_name):
            for file_name in file_names:
                if file_filter(file_name):
                    # create complete file path of file in directory
                    file_path = os.path.join(folder_name, file_name)
                    # Add file to zip
                    zip_obj.write(file_path, os.path.basename(file_path))
    return zip_file_name

def split_text_test():
    from catalog.models import Book
    book = Book.objects.filter(pk=5).first()
    return split_text(book.text)


def split_text(text):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    result = tokenizer.tokenize(text.replace('...', '$$.'))
    # print('\n-----\n'.join(tokenizer.tokenize(text)))
    return list(map(lambda x: x.replace('$$.', '...'), result))


def make_lrc_dict(book: Book):
    sentences = split_text(book.text)
    split_fld = path.join(settings.MEDIA_ROOT, 'catalog', 'book', str(book.id), 'split')
    start = 0
    i = 0
    result = {'lrc': {}, 'files': {}}
    for filename in sorted(os.listdir(split_fld))[0:len(sentences)]:
        if filename.endswith(".mp3"):
            audio = MP3(path.join(split_fld, filename))
            duration_sec = audio.info.length
            start_td = str(datetime.timedelta(seconds=start))
            hours = start_td[:1]
            if hours not in result['lrc']:
                result['lrc'][hours] = {}
                result['files'][hours] = {}
            lrc_it = result['lrc'][hours]
            files_it = result['files'][hours]
            mm_ss_fffffff = '.'.join((start_td[2:] + '.000000').split('.')[0:2])
            lrc_it[mm_ss_fffffff] = sentences[i].replace('\n', ' ').replace('\r', ' ')
            files_it[mm_ss_fffffff] = f'{((i+1)//2 + (i+1)%2):06}'
            start += duration_sec
            i += 1
    return result


def make_lrc_files(book):
    lrc_files_dict = make_lrc_dict(book)
    lrc_dict = lrc_files_dict['lrc']
    files_dict = lrc_files_dict['files']
    split_fld = path.join(settings.MEDIA_ROOT, 'catalog', 'book', str(book.id), 'split')
    join_fld = path.join(settings.MEDIA_ROOT, 'catalog', 'book', str(book.id), 'lrc')
    os.makedirs(join_fld, exist_ok=True)
    for hour in lrc_dict:
        hour_fld = os.path.join(split_fld, hour)
        os.makedirs(hour_fld, exist_ok=True)
        for _, file_prefix in files_dict[hour].items():
            for file in glob.glob(os.path.join(split_fld, file_prefix + '_*.mp3')):
                shutil.copy(file, hour_fld)
        merge_path = os.path.join(join_fld, hour)
        sys_merge_mp3 = f'cat {os.path.join(hour_fld, "*.mp3")} > {merge_path}.mp3'
        os.system(sys_merge_mp3)
        shutil.rmtree(hour_fld)
        lrc_text = '\n'.join([f'[{time}] {line}' for time, line in lrc_dict[hour].items()])
        with open(f'{merge_path}.lrc', "w") as text_file:
            text_file.write(lrc_text)

    def include_in_zip(file_name):
        if file_name.endswith('mp3') or file_name.endswith('lrc'):
            return True
    return zip_files_in_dir(join_fld, path.join(join_fld, book.title + '.zip'), include_in_zip)


def init_langs():
    Language.objects.create(name='Afrikaans', language_code='af')
    Language.objects.create(name='Albanian', language_code='sq')
    Language.objects.create(name='Amharic', language_code='am')
    Language.objects.create(name='Arab', language_code='ar')
    Language.objects.create(name='Armenian', language_code='hy')
    Language.objects.create(name='Azerbaijani', language_code='az')
    Language.objects.create(name='Bashkir', language_code='ba')
    Language.objects.create(name='Basque', language_code='eu')
    Language.objects.create(name='Belarusian', language_code='be')
    Language.objects.create(name='Bengali', language_code='bn')
    Language.objects.create(name='Bosnian', language_code='bs')
    Language.objects.create(name='Bulgarian', language_code='bg')
    Language.objects.create(name='Burmese', language_code='my')
    Language.objects.create(name='Catalan', language_code='ca')
    Language.objects.create(name='Cebuano', language_code='ceb')
    Language.objects.create(name='Chinese', language_code='zh')
    Language.objects.create(name='Croatian', language_code='hr')
    Language.objects.create(name='Czech', language_code='cs')
    Language.objects.create(name='Danish', language_code='da')
    Language.objects.create(name='Dutch', language_code='nl')
    Language.objects.create(name='English', language_code='en')
    Language.objects.create(name='Esperanto', language_code='eo')
    Language.objects.create(name='Estonian', language_code='et')
    Language.objects.create(name='Finnish', language_code='fi')
    Language.objects.create(name='French', language_code='fr')
    Language.objects.create(name='Galician', language_code='gl')
    Language.objects.create(name='Georgian', language_code='ka')
    Language.objects.create(name='German', language_code='de')
    Language.objects.create(name='Greek', language_code='el')
    Language.objects.create(name='Gujarati', language_code='gu')
    Language.objects.create(name='Haitian (Creole)', language_code='ht')
    Language.objects.create(name='Hebrew', language_code='he')
    Language.objects.create(name='Hindi', language_code='hi')
    Language.objects.create(name='Hungarian', language_code='hu')
    Language.objects.create(name='Icelandic', language_code='is')
    Language.objects.create(name='Indonesian', language_code='id')
    Language.objects.create(name='Irish', language_code='ga')
    Language.objects.create(name='Italian', language_code='it')
    Language.objects.create(name='Japanese', language_code='ja')
    Language.objects.create(name='Javanese', language_code='jv')
    Language.objects.create(name='Kannada', language_code='kn')
    Language.objects.create(name='Kazakh', language_code='kk')
    Language.objects.create(name='Khmer', language_code='km')
    Language.objects.create(name='Kirghiz', language_code='ky')
    Language.objects.create(name='Korean', language_code='ko')
    Language.objects.create(name='Lao', language_code='lo')
    Language.objects.create(name='Latin', language_code='la')
    Language.objects.create(name='Latvian', language_code='lv')
    Language.objects.create(name='Lithuanian', language_code='lt')
    Language.objects.create(name='Luxembourg', language_code='lb')
    Language.objects.create(name='Macedonian', language_code='mk')
    Language.objects.create(name='Malagasy', language_code='mg')
    Language.objects.create(name='Malay', language_code='ms')
    Language.objects.create(name='Malayalam', language_code='ml')
    Language.objects.create(name='Maltese', language_code='mt')
    Language.objects.create(name='Maori', language_code='mi')
    Language.objects.create(name='Marathi', language_code='mr')
    Language.objects.create(name='Mari', language_code='mhr')
    Language.objects.create(name='Mari', language_code='mrj')
    Language.objects.create(name='Mongolian', language_code='mn')
    Language.objects.create(name='Nepali', language_code='ne')
    Language.objects.create(name='Norwegian', language_code='no')
    Language.objects.create(name='Papiamento', language_code='pap')
    Language.objects.create(name='Persian', language_code='fa')
    Language.objects.create(name='Polish', language_code='pl')
    Language.objects.create(name='Portuguese', language_code='pt')
    Language.objects.create(name='Punjabi', language_code='pa')
    Language.objects.create(name='Romanian', language_code='ro')
    Language.objects.create(name='Russian', language_code='ru')
    Language.objects.create(name='Scottish', language_code='gd')
    Language.objects.create(name='Serbian', language_code='SK')
    Language.objects.create(name='Sinhala', language_code='si')
    Language.objects.create(name='Slovak', language_code='sk')
    Language.objects.create(name='Slovenian', language_code='sl')
    Language.objects.create(name='Spanish', language_code='es')
    Language.objects.create(name='Sundanese', language_code='su')
    Language.objects.create(name='Swahili', language_code='sw')
    Language.objects.create(name='Swedish', language_code='sv')
    Language.objects.create(name='Tagalog', language_code='tl')
    Language.objects.create(name='Tajik', language_code='tg')
    Language.objects.create(name='Tamil', language_code='ta')
    Language.objects.create(name='Tatar', language_code='tt')
    Language.objects.create(name='Telugu', language_code='te')
    Language.objects.create(name='Thai', language_code='th')
    Language.objects.create(name='Turkish', language_code='tr')
    Language.objects.create(name='Udmurt', language_code='udm')
    Language.objects.create(name='Ukrainian', language_code='uk')
    Language.objects.create(name='Urdu', language_code='ur')
    Language.objects.create(name='Uzbek', language_code='uz')
    Language.objects.create(name='Vietnamese', language_code='vi')
    Language.objects.create(name='Welsh', language_code='cy')
    Language.objects.create(name='Xhosa', language_code='xh')
    Language.objects.create(name='Yiddish', language_code='yi')


def init_author():
    author = Author.objects.create(
        date_of_birth=datetime.datetime.strptime('01.01.2001', '%d.%m.%Y'),
        date_of_death=datetime.datetime.strptime('01.01.2021', '%d.%m.%Y'),
        first_name="Test",
        last_name="Author"
    )
    return author


def init_genre():
    genre = Genre.objects.create(
        name='Test genre',
    )
    return genre


def init_user_settings(user):
    UserSettings.objects.all().delete()
    us = UserSettings.objects.create(user=user)
    us.default_translation_language = Language.objects.filter(name='Russian').first()
    us.save()
    return us


def get_first(of_class, with_prop, prop_value):
    try:
        return of_class.objects.filter(**{with_prop: prop_value}).first()
    except ObjectDoesNotExist:
        pass


def user_settings(user):
    return get_first(UserSettings, 'user', user)


def init(delete_all):
    user = User.objects.get(pk=1)
    if not user_settings(user):
        init_user_settings(user)

    if delete_all:
        Author.objects.all().delete()
        Language.objects.all().delete()
        Book.objects.all().delete()
        Genre.objects.all().delete()
        init_langs()

    if Author.objects.count() == 0:
        author = init_author()
    else:
        author = Author.objects.all().first()

    if Genre.objects.count() == 0:
        genre = init_genre()
    else:
        genre = Genre.objects.all().first()

    if Book.objects.all().count() == 0:
        book = Book.objects.create(
            title='My test book',
            author=author,
            summary='test summary',
            text="This project will help you to learn a new language without any textbooks or dictionaries. " +
                 "It automates the process of learning a language, ridding you of all the overhead mechanical " +
                 "work needed in the process. The main problem when learning a new language is you don't " +
                 "understand it, and you can't learn something you don't understand. On the other hand, " +
                 "understanding something is all you really need to learn it. This project helps you solve " +
                 "this problem by providing you with a tool to translate books sentence-by-sentence. " +
                 "As the most natural way of learning a language is through hearing, the resulting translation " +
                 "is voiced along with the source text to an mp3 file. The resulting file is served with subtitles " +
                 "to help your utilise your vision as well as your hearing. Subtitles in the form of lrc-files " +
                 "can be played by a number of music-playing pieces of software, available for free " +
                 "(check out lrc wiki-page)."
        )
        book.save()  # need to save to satisfy Non-null requirement
        book.genre.set((genre,))
    else:
        book = Book.objects.all().first()
        print(Book.objects.all().count())
        book.save()

    book.text_with_translation, translate, book.translation_problems, result_file_path = \
        translate_book(book, user, True)
    book.save()
    return book.text_with_translation, translate, book.translation_problems


from gtts import gTTS
import os
from django.conf import settings
import shutil


def get_yandex_translate():
    from yandex_translate import YandexTranslate
    return YandexTranslate(
        'trnsl.1.1.20181030T164747Z.50350640be185f5d.a9c2d0892171111c7027edd85669141908d3301a')


def translate_text(text: str, translate_directions: str, translate) -> str:
    if not translate:
        translate = get_yandex_translate()
    return translate.translate(text, translate_directions)


def detect_language(text: str, translate) -> str:
    if not translate:
        translate = get_yandex_translate()
    return translate.detect(text)


def translate_by_sentences(text: str, from_lang: str, to_lang: str, voice_path: str = '', voice_extension='mp3',
                           translate=None, book=None):
    if not translate:
        translate = get_yandex_translate()
    sentences = split_text_by_sentences(text)
    if sentences:
        text_with_translation = ''
        translation_problems = ''
        translate_directions = f'{from_lang}-{to_lang}'
        sentence_i = 0

        for sentence in sentences:
            sentence_i += 1
            if voice_path:
                file_base_name = f'{sentence_i:06}'
                f_src_path = os.path.join(voice_path, file_base_name + '_02_src.' + voice_extension)
                os.makedirs(voice_path, exist_ok=True)
                f_trg_path = os.path.join(voice_path, file_base_name + '_01_trg.' + voice_extension)
                tts = gTTS(text=sentence, lang=from_lang, slow=True)
                tts.save(f_src_path)

            translation_result = translate_text(sentence, translate_directions, translate)
            sentence_translated = translation_result['text'][0]
            if translation_result['code'] != 200:
                translation_problems = '\n'.join([translation_problems, translation_result['code']])
                translation_problems = '\n'.join([translation_problems, sentence])
                translation_problems = '\n'.join([translation_problems, sentence_translated])
            text_with_translation = '\n'.join([text_with_translation, sentence_translated])
            text_with_translation = '\n'.join([text_with_translation, sentence, ''])
            if voice_path:
                tts = gTTS(text=sentence_translated, lang=to_lang, slow=False)
                tts.save(f_trg_path)
            if book:
                book.text_with_translation = text_with_translation
                book.save()
        return text_with_translation, translation_problems


def translate_book(book, user, set_book_langs_if_none: bool):
    translate = None
    if not book.source_language:
        from_lang = detect_language(book.text, translate)
        if set_book_langs_if_none:
            book.source_language = Language.objects.filter(language_code=from_lang).first()
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
    else:
        to_lang = book.translation_language.language_code

    # print('Languages:', translate.langs)
    # print('Translate directions:', translate.directions)
    # print('Detect language:', translate.detect('Привет, мир!'))
    # print('Translate:', translate.translate('Привет, мир!', 'ru-en'))  # or just 'en'

    book_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'catalog', 'book', str(book.id))
    split_path = os.path.join(book_path, 'split')
    extension = 'mp3'
    text_with_translation, translation_problems = translate_by_sentences(
        book.text, from_lang, to_lang, split_path, extension, translate, book)
    if text_with_translation:
        result_file_path = join_sound_files(split_path, os.path.join(book_path, 'joint'), book.title, extension, False)
        return text_with_translation, translate, translation_problems, result_file_path


def join_sound_files(src_fld, trg_fld, result_file_name, extension, use_pydub):
    result_file_path = os.path.join(trg_fld, result_file_name + "." + extension)
    if use_pydub:
        # has some system dependencies (check out pydub gihub page)
        from pydub import AudioSegment

        result_file = None
        for f in os.listdir(src_fld):
            # f_full = os.path.abspath(os.path.join(src_fld, f))
            f_full = os.path.join(src_fld, f)
            if f.endswith(extension):
                if result_file:
                    result_file = result_file + AudioSegment.from_wav(f_full)
                else:
                    result_file = AudioSegment.from_wav(f_full)

        # writing mp3 files is a one liner
        if result_file:
            os.makedirs(trg_fld, exist_ok=True)
            result_file.export(os.path.join(trg_fld, result_file_name))  #, format="mp3")
    else:
        if not os.path.isdir(trg_fld):
            os.makedirs(trg_fld, exist_ok=True)
        # run system command to concatenate files. mac OS is supposed,
        # edit code to run on Windows (e. g. "copy" instead of cat, but not tested)
        # e.g.: cat *.mp3 > ../join/join.mp3
        command = f'cat "{os.path.join(src_fld, "*." + extension)}" > '
        command += f'"{os.path.join(trg_fld, result_file_name + "." + extension)}"'
        resp = os.system(command)
        if resp != 0:  # failed, try Windows batch command
            command = f'copy /b "{os.path.join(src_fld, "*." + extension)}" '
            command += f'"{os.path.join(trg_fld, result_file_name + "." + extension)}"'
            resp = os.system(command)
        if resp != 0:
            print(f'Failed to execute "{command}"')

    if os.path.isfile(result_file_path):
        if settings.MEDIA_ROOT in result_file_path:
            root = os.path.join(settings.MEDIA_ROOT, '')  # append trailing slash if not there
            result_file_path = result_file_path[len(root):]
        return result_file_path


def split_text_by_sentences_re(text):
    import re
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences


def split_text_by_sentences(text):
    import nltk.data
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # print('\n-----\n'.join(tokenizer.tokenize(text)))
    return tokenizer.tokenize(text)

# import catalog.init_db
# from importlib import reload
# from catalog.init_db import *
# reload(catalog.init_db).init(True)


# reload(catalog.init_db).split_text()
# text_with_translation, translate, translation_problems, result_file_path = reload(catalog.init_db).init(True)

