# remove cruft that has been added through pasting from word
# into a wysiwyg editor

import re
import unicodedata

match_tags_with_attributes = re.compile(r'<([a-zA-Z]+[0-9]?) [^>]+>')
match_spans = re.compile(r'</?span[^>]*>')
match_divs = re.compile(r'</?div[^>]*>')
match_empty_elements = re.compile(r'<([a-zA-Z]+)>\s*</\1>')
match_multiple_linebreaks = re.compile(r'(\n\s*){3,}')

def ignore_some_tags(matchobj):
    # don't strip attributes for <a>s
    if matchobj.group(1) == 'a':
        return matchobj.group(0)
    else:
        return '<%s>' % matchobj.group(1)

def stripAttributes(str):
    # remove attributes from all tags
    return match_tags_with_attributes.sub(ignore_some_tags,str)

def stripSpans(str):
    # remove spans
    return match_spans.sub('',str)
    
def stripDivs(str):
    # remove divs
    return match_divs.sub('',str)
    
def reduceLineBreaks(str):
    # reduce >2 line breaks into two
    return match_multiple_linebreaks.sub('\n\n',str)
        
def stripEmptyElements(str):
    # remove elements which contain nothing or whitespace
    return match_empty_elements.sub('', str)

def xenophobia(str):
    # convert everything to ascii
    utf8_string = str.decode('utf-8')
    return unicodedata.normalize('NFKD', utf8_string).encode('ascii', 'ignore')

def superClean(str):
    clean = stripAttributes(str)
    cleaner = stripSpans(clean)
    cleaner = stripDivs(cleaner)
    #cleaner = xenophobia(cleaner)
    cleaner = stripEmptyElements(cleaner)
    cleaner = stripEmptyElements(cleaner)
    cleaner = stripEmptyElements(cleaner)
    cleaner = reduceLineBreaks(cleaner)
    return cleaner