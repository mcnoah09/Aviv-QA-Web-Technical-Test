from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

        # Define the page's URL
        self.url = "https://demo.nopcommerce.com/login"

        # Define web elements on the page
        self.email_textbox = (By.ID, "Email")
        self.password_textbox = (By.ID, "Password")
        self.remember_me_checkbox = (By.ID, "RememberMe")
        self.login_button = (By.CSS_SELECTOR, ".login-button")
        self.logout_button = (By.CSS_SELECTOR, ".ico-logout")

    def open(self):
        self.driver.get(self.url)

    def enter_email(self, email):
        email_textbox = self.wait.until(EC.element_to_be_clickable(self.email_textbox))
        email_textbox.clear()
        email_textbox.send_keys(email)

    def enter_password(self, password):
        password_textbox = self.wait.until(
            EC.element_to_be_clickable(self.password_textbox)
        )
        password_textbox.clear()
        password_textbox.send_keys(password)

    def click_remember_me(self):
        self.wait.until(EC.element_to_be_clickable(self.remember_me_checkbox)).click()

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self.login_button)).click()

    def click_logout(self):
        self.wait.until(EC.element_to_be_clickable(self.logout_button)).click()
