from django.test import TestCase
from django.urls import reverse


class PublicWebsitePageTests(TestCase):
    def test_public_pages_load_successfully(self):
        page_names = [
            "website:home",
            "website:new_here",
            "website:about",
            "website:schedule",
            "website:ministries",
            "website:events",
            "website:sermons",
            "website:sacraments",
            "website:contact",
            "website:livestream",
            "website:give",
        ]

        for page_name in page_names:
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)