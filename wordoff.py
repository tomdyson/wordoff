# remove cruft that has been added through pasting from word
# into a wysiwyg editor

import re
import unicodedata

match_tags_with_attributes = re.compile(r'<([a-zA-Z]+[0-9]?) ([^/>]*)(/?)>')
match_spans = re.compile(r'</?span[^>]*>')
match_divs = re.compile(r'</?div[^>]*>')
match_empty_elements = re.compile(r'<([a-zA-Z]+)>\s*</\1>')
match_multiple_linebreaks = re.compile(r'(\n\s*){3,}')
match_word_namespaced_elements = re.compile(r'<([wo]:[a-zA-Z]+)( [^>]+)?>.*</\1>', re.DOTALL)
match_empty_word_namespaced_elements = re.compile(r'<([wo]:[a-zA-Z]+)( [^>]+)?/>')
match_style_attributes = re.compile(r'\s*style\s*=\s*[\'"][^\'"]+[\'"]\s*')

def ignore_some_tags(matchobj):
    # only strip style attributes for <a>s or <img>s
    if matchobj.group(1) in ['a', 'img']:
        return match_style_attributes.sub(' ', matchobj.group(0))
    # but strip all attibrutes for everything else
    else:
        if matchobj.group(3): # preserve trailing slashes for void elements
            return '<%s />' % matchobj.group(1)
        return '<%s>' % matchobj.group(1)


def stripAttributes(str):
    # remove attributes from all tags
    return match_tags_with_attributes.sub(ignore_some_tags, str)


def stripSpans(str):
    # remove spans
    return match_spans.sub('', str)


def stripDivs(str):
    # remove divs
    return match_divs.sub('', str)


def reduceLineBreaks(str):
    # reduce >2 line breaks into two
    return match_multiple_linebreaks.sub('\n\n', str)


def stripEmptyElements(str):
    # remove elements which contain nothing or whitespace
    return match_empty_elements.sub('', str)


def strip_word_namespaced_elements(str):
    # remove elements which are w: namespaced
    str = match_word_namespaced_elements.sub('', str)
    return match_empty_word_namespaced_elements.sub('', str)


def xenophobia(str):
    # convert everything to ascii
    utf8_string = str.decode('utf-8')
    return unicodedata.normalize('NFKD', utf8_string).encode('ascii', 'ignore')


def superClean(str):
    clean = stripAttributes(str)
    cleaner = stripSpans(clean)
    cleaner = stripDivs(cleaner)
    cleaner = strip_word_namespaced_elements(cleaner)
    #cleaner = xenophobia(cleaner)
    cleaner = stripEmptyElements(cleaner)
    cleaner = stripEmptyElements(cleaner)
    cleaner = stripEmptyElements(cleaner)
    cleaner = reduceLineBreaks(cleaner)
    return cleaner
