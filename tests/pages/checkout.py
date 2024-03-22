from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class CheckoutPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait


class BillingAddress(CheckoutPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

        # Define web elements on the page
        self.ship_to_same_address_checkbox = (
            By.CSS_SELECTOR,
            ".section.ship-to-same-address",
        )
        self.first_name_input = (By.ID, "BillingNewAddress_FirstName")
        self.last_name_input = (By.ID, "BillingNewAddress_LastName")
        self.email_input = (By.ID, "BillingNewAddress_Email")
        self.company_input = (By.ID, "BillingNewAddress_Company")
        self.country_select = (By.ID, "BillingNewAddress_CountryId")
        self.state_select = (By.ID, "BillingNewAddress_StateProvinceId")
        self.city_input = (By.ID, "BillingNewAddress_City")
        self.address1_input = (By.ID, "BillingNewAddress_Address1")
        self.address2_input = (By.ID, "BillingNewAddress_Address2")
        self.zip_input = (By.ID, "BillingNewAddress_ZipPostalCode")
        self.phone_input = (By.ID, "BillingNewAddress_PhoneNumber")
        self.fax_input = (By.ID, "BillingNewAddress_FaxNumber")
        self.continue_button = (
            By.CSS_SELECTOR,
            ".new-address-next-step-button:not([disabled])",
        )

    def click_ship_to_same_address(self):
        elm = self.wait.until(
            EC.element_to_be_clickable(self.ship_to_same_address_checkbox)
        )
        if elm.is_selected():
            elm.click()

    def uncheck_ship_to_same_address(self):
        elm = self.wait.until(
            EC.element_to_be_clickable(self.ship_to_same_address_checkbox)
        )
        if not elm.is_selected():
            # Odd behaviour: if the checkbox is not selected, is selected() returns True
            elm.click()

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

    def enter_company(self, company: str):
        company_textbox = self.wait.until(
            EC.element_to_be_clickable(self.company_input)
        )
        company_textbox.clear()
        company_textbox.send_keys(company)

    def select_country(self, country: str):
        country_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.country_select))
        )
        country_select.select_by_visible_text(country)

    def select_state(self, state: str):
        state_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.state_select))
        )
        state_select.select_by_value(state)

    def enter_city(self, city: str):
        city_textbox = self.wait.until(EC.element_to_be_clickable(self.city_input))
        city_textbox.clear()
        city_textbox.send_keys(city)

    def enter_address1(self, address1: str):
        address1_textbox = self.wait.until(
            EC.element_to_be_clickable(self.address1_input)
        )
        address1_textbox.clear()
        address1_textbox.send_keys(address1)

    def enter_address2(self, address2: str):
        address2_textbox = self.wait.until(
            EC.element_to_be_clickable(self.address2_input)
        )
        address2_textbox.clear()
        address2_textbox.send_keys(address2)

    def enter_zip_postal_code(self, zip_code: str):
        zip_textbox = self.wait.until(EC.element_to_be_clickable(self.zip_input))
        zip_textbox.clear()
        zip_textbox.send_keys(zip_code)

    def enter_phone_number(self, phone: str):
        phone_textbox = self.wait.until(EC.element_to_be_clickable(self.phone_input))
        phone_textbox.clear()
        phone_textbox.send_keys(phone)

    def enter_fax_number(self, fax: str):
        fax_textbox = self.wait.until(EC.element_to_be_clickable(self.fax_input))
        fax_textbox.clear()
        fax_textbox.send_keys(fax)

    def click_continue(self):
        self.wait.until(EC.element_to_be_clickable(self.continue_button)).click()


