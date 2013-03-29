"""
Given a flickr set id, get those photos and create
proxy tiddlers for the original, medium, small and thumb
sized photos in a specified tiddlyweb hosted bag.
"""

from __future__ import print_function

import json
import sys
import requests
import urllib

from docopt import docopt
from calendar import timegm
from time import strptime

HELP = """Usage: flicktid [-vh] --user=<user> --pass=<pass> <setid> <bag-uri>

-h, --help              Show this help.
-v, --verbose           Verbosely report web interactions.

flicktid is used to create tiddlers at bag-uri which map to the
photos in a flickr set identified by setid.

"""

URL_FIELDS = ['url_t', 'url_s', 'url_m', 'url_o']
EXTRAS = URL_FIELDS + ['date_upload', 'date_taken', 'tags']
API_KEY = "f9af7135045d17357d881e9a123cf3cd"

SET_URI = "http://api.flickr.com/services/rest/?method=flickr.photosets.getPhotos&api_key=%s&photoset_id=%s&extras=%s&format=json&nojsoncallback=1"


def get_set(options):
    """
    Get the flickr set data.
    """
    verbose = options['--verbose']
    set_request_uri = SET_URI % (API_KEY, options['<setid>'],
            '%2c'.join(EXTRAS))
    if verbose:
        print('GET', set_request_uri, file=sys.stderr)
    response = requests.get(set_request_uri)
    data = response.json()
    photos = data['photoset']['photo']
    for photo in photos:
        if verbose:
            print('Handling photo', photo['id'], file=sys.stderr)
        for url_type in URL_FIELDS:
            put_tiddler(options, url_type, photo)


def put_tiddler(options, url_type, photo):
    """
    Put a canonical_url based tiddler of url_type to the target bag.
    """
    user = options['--user']
    password = options['--pass']
    verbose = options['--verbose']
    target_url = options['<bag-uri>']
    photo_url = photo[url_type]

    tags = photo['tags'].split(' ')
    date_taken = to_epoch(photo['datetaken']) # YYYY-MM-DD HH:MM:SS
    date_uploaded = photo['dateupload'] # epoch

    # use the title on the photo if it exists
    # XXX: this might be a bad thing because of collisions
    title = photo['title']
    if not title:
        title = photo['id']

    suffix = url_type.split('_', 1)[1]
    json_data = {'fields': {
        '_canonical_uri': photo_url,
        'datetaken': date_taken,
        'dateupload': date_uploaded
        },
        'tags': tags}

    target_url = target_url + '/' + encode_name(title) + '_%s' % suffix
    if verbose:
        print('PUT', target_url, file=sys.stderr)
    response = requests.put(target_url,
            headers={'Content-type': 'application/json'},
            data=json.dumps(json_data),
            auth=(user, password))
    status = response.status_code
    if status != 204:
        print(response.status_code, file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)


def to_epoch(datestring):
    """
    Turn a datestring into an epoch time.
    """
    time_struct =strptime('2013-03-23 16:56:34', '%Y-%m-%d %H:%M:%S')
    return timegm(time_struct)


def encode_name(name):
    """
    Make a photo title safe for uris.
    """
    return urllib.quote(name.encode('utf-8'), safe='')


def run():
    """
    Get the options and start the process.

    We use the options as a sort of GOD object throughout.
    """
    get_set(docopt(HELP))
