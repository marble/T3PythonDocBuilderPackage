# tweak_dllisttables.py
# mb, 2012-05-21, 2013-06-11, 2016-01-30

import codecs
import os
import sys
import re
import prepend_sections_with_labels

ospj = os.path.join
ospe = os.path.exists

from constants import CUTTER_MARK_IMAGES
from constants import SNIPPETS
from constants import SECTION_UNDERLINERS

CURRENT_UNDERLINER = '*'

def tweakTableRow(lines0):
    ok = True

    # make a copy
    lines = [line.rstrip() for line in lines0]

    # check 2, manipulation: insert label and header
    p = SECTION_UNDERLINERS.index(CURRENT_UNDERLINER)
    underliner = SECTION_UNDERLINERS[p+1]

    # remove line '.. container:: table-row'
    del lines[0]

    # make sure all lines with content are indented by 3 at least
    for line in lines:
        if line[:3].strip():
            ok = False
            break

    lines = [line[3:] for line in lines]

    result = []
    # keep only cells with content
    state = 'before cell'
    istart = 0
    hasContent = False
    for i in range(len(lines)):
        line = lines[i]
        if line:
            if line[0] == ' ':
                hasContent = True
            else:
                if hasContent:
                    for ii in range(istart, i):
                        result.append(lines[ii])
                hasContent = False
                istart = i

    # save the last one
    if hasContent:
        for ii in range(istart, len(lines)):
            result.append(lines[ii])

    lines = result
    if ok:
        dt = None
        dd = None
        property = ''
        rowIsMeaningful = False
        for i in range(len(lines)):
            line = lines[i]
            if not line:
                continue
            if line[0] != ' ':
                dt = line
                dd = None
                lines[i] = u':aspect:`%s`\n' % line
            else:
                if not dd is None:
                    # more than one dd line
                    rowIsMeaningful = True
                dd = line.strip()
                if not property:
                    property = dd
            if dt is None and dd is not None:
                ok = False
                break
            if dt and dd and not rowIsMeaningful:
                if dt.rstrip(':') != dd.rstrip(':'):
                    rowIsMeaningful = True

        if not rowIsMeaningful:
            # remove this row
            lines = []
            return lines

        if ok and not property:
            property = '((Unknown Property))'

        if ok and property:
            label = prepend_sections_with_labels.sectionToLabel(property)
            s = (
              '\n'
              '\n'
              '.. _%s:\n'
              '\n'
              '%s\n'
              '%s\n'
              '\n' % (label, property, underliner * len(property))
            )
            lines.insert(0, s)

    if not ok:
        lines = [line.rstrip() for line in lines0]
    return lines



def processRstFile(f1path):
    global CURRENT_UNDERLINER
    withinTable = False
    f2path = f1path + '.temp.txt'
    f1 = codecs.open(f1path, 'r', 'utf-8-sig')
    f2 = codecs.open(f2path, 'w', 'utf-8-sig')
    state = None
    indentLen = 0
    indentStr = ''
    lines = []
    for line in f1:

        if withinTable:

            if beginOfTableIndent > 0:
                line = line[beginOfTableIndent:]

            if state == 'before table-row':
                containerTableRowIndent = line.find(u'.. container:: table-row')
                if containerTableRowIndent < 0:
                    f2.write(line)
                else:
                    state = 'before first cell'
                    lines.append(line)
            elif state == 'before first cell':
                if line.strip():
                    # line has contents
                    state = 'within row'
                lines.append(line)
            elif state == 'within row':
                if not line.strip():
                    # line is white space
                    lines.append(line)
                elif line[0:3] == '   ':
                    # line has content and is still indented
                    lines.append(line)
                else:
                    # line is not indented. Something happens
                    state = 'at end of row'
                    # process collected lines
                    lines = tweakTableRow(lines)
                    # write processed lines
                    for aline in lines:
                        f2.write(aline)
                        f2.write('\n')
                    # empty our linebuffer
                    lines = []
                    # end of table?
                    if line.strip().startswith('.. ###### END~OF~TABLE ######'):
                        withinTable = False
                        f2.write(line)
                    # another row?
                    elif line.strip().startswith('.. container:: table-row'):
                        containerTableRowIndent = line.find(u'.. container:: table-row')
                        state = 'before first cell'
                        lines.append(line)
                    else:
                        # should not happen. Assume end of table
                        withinTable = False
                        f2.write(line)
        else:
            lines.append(line)
            while len(lines) >= 4:
                hot = len(lines[0].strip()) == 0
                hot = hot and (len(lines[1].strip()) != 0)
                hot = hot and (len(lines[2].strip()) != 0)
                hot = hot and (len(lines[3].strip()) == 0)
                hot = hot and (lines[1].rstrip('\r\n') <> (lines[1][0] * len(lines[1].rstrip('\r\n'))))
                hot = hot and (lines[2].rstrip('\r\n') == (lines[2][0] * len(lines[2].rstrip('\r\n'))))
                if hot:
                    CURRENT_UNDERLINER = lines[2][0]
                    del lines[0:3]
                else:
                    del lines[0]

            if line.strip().startswith('.. ### BEGIN~OF~TABLE ###'):
                withinTable = True
                state = 'before table-row'
                beginOfTableIndent = line.find('.. ### BEGIN~OF~TABLE ###')
                lines = []

            f2.write(line)


    while lines:
        # f2.write(lines[0])
        del lines[0]

    if not f2 is sys.stdout:
        f2.close()
    f1.close()

    if 1:
        os.remove(f1path)
        os.rename(f2path, f1path)


def main(startDir):
    for path, dirs, files in os.walk(startDir):
        for fname in files:
            stem, ext = os.path.splitext(fname)
            if ext == '.rst':
                f1path = ospj(path, fname)
                processRstFile(f1path)

if __name__ == "__main__":
    if 1 and "testing at home":
        startDir = r'D:\T3PythonDocBuilder\temp\t3pdb\Documentation'
        main(startDir)
    else:
        print "Please import and run main(...)"
