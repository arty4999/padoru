from config import YANDEX_TOKEN
from yandex import Translater

tr = Translater()
tr.set_key(YANDEX_TOKEN)


def do_translate(in_text, out_lang, in_lang=""):
    print(in_text, out_lang, in_lang)
    tr.set_text(in_text)
    if in_lang is "":
        tr.set_from_lang(tr.detect_lang())
    else:
        tr.set_from_lang(in_lang)
    tr.set_to_lang(out_lang)
    return tr.translate()


def get_valid_langs():
    return tr.valid_lang
