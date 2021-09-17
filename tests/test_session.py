import os
import sys
import unittest
from threading import Thread

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ovos_skills_manager.session import *


class TestCachedSession(unittest.TestCase):
    def test_cached_request(self):
        resp = SESSION.get("https://openvoiceos.com/")
        self.assertFalse(resp.from_cache)
        self.assertFalse(resp.is_expired)

        cached = SESSION.get("https://openvoiceos.com/")
        self.assertTrue(cached.from_cache)
        self.assertFalse(cached.is_expired)

    def test_cached_request_case_sensitive(self):
        SESSION.get("https://openvoiceos.com/")

        cached = SESSION.get("https://OpenVoiceOS.com/")
        self.assertTrue(cached.from_cache)
        self.assertFalse(cached.is_expired)

    def test_threaded_cached_requests(self):
        SESSION.get("https://openvoiceos.com/")
        responses = dict()

        def get_cached_response(idx):
            responses[idx] = SESSION.get("https://openvoiceos.com/").from_cache

        for i in range(8):
            t = Thread(target=get_cached_response, args=(i,), daemon=True)
            t.start()
            t.join()
            self.assertTrue(responses[i])


if __name__ == '__main__':
    unittest.main()
