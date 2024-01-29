from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

        # Define the page's URL
        self.url = "https://demo.nopcommerce.com/register"

        # Define web elements on the page
        self.register_page_button = (By.CSS_SELECTOR, ".ico-register")
        self.male_gender_input = (By.ID, "gender-male")
        self.female_gender_input = (By.ID, "gender-female")
        self.first_name_input = (By.ID, "FirstName")
        self.last_name_input = (By.ID, "LastName")
        self.email_input = (By.ID, "Email")
        self.day_of_birth_select = (By.NAME, "DateOfBirthDay")
        self.month_of_birth_select = (By.NAME, "DateOfBirthMonth")
        self.year_of_birth_select = (By.NAME, "DateOfBirthYear")
        self.company_name_input = (By.ID, "Company")
        self.newsletter_checkbox = (By.ID, "Newsletter")
        self.password_input = (By.ID, "Password")
        self.confirm_password_input = (By.ID, "ConfirmPassword")
        self.register_button = (By.ID, "register-button")
        self.registration_success_message = (By.XPATH, "//div[@class='result']")
        self.continue_button = (By.XPATH, "//a[text()='Continue']")

        self.field_validation_error = (By.CSS_SELECTOR, ".field-validation-error span")

    def open(self):
        self.driver.get(self.url)

    def click_register_page(self):
        self.wait.until(EC.element_to_be_clickable(self.register_page_button)).click()

    def select_gender(self, gender: str):
        if gender.lower() == "male":
            self.wait.until(EC.element_to_be_clickable(self.male_gender_input)).click()
        elif gender.lower() == "female":
            self.wait.until(
                EC.element_to_be_clickable(self.female_gender_input)
            ).click()
        else:
            raise ValueError("Unexpected value for gender!")

    def enter_first_name(self, first_name: str):
        first_name_textbox = self.wait.until(
            EC.element_to_be_clickable(self.first_name_input)
        )
        first_name_textbox.clear()
        first_name_textbox.send_keys(first_name)

    def enter_last_name(self, last_name: str):
        last_name_textbox = self.wait.until(
            EC.element_to_be_clickable(self.last_name_input)
        )
        last_name_textbox.clear()
        last_name_textbox.send_keys(last_name)

    def enter_email(self, email: str):
        email_textbox = self.wait.until(EC.element_to_be_clickable(self.email_input))
        email_textbox.clear()
        email_textbox.send_keys(email)

    def enter_password(self, password: str):
        password_textbox = self.wait.until(
            EC.element_to_be_clickable(self.password_input)
        )
        password_textbox.clear()
        password_textbox.send_keys(password)

    def enter_confirm_password(self, password: str):
        confirm_password_textbox = self.wait.until(
            EC.element_to_be_clickable(self.confirm_password_input)
        )
        confirm_password_textbox.clear()
        confirm_password_textbox.send_keys(password)

    def enter_date_of_birth(self, date_of_birth: date):
        self.wait.until(EC.element_to_be_clickable(self.day_of_birth_select)).send_keys(
            str(date_of_birth.day)
        )
        self.wait.until(
            EC.element_to_be_clickable(self.month_of_birth_select)
        ).send_keys(str(date_of_birth.month))
        self.wait.until(
            EC.element_to_be_clickable(self.year_of_birth_select)
        ).send_keys(str(date_of_birth.year))

    def enter_company_name(self, company_name: str):
        company_name_textbox = self.wait.until(
            EC.element_to_be_clickable(self.company_name_input)
        )
        company_name_textbox.clear()
        company_name_textbox.send_keys(company_name)

    def click_newsletter(self):
        self.wait.until(EC.element_to_be_clickable(self.newsletter_checkbox)).click()

    def click_register(self):
        self.wait.until(EC.element_to_be_clickable(self.register_button)).click()

    def click_continue(self):
        self.wait.until(EC.element_to_be_clickable(self.continue_button)).click()

    def get_field_validation_error(self):
        return self.wait.until(
            EC.presence_of_element_located(self.field_validation_error)
        ).text
