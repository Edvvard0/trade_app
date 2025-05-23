from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad


class AdsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="otheruser", password="password")

        self.ad = Ad.objects.create(
            user=self.user,
            title="Test Ad",
            description="This is a test ad",
            category="cars",
            condition="new",
            image_url="http://example.com/image.jpg"
        )

    def test_all_ads_view(self):
        response = self.client.get(reverse("all_ads"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/all_ads.html")
        self.assertContains(response, self.ad.title)

    def test_all_ads_filter_category(self):
        Ad.objects.create(
            user=self.user,
            title="Other Ad",
            description="House description",
            category="house",
            condition="new",
        )
        response = self.client.get(reverse("all_ads") + "?category=cars")
        self.assertContains(response, "Test Ad")
        self.assertNotContains(response, "Other Ad")

    def test_current_ad_view(self):
        response = self.client.get(reverse("current_ad", args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/current_ad.html")
        self.assertContains(response, self.ad.title)

    def test_get_my_ads(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("my_ads"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/all_ads.html")
        self.assertContains(response, self.ad.title)

    def test_create_ad_get(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("create_ad"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/create_ads.html")

    def test_create_ad_post(self):
        self.client.login(username="testuser", password="password")
        data = {
            "title": "Created Ad",
            "description": "Ad created in POST",
            "image_url": "",
            "category": "house",
            "condition": "used"
        }
        response = self.client.post(reverse("create_ad"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title="Created Ad").exists())

    def test_update_ad_get(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("update_ad", args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/update_ad.html")

    def test_update_ad_post(self):
        self.client.login(username="testuser", password="password")
        data = {
            "title": "Updated Title",
            "description": "Updated Desc",
            "category": "cars",
            "condition": "new",
            "image_url": "http://example.com/new.jpg"
        }
        response = self.client.post(reverse("update_ad", args=[self.ad.id]), data)
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, "Updated Title")

    def test_update_ad_forbidden(self):
        self.client.login(username="otheruser", password="password")
        response = self.client.post(reverse("update_ad", args=[self.ad.id]), {
            "title": "Hacked!",
            "description": "Hacked!",
            "category": "cars",
            "condition": "new",
            "image_url": ""
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_ad_success(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("delete_ad", args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())

    def test_delete_ad_forbidden(self):
        self.client.login(username="otheruser", password="password")
        response = self.client.post(reverse("delete_ad", args=[self.ad.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Ad.objects.filter(id=self.ad.id).exists())

    def test_search_view(self):
        response = self.client.get(reverse("search") + "?q=Test")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/all_ads.html")
        self.assertContains(response, self.ad.title)
