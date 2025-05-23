from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad
from exchange.models import ExchangeProposal


class ExchangeViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.ad1 = Ad.objects.create(title="Ad 1", description="Desc", user=self.user1)
        self.ad2 = Ad.objects.create(title="Ad 2", description="Desc", user=self.user2)

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment="Let's trade!"
        )

    def test_get_my_proposals(self):
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse("my_proposals"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.proposal, response.context["proposals"])

    def test_get_proposals_sent_me(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse("proposals_sent_me"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.proposal, response.context["proposals"])

    def test_get_current_proposal(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse("current_proposal", args=[self.proposal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["proposal"], self.proposal)

    def test_accept_proposal(self):
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse("accept_proposal", args=[self.proposal.id]))
        self.assertRedirects(response, reverse("my_proposals"))
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, "принята")

    def test_reject_proposal(self):
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse("reject_proposal", args=[self.proposal.id]))
        self.assertRedirects(response, reverse("my_proposals"))
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, "отклонена")

    def test_create_proposal(self):
        self.client.login(username='user1', password='pass')
        data = {
            "ad_sender": self.ad1.id,
            "ad_receiver": self.ad2.id,
            "comment": "New trade idea",
        }
        response = self.client.post(reverse("create_proposal"), data)
        self.assertRedirects(response, reverse("all_ads"))
        self.assertEqual(ExchangeProposal.objects.count(), 2)

    def test_update_proposal(self):
        self.client.login(username='user1', password='pass')
        data = {
            "ad_sender": self.ad1.id,
            "ad_receiver": self.ad2.id,
            "comment": "Updated comment",
        }
        response = self.client.post(reverse("update_proposal", args=[self.proposal.id]), data)
        self.assertRedirects(response, reverse("my_proposals"))
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.comment, "Updated comment")

    def test_delete_proposal(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse("delete_proposal", args=[self.proposal.id]))
        self.assertRedirects(response, reverse("my_ads"))
        self.assertFalse(ExchangeProposal.objects.filter(id=self.proposal.id).exists())
