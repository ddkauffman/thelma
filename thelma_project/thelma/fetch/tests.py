from django.test import TestCase


class TestFetch(TestCase):

    def test_smoke_test(self):

        self.assertEqual(1, 1)

    def test_fetch_template_is_used(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'fetch/index.html')
