from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text  
        self.assertIn("To-Do", header_text)

        # 3. enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # 4. Type "Buy peacock feathers" into a text box
        inputbox.send_keys("Buy peacock feathers") 

        # When hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # There is still a text box to add another item.
        # enters "Use peacock feathers to make a fly"

        self.fail("Finish the test!")

        # The page updates again, and now shows both items on the list

        # sleep a bit and close Firefox page
        time.sleep(5)

if __name__ == "__main__":
    unittest.main()   # warnings='ignore'