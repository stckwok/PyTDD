from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

import time
import warnings

MAX_WAIT = 5 

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test

class VisitorPageTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")  
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException):  
                if time.time() - start_time > MAX_WAIT:  
                    raise  
                time.sleep(0.5)  

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_todolist(self):
        # 1. Launch home page of ToDoList App
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # self.fail("Finish the test!")

        # sleep a bit and close Firefox page
        time.sleep(2)

    def test_redirects_after_POST(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


    # def test_multiple_users_can_start_lists_at_different_urls(self):
    #     # starts a new to-do list
    #     self.browser.get(self.live_server_url)
    #     inputbox = self.browser.find_element(By.ID, "id_new_item")
    #     inputbox.send_keys("Buy peacock feathers")
    #     inputbox.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table("1: Buy peacock feathers")

    #     # list has a unique URL
    #     userA_list_url = self.browser.current_url
    #     self.assertRegex(userA_list_url, "/lists/.+")

    #      # Now a new user B, comes along to the site.

    #     ## We delete all the browser's cookies
    #     ## as a way of simulating a brand new user session  
    #     self.browser.delete_all_cookies()

    #     # UserB visits the home page.  There is no sign of Edith's
    #     # list
    #     self.browser.get(self.live_server_url)
    #     page_text = self.browser.find_element(By.TAG_NAME, "body").text
    #     self.assertNotIn("Buy peacock feathers", page_text)
    #     self.assertNotIn("make a fly", page_text)

    #     # User B starts a new list by entering a new item. He
    #     # is less interesting than Edith...
    #     inputbox = self.browser.find_element(By.ID, "id_new_item")
    #     inputbox.send_keys("Buy milk")
    #     inputbox.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table("1: Buy milk")

    #     #  gets his own unique URL
    #     userB_list_url = self.browser.current_url
    #     self.assertRegex(userB_list_url, "/lists/.+")
    #     self.assertNotEqual(userB_list_url, userA_list_url)

    #     # Again, there is no trace of Edith's list
    #     page_text = self.browser.find_element(By.TAG_NAME, "body").text
    #     self.assertNotIn("Buy peacock feathers", page_text)
    #     self.assertIn("Buy milk", page_text)

    #     # Satisfied, they both go back to sleep