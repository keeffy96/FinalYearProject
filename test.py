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

	#testing login page to ensure login behaves correctly given the correct credentials
	def test_logout_correct(self):
		tester = app.test_client(self)
		tester.post('/signIn', data=dict(username="keeffy96@gmail.com", password="password"), follow_redirects=True)
		response = tester.get('/logout', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()