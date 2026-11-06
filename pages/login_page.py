from playwright.sync_api import Page, expect

class LoginPortalException(Exception):
    pass

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.zenclass.in/"  # Replace with your actual Zen Portal URL if different

        # Locators (Adjust selectors based on actual DOM attributes)
        self.username_input = "//input[@id=':r1:']"
        self.password_input = "//input[@id=':r2:']"
        self.submit_button = "//button[@type='submit']"
        self.logout_button = "//div[.='Log out']"
        self.user_profile_icon =  "//p[.='student']"
        self.popup_close_button = "button.custom-close-button"


    def load(self):
        """Navigates to the Zen Portal login page."""
        try:
            self.page.goto(self.url, timeout=60000)
        except Exception as e:
            raise LoginPortalException(f"Failed to load URL {self.url}: {str(e)}")

    def validate_input_boxes(self):
        """Validates that Username and Password input boxes are visible and editable."""
        try:
            expect(self.page.locator(self.username_input)).to_be_visible()
            expect(self.page.locator(self.username_input)).to_be_editable()

            expect(self.page.locator(self.password_input)).to_be_visible()
            expect(self.page.locator(self.password_input)).to_be_editable()
        except AssertionError as ae:
            raise LoginPortalException(f"Input box validation failed: {str(ae)}")

    def validate_submit_button(self):
        """Validates that the submit button is present and enabled."""
        try:
            submit_btn = self.page.locator(self.submit_button)
            expect(submit_btn).to_be_visible()
            expect(submit_btn).to_be_enabled()
        except AssertionError as ae:
            raise LoginPortalException(f"Submit button validation failed: {str(ae)}")

    def login(self, username: str, password: str):
        """Performs login action."""
        try:
            self.page.fill(self.username_input, username)
            self.page.fill(self.password_input, password)
            self.page.click(self.submit_button)
        except Exception as e:
            raise LoginPortalException(f"Error occurred during login action: {str(e)}")

    def verify_successful_login(self):

        try:
            # Explicitly wait for navigation or profile element to appear after login
            self.page.wait_for_load_state("networkidle", timeout=10000)
            self.page.click(self.popup_close_button)
            # Ensure we are no longer on the login page or profile element is visible
            expect(self.page.locator(self.logout_button).or_(self.page.locator(self.user_profile_icon))).to_be_visible(
                timeout=10000)
        except Exception as e:
            raise LoginPortalException(f"Successful login verification failed: {str(e)}")

    def verify_unsuccessful_login(self):
        """Verifies error message or failure to navigate on invalid credentials."""
        try:
            # Check that user remains on login page or an error message toast appears
            error_msg = self.page.locator(".error-message, .toast-error, [role='alert']")
            if error_msg.count() > 0:
                expect(error_msg.first).to_be_visible()
            else:
                # Fallback: confirm logout button is NOT visible
                expect(self.page.locator(self.logout_button)).not_to_be_visible()
        except Exception as e:
            raise LoginPortalException(f"Unsuccessful login validation failed: {str(e)}")

    def logout(self):
        """Performs logout action by opening the profile menu and clicking Log out."""
        try:
            # 1. Click the profile icon/avatar to open the dropdown menu
            profile_icon = self.page.locator(
                "//p[.='student']").first
            if profile_icon.count() > 0:
                profile_icon.click()

            # 2. Wait explicitly for the 'Log out' text element to become visible inside the menu
            logout_elem = self.page.locator("//div[.='Log out']").first
            logout_elem.wait_for(state="visible", timeout=50000)
            logout_elem.click()

            # 3. Verify user is redirected back to the login screen
            expect(self.page.locator(self.username_input).first).to_be_visible(timeout=10000)
        except Exception as e:
            raise LoginPortalException(f"Logout functionality validation failed: {str(e)}")