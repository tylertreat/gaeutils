import datetime
import time

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import ndb

BUILTIN_TYPES = (int, long, float, bool, dict, basestring, list)


def to_dict(model):
    """Convert an ndb or db entity to a JSON-encodable dict."""

    output = {}

    for key, prop in model._properties.iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, BUILTIN_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to milliseconds-since-epoch
            ms = time.mktime(value.utctimetuple()) * 1000
            ms += getattr(value, 'microseconds', 0) / 1000
            output[key] = int(ms)
        elif isinstance(value, (db.GeoPt, ndb.GeoPt)):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, blobstore.BlobKey):
            output[key] = str(value)
        elif isinstance(value, db.Key):
            output[key] = str(value)
        elif isinstance(value, ndb.Key):
            output[key] = value.urlsafe()
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output

