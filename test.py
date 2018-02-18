from login_example import app
import unittest

class flaskTestCase(unittest.TestCase):

	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	def test_login_page(self):
		tester = app.test_client(self)
		response = tester.get('/signIn', content_type='html/text')
		self.assertTrue(b'Sign In' in response.data)

	#When user no user is logged in make sure redirects handle accordingly
	def test_profile_redirect_page(self):
		tester = app.test_client(self)
		response = tester.get('/profile',
			 follow_redirects=True)
		self.assertTrue(b'Sign In' in response.data)

	def test_profile_displays_correcly_page(self):
		tester = app.test_client(self)
		response = tester.get('/profile',
			data=dict(name="keeffy96@gmail.com", passw="password"),
			follow_redirects=True)
		self.assertIn(b'Computer Science Course: Material', response.data)	

	# #testing login page to ensure login behaves correctly given the correct credentials
	# def test_logout_correct(self):
	# 	tester = app.test_client(self)
	# 	response = tester.get('/profile', 
	# 		data=dict(username="abc", password="abc"), 
	# 		follow_redirects=True)
	# 	self.assertTrue(b'Home Page' in response.data)

if __name__ == '__main__':
	unittest.main()