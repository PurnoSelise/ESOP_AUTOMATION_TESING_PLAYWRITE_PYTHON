import pytest
from utils.base_test import BaseTest
from datetime import date
from pages.Checout_COD import checkout_COD
@pytest.mark.usefixtures("setup_class")
class TestCheckoutCOD(BaseTest):
    def test_checkout_cod(self):
        checkout = checkout_COD(self.page)  # page already logged in from BaseTest
        checkout.checkout()
        today = date.today()
        b="Check out COD is working fine >>"
        print(b + str(today))

        with open("test_results.txt", "a") as f:
            f.write(f"{b}{today}\n")