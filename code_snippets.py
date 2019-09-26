from django.conf import settings
from os import path
import os
from mutagen.mp3 import MP3
import datetime
import nltk.data


def split_text():
    from catalog.models import Book
    book = Book.objects.all().first()
    # book = Book.objects.filter(pk=).first()
    text = book.text_with_translation
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    result = tokenizer.tokenize(text)
    # print('\n-----\n'.join(tokenizer.tokenize(text)))
    return book, result


def make_lrc_dict():
    book, sentences = split_text()
    split_fld = path.join(settings.MEDIA_ROOT, 'catalog', 'book', str(book.id), 'split')

    start = 0
    i = 0
    result = {'lrc': {}, 'files': {}}
    lrc_it = {}
    for filename in os.listdir(split_fld):
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
            files_it[mm_ss_fffffff] = f'{i+1:06}'
            start += duration_sec
            i += 1

    return result, book

import shutil
import glob

def make_lrc_files():
    lrc_files_dict, book = make_lrc_dict()
    lrc_dict = lrc_files_dict['lrc']
    files_dict = lrc_files_dict['files']
    split_fld = path.join(settings.MEDIA_ROOT, 'catalog', 'book', str(book.id), 'split')
    join_fld = path.join(settings.MEDIA_ROOT, 'catalog', 'book', str(book.id), 'join')
    for hour in lrc_dict:
        hour_fld = os.path.join(split_fld, hour)
        os.makedirs(hour_fld, exist_ok=True)
        for file_prefix in files_dict:
            for file in glob.glob(os.path.join(split_fld, file_prefix + '*.mp3')):
                shutil.copy(file, hour_fld)
        merge_path = os.path.join(join_fld, hour)
        os.makedirs(join_fld, exist_ok=True)
        sys_merge_mp3 = f'cat {os.path.join(hour_fld, "*.mp3")} > {merge_path}.mp3'
        os.system(sys_merge_mp3)
        shutil.rmtree(hour_fld)
        lrc_text = '\n'.join([f'[{time}] {line}' for time, line in lrc_dict[hour].items()])
        with open(f'{merge_path}.lrc', "w") as text_file:
            text_file.write(lrc_text)

    # print(str(start))
    # print(str(MP3(path.join(settings.MEDIA_ROOT, 'catalog', 'book', str(book.id), 'joint', 'Sempé-Goscinny.mp3')).info.length))

# from importlib import reload
# import code_snippets
# from code_snippets import split_text
# reload(code_snippets).split_text()
# from code_snippets import *
