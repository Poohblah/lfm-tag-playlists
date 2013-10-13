#!/usr/bin/env python

import plistlib
import xml.etree.ElementTree as ET
import urllib
import LastFMFetcher as fetcher
import ITunesLibrary as ilibrary

# global variables

print 'creating a fetcher...'
f = fetcher.LastFMFetcher()
print 'reading the itunes library...'
ilib = ilibrary.ITunesLibrary()

# functions for getting artist and track info from iTunes library

def getArtistList():
    '''
    returns a dict where each key is an artist and
    the value is a list of tracks by that artist.
    '''
    print 'creating artist list...'
    result = {}
    # p = plistlib.readPlist(ITUNES_LIBRARY)
    p = ilib.plist
    tracks = p['Tracks']
    for t in tracks:
        artist = tracks[t].get('Artist')
        if not artist:
            continue
        ad = result.get(artist)
        if not ad:
            result[artist] = {}
            ad = result.get(artist)
        result[artist][t] = tracks[t]
    return result

# functions for retrieving tag info from last.fm

def makePlaylists():
    '''
    returns a dict where each key is a tag name
    and the value is the songs that have that tag.
    '''
    print 'fetching tags...'
    artists = getArtistList()
    result = {}
    for a in artists:
        print a
        tags = f.fetchArtistTags(a)
        print tags
        for t in tags:
            td = result.get(t)
            if not td:
                result[t] = {}
                td = result.get(t)
            for track in artists[a]:
                td[track] = artists[a][track]
        print ''
    print 'saving cache...'
    f.dumpCache()
    return result

# begin our main function
if __name__ == '__main__':
    pls = makePlaylists()
    print 'making playlists...'
    result = []
    for tag in pls:
        artists = []
        for t in pls[tag]:
            track = pls[tag][t]
            artist = track.get('Artist')
            if artist and artist not in artists:
                artists.append(artist)
        if len(artists) > 1:
            result.append([tag, artists])
    result.sort(key=lambda x:len(x[1]), reverse=True)
    result = result[:len(result)/2]
    for tag, artist in result:
        playlist = []
        for trackid in pls[tag]:
            trackid = int(trackid)
            playlist.append({'Track ID': trackid})
        ilib.addPlaylist('LFM ' + tag, playlist)
    print 'writing playlist to disk...'
    ilib.writeLibrary()
            
    # for t, l in result:
    #     print t
    #     print l
    #     print ''