class ShippingAddress(CheckoutPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

        # Define web elements on the page
        self.shipping_address_select = (By.ID, "shipping-address-select")
        self.first_name_input = (By.ID, "ShippingNewAddress_FirstName")
        self.last_name_input = (By.ID, "ShippingNewAddress_LastName")
        self.email_input = (By.ID, "ShippingNewAddress_Email")
        self.company_input = (By.ID, "ShippingNewAddress_Company")
        self.country_select = (By.ID, "ShippingNewAddress_CountryId")
        self.state_select = (By.ID, "ShippingNewAddress_StateProvinceId")
        self.city_input = (By.ID, "ShippingNewAddress_City")
        self.address1_input = (By.ID, "ShippingNewAddress_Address1")
        self.address2_input = (By.ID, "ShippingNewAddress_Address2")
        self.zip_input = (By.ID, "ShippingNewAddress_ZipPostalCode")
        self.phone_input = (By.ID, "ShippingNewAddress_PhoneNumber")
        self.fax_input = (By.ID, "ShippingNewAddress_FaxNumber")
        self.continue_button = (
            By.XPATH,
            (
                "//span[@id='shipping-please-wait']/preceding-sibling::button[@class='button-1"
                " new-address-next-step-button']"
            ),
        )

    def select_billing_address(self):
        shipping_address_select = self.wait.until(
            EC.element_to_be_clickable(self.shipping_address_select)
        )
        shipping_address_select.select_by_index(0)

    def select_new_shipping_address(self):
        shipping_address_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.shipping_address_select))
        )
        shipping_address_select.select_by_visible_text("New Address")

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

    def enter_company(self, company: str):
        company_textbox = self.wait.until(
            EC.element_to_be_clickable(self.company_input)
        )
        company_textbox.clear()
        company_textbox.send_keys(company)

    def select_country(self, country: str):
        country_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.country_select))
        )
        country_select.select_by_visible_text(country)

    def select_state(self, state: str):
        state_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.state_select))
        )
        state_select.select_by_visible_text(state)

    def enter_city(self, city: str):
        city_textbox = self.wait.until(EC.element_to_be_clickable(self.city_input))
        city_textbox.clear()
        city_textbox.send_keys(city)

    def enter_address1(self, address1: str):
        address1_textbox = self.wait.until(
            EC.element_to_be_clickable(self.address1_input)
        )
        address1_textbox.clear()
        address1_textbox.send_keys(address1)

    def enter_address2(self, address2: str):
        address2_textbox = self.wait.until(
            EC.element_to_be_clickable(self.address2_input)
        )
        address2_textbox.clear()
        address2_textbox.send_keys(address2)

    def enter_zip_postal_code(self, zip: str):
        zip_textbox = self.wait.until(EC.element_to_be_clickable(self.zip_input))
        zip_textbox.clear()
        zip_textbox.send_keys(zip)

    def enter_phone_number(self, phone: str):
        phone_textbox = self.wait.until(EC.element_to_be_clickable(self.phone_input))
        phone_textbox.clear()
        phone_textbox.send_keys(phone)

    def enter_fax_number(self, fax: str):
        fax_textbox = self.wait.until(EC.element_to_be_clickable(self.fax_input))
        fax_textbox.clear()
        fax_textbox.send_keys(fax)

    def click_continue(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight / 2);"
        )
        self.wait.until(EC.element_to_be_clickable(self.continue_button)).click()


