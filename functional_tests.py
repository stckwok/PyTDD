from selenium import webdriver
import unittest
import time
import warnings

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test

class VisitorPageTest(unittest.TestCase):
    @ignore_warnings
    def setUp(self):
        self.browser = webdriver.Firefox()

    @ignore_warnings
    def tearDown(self):
        self.browser.quit()

    @ignore_warnings
    def test_can_start_a_todolist(self):
        # 1. Launch home page of ToDoList App
        self.browser.get("http://localhost:8000")

        print("Title : ", self.browser.title)
        # assert "Congratulations!" in self.browser.title
        # print("OK")

        # 2. page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)

        # 3. enter a to-do item straight away
        self.fail("Finish the test!") 

        # sleep a bit and close Firefox page
        time.sleep(5)

if __name__ == "__main__":
    unittest.main()   # warnings='ignore'