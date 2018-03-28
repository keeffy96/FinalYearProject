from main import app
import unittest

class flaskTestCase(unittest.TestCase):	
	
	#Checks if home page loads correctly
	def test_homePage_loads_correctly(self):
		tester = app.test_client(self)
		response = tester.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	#Checks if profile page returns code 302 - due to no user been signed in
	def test_profilePage_loads_correctly(self):
		tester = app.test_client(self)
		response = tester.get('/profile', content_type='html/text')
		self.assertEqual(response.status_code, 302)

	#Checks if invalid url returns error 404
	def test_invalid_url(self):
		tester = app.test_client(self)
		response = tester.get('/notVaidURL', content_type='html/text')
		self.assertEqual(response.status_code, 404)

	#Checks if student authentication page loads correctly
	def test_studentRegisterPage_loads_correctly(self):
		tester = app.test_client(self)
		response = tester.get('/studentRegister', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	#Checks if teacher authentication page loads correctly
	def test_teacherRegisterPage_loads_correctly(self):
		tester = app.test_client(self)
		response = tester.get('/register', content_type='html/text')
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()