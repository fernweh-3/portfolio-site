import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # home page tests
    def test_home(self):
        response = self.client.get("/")
        assert response.content_type == "text/html; charset=utf-8"
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Portfolio Site</title>" in html
        assert "Yixing Lei" in html

        # check the profile picture is present
        assert '<img' in html
        assert 'src="/static/img/avatar.png"' in html
        
        assert "About Me" in html

        # check if the page has navigation links
        assert 'href="/profile"' in html
        assert 'href="/timeline"' in html
        assert 'href="/map"' in html
        assert 'href="/hobbies"' in html

        # check if the footer data is injected
        assert "Follow me on:" in html

    # timelime page & API tests
    def test_timeline(self):
        # test GET request before any posts are created
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        # test a POST request
        response = self.client.post("/api/timeline_post", data={
            "name": "Salim",
            "email": "salim@pineapple.lover",
            "content": "I like pineapple on my pizza."
        })
        assert response.status_code == 200
        json = response.get_json()
        assert json["name"] == "Salim"
        assert json["email"] == "salim@pineapple.lover"
        assert json["content"] == "I like pineapple on my pizza."
        # test GET request after a post is created
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert "timeline_posts" in json
        assert any(post["name"] == "Salim" for post in json["timeline_posts"])
        assert any(post["email"] == "salim@pineapple.lover" for post in json["timeline_posts"])
        # test the timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        # Check form and fields
        assert '<form id="timelineForm">' in html
        assert 'name="name"' in html
        assert 'name="email"' in html
        assert 'name="content"' in html
        assert '<button type="submit"' in html
        # Check Past Posts section
        assert "Past Posts" in html
        assert "Salim" in html
        assert "salim@pineapple.lover" in html
        assert "I like pineapple on my pizza." in html
        # test deleting the post
        post_id = json["timeline_posts"][0]["id"]
        response = self.client.delete(f"/api/timeline_post/{post_id}")
        assert response.status_code == 200
        json = response.get_json()
        assert json["status"] == "success"

    def test_malformed_timeline_post(self):
        # POST request with missing name
        response = self.client.post("/api/timeline_post", data=
{"email": "john@example.com", "content": "Hello World! I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data=
{"name": "John", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
{"name": "John", "email": "not-an-email", "content": "Hello World! I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html