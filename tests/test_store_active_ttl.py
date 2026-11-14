import asyncio
import time
import unittest
from pyredis.store import DataStore

class TestStoreActiveTTL(unittest.TestCase):
    def test_purge_expired_probabilistic(self):
        store = DataStore()
        now = time.time()
        # Insert 50 keys, 30 of which are already expired
        for i in range(20):
            store.set(f"alive:{i}", "val", ex_sec=100)
        for i in range(30):
            store.set(f"expired:{i}", "val", ex_sec=100)
            # Force timestamp to the past
            store._expires[f"expired:{i}"] = now - 10.0

        purged = store.purge_expired(sample_size=20, threshold=0.25)
        self.assertGreaterEqual(purged, 1)

        # Check that remaining expired keys can be fully purged
        store.purge_expired(sample_size=50, threshold=0.0)
        for i in range(30):
            self.assertNotIn(f"expired:{i}", store._data)
            self.assertNotIn(f"expired:{i}", store._expires)

        # Alive keys remain intact
        for i in range(20):
            self.assertEqual(store.get(f"alive:{i}"), "val")

    def test_async_active_sweep_background_task(self):
        async def run_async_test():
            store = DataStore()
            now = time.time()
            for i in range(15):
                store.set(f"auto_exp:{i}", "val", ex_sec=100)
                store._expires[f"auto_exp:{i}"] = now - 5.0

            # Start active background expiration loop with 0.02s interval
            task = store.start_active_expiration(interval_sec=0.02)
            await asyncio.sleep(0.08)
            store.stop_active_expiration()

            # Confirm background sweep evicted the expired keys without direct access
            remaining = [k for k in store._data if k.startswith("auto_exp:")]
            self.assertEqual(len(remaining), 0)

        asyncio.run(run_async_test())

if __name__ == "__main__":
    unittest.main()
