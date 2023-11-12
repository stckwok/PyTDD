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
    def test_can_start_a_list(self):

        self.browser.get("http://localhost:8000")

        print("Title : ", self.browser.title)
        assert "Congratulations!" in self.browser.title
        print("OK")

        # sleep a bit and close Firefox page
        time.sleep(5)

if __name__ == "__main__":
    unittest.main()   # warnings='ignore'