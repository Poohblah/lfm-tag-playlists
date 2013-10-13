# the ITunesLibrary class
#
# encapsulates methods for reading data from an iTunes library in
# Apple pList XML format and writing playlists to disk in the same
# format.

# includes

import plistlib

# global variables

library_file = '/Users/jay/Music/iTunes/iTunes Music Library.xml'
playlist_file = 'lfmplaylists.xml'

# the Library class

class ITunesLibrary:
    def __init__(self, l_file=library_file):
        self.plist = plistlib.readPlist(l_file) 
        self.stripExistingPlaylists()

    def stripExistingPlaylists(self):
        '''
        Removes existing playlists from the library
        to prevent duplicates when importing.
        '''
        self.plist['Playlists'] = []

    def addPlaylist(self, name, playlist):
        '''
        given a name and an array of dictionaries in the format:
            { 'Track ID' : trackid }
        , adds a playlist by that name to the library.
        '''
	# TODO: create a Playlist class and have this method take
	# objects of that class instead.
        self.plist['Playlists'].append({
            'Name'           : name,
            'Playlist Items' : playlist
            })

    def writeLibrary(self, filename=playlist_file):
        '''
	writes the library, including any new playlists, to a file.
	the name of the file defaults to the value of the playlist_file
	variable.
        '''
        plistlib.writePlist(self.plist, filename)
