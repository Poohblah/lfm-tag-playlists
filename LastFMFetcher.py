# the LastFMFetcher class
#
# encapsulates methods for retrieving info and tag lists related
# to artists, albums, and songs. TagFetcher queries first hit a local
# cache. if the desired information is not in the cache, or if the
# cache entry is stale, then TagFetcher fetches the information via
# the last.fm API and updates the local cache.

# global variables

# last.fm API
api_key            = '&api_key=c2ee43fd2694da3ec5f7b06a9a27bed8'
base_url           = 'http://ws.audioscrobbler.com/2.0/'
track_tags_method  = '?method=track.gettoptags&artist=%s&track=%s'
album_tags_method  = '?method=album.gettoptags&artist=%s&album=%s'
artist_tags_method = '?method=artist.gettoptags&artist=%s'
track_info_method  = '?method=track.getinfo&artist=%s&track=%s'
album_info_method  = '?method=album.getinfo&artist=%s&album=%s'
artist_info_method = '?method=artist.getinfo&artist=%s'

# local cache
pickle_file        = 'cache.pickle'

# includes
import datetime
import xml.etree.ElementTree as ET
import urllib
import cPickle as pickle

# class definition

class LastFMFetcher:

    def __init__(self):
        self.loadCache()

    # cache methods

    def loadCache(self):
        '''
        populates self.cache and returns True if the cache exists;
        otherwise returns False and initializes self.cache as an
        empty dictionary object.
        '''
        try:
            with open(pickle_file, 'rb') as f:
                self.cache = pickle.load(f)
            return True
        except IOError:
            self.cache = {}
            return False

    def dumpCache(self):
        '''
        writes the cache to disk.
        '''
        with open(pickle_file, 'wb') as f:
            pickle.dump(self.cache, f)

    # fetching methods

    def fetchURL(self, url):
        '''
        given a url to fetch, returns the data as an XML ETree object.
        first checks the cache for the data; if the data is not there
        or the data is stale (over 2 weeks old), then the data is 
        retrieved from the last.fm servers and the cache is updated.
        '''
        now = datetime.datetime.now()
        cached = self.cache.get(url)
        if not cached or (now - cached.get('updated')).days > 14:
            # fetch the data from last.fm and update the cache
            data = ET.fromstring(urllib.urlopen(url+api_key).read())
            self.cache[url] = {
                'data'     : data,
                'updated'  : now
                }
            return data
        else:
            # return the cached data 
            return cached.get('data')

    def fetchArtistTags(self, artist):
        '''
        placeholder method; given an artist, the top 15 tags as a list of strings.
        '''
        artist = urllib.quote_plus(artist.encode('utf-8'))
        url = base_url + artist_tags_method %(artist)
        toptags = self.fetchURL(url).find('toptags')
        result = []
        for i in range(15):
            try:
                result.append(toptags[i].find('name').text)
            except:
                break
        return result
