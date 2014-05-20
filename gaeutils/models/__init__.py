import calendar
import datetime
import json
import logging
import time

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import ndb


BUILTIN_TYPES = (int, long, float, bool, dict, basestring, list)


class SerializableMixin(object):

    def to_json_dict(self, includes=None, excludes=None):
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
            elif isinstance(value, SerializableMixin):
                output[key] = value.to_json_dict()
            elif isinstance(value, (db.Model, ndb.Model)):
                output[key] = value.to_dict()
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
            return calendar.timegm(obj.utctimetuple())

        elif isinstance(obj, SerializableMixin):
            return obj.to_json_dict()

        elif isinstance(obj, (db.Model, ndb.Model)):
            return obj.to_dict()

        else:
            return json.JSONEncoder.default(self, obj)

