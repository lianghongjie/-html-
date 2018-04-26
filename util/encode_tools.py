# -*- encoding: utf-8 -*-

import chardet
import six


def code_to_unicode(text):
    try:
        if not isinstance(text, six.text_type):
            text = text.decode(chardet.detect(text).get('encoding'))
    except TypeError:
        pass
    return text

