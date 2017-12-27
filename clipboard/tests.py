from django.test import TestCase
from clipboard.models import Entry 
import string

# Create your tests here.

class Test_Session_Id(TestCase):


	
	def test_no_duplicates(self):
		# Test uniqueness of session_id
		one = Entry(data="one")
		two = Entry(data="two")
		self.assertNotEqual(one.session_id, two.session_id)
	
	def test_no_symbols(self):
		# ensure the session id only has numbers and letters
		one = Entry()
		sessionId = one.session_id
		okay =(string.ascii_letters + string.digits) 
		invalid = [j for j in sessionId if j not in okay]
		self.assertEqual(len(invalid), 0)
		
	def test_session_id_length_eight(self):
		one = Entry()
		sessionId = one.session_id
		self.assertEqual(len(sessionId),8)

class Test_Entry_Data(TestCase):
	def test_entries_contain_data(self):
		# Test data binding
		one = Entry(data="one")
		self.assertEqual(one.data, "one")



