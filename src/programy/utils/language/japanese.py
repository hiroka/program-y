"""
Copyright (c) 2016-17 Hiroka Koizumi
"""

from programy.utils.logging.ylogger import YLogger
import MeCab
import re
from programy.utils.language.normalization import JapaneseNormalize

class JapaneseLanguage (object):

    @staticmethod
    def is_language(text):

        # Normalize
        #text = JapaneseNormalize.normalize(text)

        # Dictinary or Wakachi
        tagger = MeCab.Tagger("-Owakati")
        #tagger = MeCab.Tagger("-d /usr/lib64/mecab/dic/mecab-ipadic-neologd/ -Owakati")

        text = tagger.parse(text)
        text = re.sub('\n',"",text)

        return text

    @staticmethod
    def split_language(s):
        result = []
        for c in s:
            if JapaneseLanguage.is_language(c):
                result.extend([" ", c, " "])
            else:
                result.append(c)
        ret = ''.join(result)
        return ret.split()

    @staticmethod
    def split_unicode(s):
        segs = s.split()
        result = []
        for seg in segs:
            if any(map(JapaneseLanguage.is_language, seg)):
                result.extend(JapaneseLanguage.split_language(seg))
            else:
                result.append(seg)
        return result

    @staticmethod
    def split_with_spaces(s):
        segs = JapaneseLanguage.split_language(s)
        result = []
        for seg in segs:
            # English marks
            if seg[0] not in ".,?!":
                try:
                    str(seg[0]) and result.append(" ")
                except:
                    pass
            result.append(seg)
            try:
                str(seg[-1]) and result.append(" ")
            except:
                pass
        return ''.join(result).strip()
