from unittest import TestCase

class TryTesting(TestCase):
## Un test que siempre pasa y otro que siempre falla hecho con unittest.
    def test_always_passes(self):
        self.assertTrue(True)

    def test_always_fails(self):
        self.assertFalse(True)