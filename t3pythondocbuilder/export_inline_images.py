# make_inline_images_external.py
# mb, 2012-05-20, 2016-01-29
# This script has been placed in the public domain.
# No warrenties whatsoever. Use at your own risk.

import codecs
import sys
import os
import re
import base64
from constants import *

# parse:
# .. |img-3|      image:: data:image/png;base64,iVBORw0KGgo

inline_image_re = re.compile(
    '^(?P<part1>\.\. \|)'
    '(?P<file_stem>.+?)'
    '(?P<part3>\|\s+image::\s+data:image/)'
    '(?P<file_extension>.+?)'
    ';'
    '(?P<coding>.+?)'
    ','
    '(?P<b64data>.*)'
    '\s$')

# part1           .. |
# file_stem       img-1
# file_extension  png
# coding          base64
# part3           | image:: data:image/
# b64data         iVBORw0KGgoAAA
# part1 + file_stem + part3 + file_extension + ';' + coding + ',' + b64data

NL = '\n'


def write_image(groupdict, destdir):
    f2path = ''
    ok = True
    ok = ok and groupdict['coding'] == 'base64'
    if ok:
        f2name = 'manual_html_%s.%s' % (groupdict['file_stem'], groupdict['file_extension'])
        f2path = os.path.join(destdir, f2name)
        data = base64.b64decode(groupdict['b64data'])
        with file(f2path, 'w') as f2:
            f2.write(data)
    return f2name


def main(f1name, f2name, destdir):
    f1 = codecs.open(f1name, 'r', 'utf-8-sig')
    if f2name != '-':
        f2 = codecs.open(f2name, 'w', 'utf-8-sig')
    else:
        f2 = sys.stdout
    cnt = 0
    line = f1.readline()
    active = False
    while line:
        cnt += 1
        if active:
            M = inline_image_re.match(line)
            if M:
                groupdict = M.groupdict()
                groupdict['relpath'] = write_image(groupdict, destdir)
                if groupdict['relpath']:
                    groupdict['part3left'] = groupdict['part3'].split('image::')[0] + 'image::'
                    line = '%(part1)s%(file_stem)s%(part3left)s %(relpath)s\n' % groupdict
        elif line.startswith(CUTTER_MARK_IMAGES):
            active = True
        f2.write(line)
        line = f1.readline()

    if not f2 == sys.stdout:
        f2.close()
    f1.close()


if __name__ == "__main__":
    ok = len(sys.argv) == 3 or len(sys.argv) == 4
    if ok:
        destdir = sys.argv[1]
        f1path = sys.argv[2]
        if len(sys.argv) == 4:
            f2path = sys.argv[3]
        else:
            f2path = '-'
    ok = ok and os.path.isdir(destdir)
    ok = ok and f1path.endswith('.rst') and os.path.isfile(f1path)
    ok = ok and f1path != f2path
    if not ok:
        print 'usage: python %s <destdir> <infile.utf8.rst> [<outfile.utf8.rst>]' % sys.argv[0]
        print '       Dump inline images as files in path <path>'
        sys.exit(2)

    main(f1path, f2path, destdir)
