import unittest

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CommonMethods:
    @staticmethod
    def login(driver):
        username_field = driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        return WebDriverWait(driver, 5).until(EC.title_is("Home"))


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost")

    def testCorrectLoginIncorrectPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("wrongpass")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        assert msg_field_text == 'Incorrect username/password!'

    def testCorrectLoginEmptyPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        assert password_field.get_attribute("validationMessage") == "Please fill out this field."

    def testEmptyLoginCorrectPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        assert username_field.get_attribute("validationMessage") == "Please fill out this field."

    def testSucceedingLogin(self):
        assert CommonMethods.login(self.driver)

    def testLoginLogout(self):
        CommonMethods.login(self.driver)

        self.driver.find_element_by_xpath("//a[text()='Logout']").click()
        assert WebDriverWait(self.driver, 5).until(EC.title_is("Login"))

    def tearDown(self):
        self.driver.close()


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1/pythonlogin/register")

    def testEmptyUsernameCorrectPasswordCorrectEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert username_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameEmptyPasswordCorrectEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert password_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameCorrectPasswordEmptyEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("pass")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert email_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameCorrectPasswordIncorrectEmail(self):
        """
        "test@test", "@test.com", "test@@test.com", "test.com@"
        """
        emails_to_test = ["test@test", "@test.com", "test@@test.com", "test.com@"]
        for email in emails_to_test:
            assert self.checkMail(email)

    def checkMail(self, email):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("testuser")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("testuser")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys(email)

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        return msg_field_text == 'Invalid email address!'

    def testUsedCredentials(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        return msg_field_text == 'Account already exists!'

    def testIncorrectUsernameCorrectPasswordCorrectEmail(self):
        """
        "ad@m2020", "test2020!"
        """
        usernames_to_test = ["ad@m2020", "test2020!", "test%", "test20&"]
        for username in usernames_to_test:
            assert self.checkUsername(username)

    def checkUsername(self, username):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("pass")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@example.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        return msg_field_text == 'Username must contain only characters and numbers!'

    def tearDown(self):
        self.driver.close()


class TestFindingByTag(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1")
        CommonMethods.login(self.driver)

    def testMainImage(self):
        tag_field = self.driver.find_element_by_xpath("//input[@placeholder='Find by tag']")
        tag_field.send_keys("car")
        self.driver.find_element_by_xpath("//button").click()
        assert self.driver.find_element_by_id("main")

    def testDetailImage(self):
        tag_field = self.driver.find_element_by_xpath("//input[@placeholder='Find by tag']")
        tag_field.send_keys("car")
        self.driver.find_element_by_xpath("//button").click()
        assert self.driver.find_element_by_id("sec")

    def tearDown(self):
        self.driver.close()


class TestProfileTab(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1")
        CommonMethods.login(self.driver)
        self.driver.find_element_by_xpath("//a[text()='Profile']").click()

    def testCorrectnessUsersInfo(self):
        table = self.driver.find_element_by_xpath("//table/tbody")
        assert table.text == """Username: test
Password: test
Email: test@test.com"""

    def testAddingUrl(self):
        url = "https://www.youtube.com/watch?v=5lXNnKjui0g"
        url_field = self.driver.find_element_by_xpath("//input[@placeholder='Add stream url']")
        url_field.send_keys(url)
        self.driver.find_element_by_xpath("//button").click()

        url_table = self.driver.find_element_by_id("url_table")
        assert url in url_table.text

    def tearDown(self):
        self.driver.close()


class TestPageNotFoundError(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1")

    def testPageNotFoundForNonLoggedIn(self):
        self.driver.get("http://127.0.0.1/random_url")
        assert "Page not found." == self.driver.find_element_by_xpath("//h2").text

    def testPageNotFoundForLoggedIn(self):
        CommonMethods.login(self.driver)
        self.driver.get("http://127.0.0.1/random_url")
        assert "Page not found." == self.driver.find_element_by_xpath("//h2").text

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
