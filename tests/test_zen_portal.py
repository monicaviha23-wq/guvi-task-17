import pytest
from pages.login_page import LoginPage, LoginPortalException

# Replace with valid test credentials or load via environment variables/config
VALID_USERNAME = "monicaviha23@gmail.com"
VALID_PASSWORD = "Waffleswaves2310@"
INVALID_USERNAME = "invalid_user@example.com"
INVALID_PASSWORD = "wrong_password"

def test_validate_username_and_password_inputs(page):
    """Test case 5(c): Validate Username and Password Input boxes are present and interactive."""
    login_page = LoginPage(page)
    login_page.load()
    login_page.validate_input_boxes()


def test_validate_submit_button_working(page):
    """Test case 5(d): Validate Submit button working status."""
    login_page = LoginPage(page)
    login_page.load()
    login_page.validate_submit_button()


def test_unsuccessful_login(page):
    """Test case 5(b): Validate Unsuccessful Login with invalid credentials."""
    login_page = LoginPage(page)
    login_page.load()
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)
    login_page.verify_unsuccessful_login()


def test_successful_login_and_logout(page):
    """Test cases 5(a) & 5(e): Validate Successful Login, Dashboard access, and Logout functionality."""
    login_page = LoginPage(page)
    login_page.load()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    # 5(a) Successful Login validation
    login_page.verify_successful_login()

    # 5(e) Validate Logout functionality
    login_page.logout()