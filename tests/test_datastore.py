from snr import *
from snr.core.datastore import Datastore
from snr.core.utils.timer import Timer


class TestDatastore(SNRTestCase):
    def test_datastore(self):
        expectations = {}
        with self.expector(expectations) as expector:
            datastore: DatastoreProtocol = Datastore(self.root_context,
                                                     expector.call,
                                                     Timer())

            datastore.synchronous_store(Page("key", "data", "origin",
                                             0.0, process=True))
            page = datastore.get_page("key")
            self.assertPage(page, "key", "data", "origin", 0.0, process=True)
            self.assertEqual("data", datastore.get_data("key"))
            self.assertIsNone(datastore.get_data("invalid_key"))
            self.assertIsNone(datastore.get_page("invalid_key"))


if __name__ == '__main__':
    unittest.main()
