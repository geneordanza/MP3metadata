#!/usr/bin/python
#
# Author: Gene Ordanza <gene.ordanza@gmail.com>
# Description: Ugly hack on how to pull the metadata out of mp3 file that uses
#        the ID3v1 TAG formatting scheme.
# Usage: ./mp3meta.py
# Note : A great reference on how to pull ID3v1 data from mp3 file can be found
#        on Dive into Python (chap 5-6).
#        Also, mp3 file that uses non-ID3v1 TAG formatting will be skip.

from optparse import OptionParser
import sys, os

def display(mp3ObjecList):
    line_width = 80
    field_data = '%-5s%-24s%-24s%-23s%-4s'
    f1, f2, f3, f4, f5 = ('No.', 'Title', 'Artist', 'Album', 'Year')

    print '%47s' % 'MP3 File Metadata\n'
    print '=' * line_width
    print field_data % (f1, f2, f3, f4, f5)
    print '-' * line_width

    for mp3file in mp3ObjecList:
        print field_data % (mp3file['count'],  mp3file['Title'],
                            mp3file['Artist'], mp3file['Album'],
                            mp3file['Year'])

def stripnulls(data):
    string = data.replace('\00', '').strip()
    return string[:23]

class MP3Meta(dict):
    count = 0
    def __init__(self, name):
        self['name'] = name
        self.__class__.count += 1
        self['count'] = MP3Meta.count

    metaData = {
        'Title' : (3, 33, stripnulls),
        'Artist': (33, 63, stripnulls),
        'Album' : (63, 93, stripnulls),
        'Year'  : (93, 97, stripnulls),
        'Comment': (97, 126, stripnulls),
        'Genre' : (127, 128, ord),
        }

def getMetaData(mp3files):
    mp3ObjecList = []
    for file in mp3files:
        mp3file = MP3Meta(file)
        with open(file, 'rb') as fp:
            fp.seek(-128, 2)
            mp3data = fp.read(128)
            if mp3data[:3] == 'TAG':
                for tag, (start, end, cleanup) in mp3file.metaData.items():
                    mp3file[tag] = cleanup(mp3data[start:end])
                mp3ObjecList.append(mp3file)

    display(mp3ObjecList)

def findMP3():
    extension = '.mp3'
    mp3files = [file for file in os.listdir('.') if file.endswith(extension)]

    getMetaData(mp3files)

def main():
    parser = OptionParser(description="Extract metadata from mp3 files.",
                          usage="./%prog",
                          version="%prog 0.1")

    (options, args) = parser.parse_args()

    try:
        findMP3()
    except Exception, e:
        #print >> sys.stderr, "error ...", e
        parser.print_help()
        sys.exit(1)

if  __name__ == '__main__':
    main()
