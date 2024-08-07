import json
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse

from django.contrib.sessions.backends.db import SessionStore


class StripeWebHookViewTest(TestCase):
    @patch("stripe.Event.construct_from")
    def test_stripe_webhook(self, mock_construct_event):
        # Mock Stripe"s webhook event
        mock_event = {
            "id": "evt_test_webhook",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_session",
                    "object": "checkout.session",
                    "metadata": {
                        "session_id": self.client.session.session_key
                    }
                }
            }
        }
        mock_construct_event.return_value = mock_event

        # Make a POST request to the webhook endpoint
        response = self.client.post(reverse("store:stripe_webhook"), data=json.dumps(mock_event), content_type="application/json")

        # Verify that the webhook endpoint returns a 200 response
        self.assertEqual(response.status_code, 200)

        # Verify that the session has been cleared
        session_store = SessionStore(session_key=self.client.session.session_key)
        self.assertEqual(session_store.get("bag"), [])
        self.assertEqual(session_store.get("total_items"), 0)