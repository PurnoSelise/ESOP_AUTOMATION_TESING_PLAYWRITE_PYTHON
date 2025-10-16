import pytest
from utils.base_test import BaseTest
from datetime import date

@pytest.mark.usefixtures("setup_class")
class TestLogin(BaseTest):
    def test_login_success(self):
        today = date.today()
        a="login is working fine >>"
        print(a+str(today))

        with open("test_results.txt", "a") as f:
            f.write(f"{a}{today}\n")