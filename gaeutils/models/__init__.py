import datetime
import json
import logging
import time

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import ndb


BUILTIN_TYPES = (int, long, float, bool, dict, basestring, list)


class SerializableMixin(object):

    def to_dict_(self, includes=None, excludes=None):
        """Convert an ndb or db entity to a JSON-serializable dict."""

        output = {}

        if self.key:
            output['id'] = self.key.id()
            output['key'] = self.key.urlsafe()

        for key, prop in self._properties.iteritems():
            value = getattr(self, key)

            if value is None or isinstance(value, BUILTIN_TYPES):
                output[key] = value
            elif isinstance(value, datetime.date):
                # Convert date/datetime to unix timestamp.
                output[key] = time.mktime(value.utctimetuple())
            elif isinstance(value, (db.GeoPt, ndb.GeoPt)):
                output[key] = {'lat': value.lat, 'lon': value.lon}
            elif isinstance(value, blobstore.BlobKey):
                output[key] = str(value)
            elif isinstance(value, (db.Key, ndb.Key)):
                output[key] = value.id()
            elif isinstance(value, (db.Model, ndb.Model)):
                output[key] = self.to_dict(value)
            else:
                raise ValueError('Cannot encode %s' % repr(prop))

        if includes:
            for inc in includes:
                attr = getattr(self, inc, None)
                if attr is None:
                    cls = self.__class__
                    logging.warn('Cannot encode %s' % cls)
                    continue
                if callable(attr):
                    output[inc] = attr()
                else:
                    output[inc] = attr

        if excludes:
            [output.pop(exc) for exc in excludes if exc in output]

        return output


class EntityEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return time.mktime(obj.utctimetuple())

        elif isinstance(obj, ndb.Model):
            return obj.to_dict()

        else:
            return json.JSONEncoder.default(self, obj)

