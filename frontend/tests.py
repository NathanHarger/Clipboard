from django.test import TestCase
from .forms import SessionForm
# Create your tests here.

class ResultViewTests(TestCase):
	def test_id_result_page(self):
		# test that the results page displays the same id as generated id
		# tests the exposed error in SessionForm only 
		# storing 5 of 8 characters
		response = self.client.get('/clipboard/setClipboard/test')
		sId = response.json()["id"]
		sf = SessionForm(data = sId)
		results = self.client.get('/results/' +sf.data)
		self.assertContains(results, sf.data,status_code=301)