class ShippingMethod(CheckoutPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

        # Define web elements on the page
        self.shipping_method_ground_radio = (By.ID, "shippingoption_1")
        self.shipping_method_next_day_air_radio = (By.ID, "shippingoption_2")
        self.shipping_method_second_day_air_radio = (By.ID, "shippingoption_3")
        self.shipping_method_continue_button = (
            By.CSS_SELECTOR,
            ".shipping-method-next-step-button",
        )

    def select_ground_shipping_method(self):
        self.wait.until(
            EC.element_to_be_clickable(self.shipping_method_ground_radio)
        ).click()

    def select_next_day_air_shipping_method(self):
        self.wait.until(
            EC.element_to_be_clickable(self.shipping_method_next_day_air_radio)
        ).click()

    def select_second_day_air_shipping_method(self):
        self.wait.until(
            EC.element_to_be_clickable(self.shipping_method_second_day_air_radio)
        ).click()

    def click_continue(self):
        self.wait.until(
            EC.element_to_be_clickable(self.shipping_method_continue_button)
        ).click()


class PaymentMethod(CheckoutPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

        # Define web elements on the page
        self.payment_method_credit_card_radio = (By.ID, "paymentmethod_1")
        self.payment_method_cheque_or_cash_radio = (By.ID, "paymentmethod_0")
        self.payment_method_continue_button = (
            By.CSS_SELECTOR,
            ".payment-method-next-step-button",
        )
        self.payment_info_cheque_or_cash_continue_button = (
            By.CSS_SELECTOR,
            ".payment-info-next-step-button",
        )
        self.card_type = (By.ID, "CreditCardType")
        self.card_holder_name = (By.ID, "CardholderName")
        self.card_number = (By.ID, "CardNumber")
        self.card_expiry_month = (By.ID, "ExpireMonth")
        self.card_expiry_year = (By.ID, "ExpireYear")
        self.card_code = (By.ID, "CardCode")

    def select_credit_card_payment_method(self):
        self.wait.until(
            EC.element_to_be_clickable(self.payment_method_credit_card_radio)
        ).click()

    def select_cheque_or_cash_on_payment_method(self):
        self.wait.until(
            EC.element_to_be_clickable(self.payment_method_cheque_or_cash_radio)
        ).click()

    def click_continue_for_cheque_or_cash(self):
        self.wait.until(
            EC.element_to_be_clickable(self.payment_info_cheque_or_cash_continue_button)
        ).click()

    def select_card_type(self, card_type: str):
        card_type_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.card_type))
        )
        card_type_select.select_by_value(card_type)

    def enter_card_holder_name(self, card_holder_name: str):
        card_holder_name_textbox = self.wait.until(
            EC.element_to_be_clickable(self.card_holder_name)
        )
        card_holder_name_textbox.clear()
        card_holder_name_textbox.send_keys(card_holder_name)

    def enter_card_number(self, card_number: str):
        card_number_textbox = self.wait.until(
            EC.element_to_be_clickable(self.card_number)
        )
        card_number_textbox.clear()
        card_number_textbox.send_keys(card_number)

    def select_card_expiry_month(self, card_expiry_month: str):
        card_expiry_month_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.card_expiry_month))
        )
        card_expiry_month_select.select_by_value(card_expiry_month)

    def select_card_expiry_year(self, card_expiry_year: str):
        card_expiry_year_select = Select(
            self.wait.until(EC.element_to_be_clickable(self.card_expiry_year))
        )
        card_expiry_year_select.select_by_value(card_expiry_year)

    def enter_card_code(self, card_code: str):
        card_code_textbox = self.wait.until(EC.element_to_be_clickable(self.card_code))
        card_code_textbox.clear()
        card_code_textbox.send_keys(card_code)

    def click_continue(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight / 2);"
        )
        self.wait.until(
            EC.element_to_be_clickable(self.payment_method_continue_button)
        ).click()


class ConfirmOrder(CheckoutPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)

        # Define web elements on the page
        self.confirm_order_button = (By.CSS_SELECTOR, ".confirm-order-next-step-button")
        self.success_message_text = (
            By.CSS_SELECTOR,
            ".section.order-completed .title strong",
        )
        self.order_completed_continue_button = (
            By.CSS_SELECTOR,
            ".order-completed-continue-button",
        )

    def click_confirm_order(self):
        self.wait.until(EC.element_to_be_clickable(self.confirm_order_button)).click()

    def get_success_message_text(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.success_message_text)
        ).text

    def click_order_completed_continue(self):
        self.wait.until(
            EC.element_to_be_clickable(self.order_completed_continue_button)
        ).click()
