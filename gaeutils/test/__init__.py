import os
import unittest

from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed

from gaeutils import settings


HRD_CONSISTENCY = 1


class DatastoreTestCase(unittest.TestCase):
    """Test case with stubbed high-replication datastore API. The datastore
    stub uses an optimistic, always-consistent policy, meaning writes will
    always apply.
    """

    def setUp(self):
        super(DatastoreTestCase, self).setUp()

        self.original_environ = dict(os.environ)

        os.environ['TZ'] = 'UTC'

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(app_id=settings.APP_ID)

        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=HRD_CONSISTENCY)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

    def tearDown(self):
        super(DatastoreTestCase, self).tearDown()
        self.testbed.deactivate()

        os.environ = self.original_environ


class MemcacheTestCase(unittest.TestCase):
    """Test case with stubbed memcache API."""

    def setUp(self):
        super(MemcacheTestCase, self).setUp()

        self.original_environ = dict(os.environ)

        os.environ['TZ'] = 'UTC'

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        super(MemcacheTestCase, self).tearDown()
        self.testbed.deactivate()

        os.environ = self.original_environ


class DatastoreMemcacheTestCase(unittest.TestCase):
    """Test case with stubbed datastore and memcache APIs. The datastore
    stub uses an optimistic, always-consistent policy, meaning writes will
    always apply.
    """

    def setUp(self):
        super(DatastoreMemcacheTestCase, self).setUp()

        self.original_environ = dict(os.environ)

        os.environ['TZ'] = 'UTC'

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(app_id=settings.APP_ID)

        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=HRD_CONSISTENCY)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

        self.testbed.init_memcache_stub()

    def tearDown(self):
        super(DatastoreMemcacheTestCase, self).tearDown()
        self.testbed.deactivate()

        os.environ = self.original_environ

