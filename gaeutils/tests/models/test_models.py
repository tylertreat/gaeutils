import datetime
import time
import unittest

from google.appengine.ext import ndb

from mock import Mock

from gaeutils import models


class Foo(ndb.Model):
    string = ndb.StringProperty()
    dt = ndb.DateTimeProperty()
    geopt = ndb.GeoPtProperty()
    blobkey = ndb.BlobKeyProperty()
    ndbkey = ndb.KeyProperty()


class TestToDict(unittest.TestCase):

    def test_none_value(self):
        """Verify None values are handled correctly."""

        actual = models.to_dict(Foo())

        self.assertIsNone(actual['string'])

    def test_builtin_value(self):
        """Verify builtin types are handled correctly."""

        expected = 'foo'

        actual = models.to_dict(Foo(string=expected))

        self.assertEqual(expected, actual['string'])

    def test_datetime_value(self):
        """Verify datetime values are handled correctly."""

        expected = datetime.datetime(2013, 12, 29)

        actual = models.to_dict(Foo(dt=expected))

        expected = time.mktime(
            expected.timetuple()) * 1000 + expected.microsecond / 1000
        self.assertEqual(expected, actual['dt'])

    def test_geopt_value(self):
        """Verify GeoPt values are handled correctly."""

        expected = ndb.GeoPt(45.1234, -93.4947)

        actual = models.to_dict(Foo(geopt=expected))

        self.assertEqual({'lat': expected.lat, 'lon': expected.lon},
                         actual['geopt'])

    def test_blobkey_value(self):
        """Verify BlobKey values are handled correctly."""
        from google.appengine.ext import blobstore

        expected = 'abc'

        actual = models.to_dict(Foo(blobkey=blobstore.BlobKey(expected)))

        self.assertEqual(expected, actual['blobkey'])

    def test_key_value(self):
        """Verify db.Key values are handled correctly."""

        expected = 'abc'
        ndb_key = Mock(spec=ndb.Key)
        ndb_key.urlsafe.return_value = expected

        actual = models.to_dict(Foo(ndbkey=ndb_key))

        self.assertEqual(expected, actual['ndbkey'])

