import unittest
import os

os.environ["TESTING"] = "true"

from app import app
from tests import test_db


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # test for tylerwork.html response
    def test_home(self):
        response = self.client.get("/")  # fetch response
        assert response.status_code == 200  # first ensure successful code
        html = response.get_data(
            as_text=True
        )  # parse through response and store as text to test against existing sections of body
        assert "<h1>tyler's Portfolio</h1>" in html
        assert '<p class="lead">UTSA \'23 - CS Major, Love doing nerd stuff</p>' in html
        assert '<a href="https://www.linkedin.com/in/tyler-holstein-38ab601a0/">'

    # test GET request for timeline_post endpoint
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        # list should contain 0 elements
        assert len(json["timeline_posts"]) == 0

        # using the db test, post 2 documents to the db, request them back, and re-assert
        test_db.TestTimelinePost.test_timeline_post(self)
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2

        # if posts successful, test frontend:
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert (
            'placeholder="John Doe"' in html
        )  # first test if response is consistent with the default body
        assert "<p>Name: Sam</p>" in html  # then test if db data is properly generated
