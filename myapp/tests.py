from django.test import TestCase

class TestOriginal(TestCase):
    def test_plus(self):
        self.assertEqual(2, 1 + 1)