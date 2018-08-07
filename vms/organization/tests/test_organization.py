# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core import mail

# local Django
from pom.pages.eventsPage import EventsPage
from pom.pages.authenticationPage import AuthenticationPage
from pom.locators.eventsPageLocators import EventsPageLocators
from shift.utils import (create_admin_with_unlisted_org,
                         create_volunteer, create_organization)


class OrganizationTest(LiveServerTestCase):
    """
    E2E Tests for Organization views:
        - Create Organization
        - Edit Organization
        - Approve unlisted Organization
        - Reject unlisted Organization
        - Check duplicate Organization
        - Delete Org with registered volunteers
        - Delete Org without registered volunteers
    """

    @classmethod
    def setUpClass(cls):
        """Method to initiate class level objects.

        This method initiates Firefox WebDriver, WebDriverWait and
        the corresponding POM objects for this Test Class
        """
        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.organization_page = EventsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.elements = EventsPageLocators()
        super(OrganizationTest, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_admin_with_unlisted_org()
        self.login_admin()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        self.authentication_page.logout()

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        super(OrganizationTest, cls).tearDownClass()

    def login_admin(self):
        """
        Utility function to login as administrator with correct credentials.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def delete_organization_from_list(self):
        """
        Utility function to delete organization using form.
        """
        organization_page = self.organization_page
        self.assertEqual(
            organization_page.element_by_xpath(self.elements.DELETE_ORG).text,
            'Delete'
        )
        organization_page.element_by_xpath(
            self.elements.DELETE_ORG + '//a'
        ).click()

        # Check if Organization is deleted.
        self.assertNotEqual(organization_page.get_deletion_box(), None)
        self.assertEqual(organization_page.get_deletion_context(),
                         'Delete Organization')
        organization_page.submit_form()

    def test_approve_organization(self):
        """
        tests if the organization moves to
         the listed section if the admin approves it
        """
        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        organization_page.navigate_to_organization_view()

        # tests admin unlisted org
        self.assertEqual(organization_page.get_approval_context(), 'Approve')
        organization_page.approve_org()

        self.assertEqual(organization_page.get_org_name(), 'organization')

    def test_reject_organization(self):
        """
        tests if the organization gets removed
         from the unlisted section if the admin rejects it
        """
        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        organization_page.navigate_to_organization_view()

        # tests admin unlisted org
        self.assertEqual(organization_page.get_rejection_context(), 'Reject')
        organization_page.reject_org()

        mail.outbox = []
        mail.send_mail(
            "Organization Rejected",
            "The organization you filled while sign-up has been rejected",
            "messanger@localhost.com",
            ['admin@admin.com']
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, "Organization Rejected")
        self.assertEqual(msg.to, ['admin@admin.com'])

    def test_view_organization(self):
        """
        Test display of registered organization.
        """
        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Create a Dummy Organization
        organization = create_organization()

        # Navigate to /organization/list
        organization_page.navigate_to_organization_view()

        # Check correctness of organization
        self.assertEqual(
            organization_page.remove_i18n(self.driver.current_url),
            self.live_server_url + organization_page.organization_list_page
        )
        self.assertEqual(organization_page.get_org_name(), organization.name)

    def test_create_valid_organization(self):
        """
        Test creation of organization with valid values.
        """
        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Navigate to Organization Edit
        organization_page.navigate_to_organization_view()
        organization_page.go_to_create_organization_page()

        # Navigate to Organization Edit
        organization_page.fill_organization_form(
            'Systers Open-Source Community'
        )
        # Correctness.
        self.assertEqual(
            organization_page.get_org_name(),
            'Systers Open-Source Community'
        )

    def test_create_duplicate_organization(self):
        """
        Test creation of organization with existing name.
        """
        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Navigate to Organization Edit
        organization_page.navigate_to_organization_view()
        organization_page.go_to_create_organization_page()

        # Navigate to Organization Edit
        organization_page.fill_organization_form('DuplicateOrganization')
        self.assertEqual(
            organization_page.get_org_name(),
            'DuplicateOrganization'
        )

        # Create Organization with same name
        organization_page.go_to_create_organization_page()
        organization_page.fill_organization_form('DuplicateOrganization')

        # Check error.
        self.assertEqual(
            organization_page.get_help_block().text,
            'Organization with this Name already exists.'
        )

    def test_create_invalid_organization(self):
        """
        Test creation of organization with invalid values.
        """
        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Navigate to Organization Edit
        organization_page.navigate_to_organization_view()
        organization_page.go_to_create_organization_page()

        # Navigate to Organization Edit
        organization_page.fill_organization_form(
            'Systers Open~Source Community'
        )

        # Check Error
        self.assertEqual(
            organization_page.get_organization_name_error(),
            'Enter a valid value.'
        )

    def test_edit_organization_with_invalid_value(self):
        """
        Test edit of organization with invalid values.
        """
        # Create Organization
        org = create_organization()

        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Navigate to Organization list view
        organization_page.navigate_to_organization_view()

        # Edit Organization
        self.assertEqual(
            organization_page.element_by_xpath(self.elements.EDIT_ORG).text,
            'Edit'
        )

        organization_page.go_to_edit_organization_page()
        organization_page.fill_organization_form('New~Organization')

        # Check Error
        self.assertEqual(
            organization_page.get_organization_name_error(),
            'Enter a valid value.'
        )

    def test_edit_organization_with_valid_value(self):
        """
        Test edit of organization with valid values.
        """
        # Create Organization
        org = create_organization()

        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Navigate to Organization list view
        organization_page.navigate_to_organization_view()

        # Edit Organization
        self.assertEqual(
            organization_page.element_by_xpath(self.elements.EDIT_ORG).text,
            'Edit'
        )

        organization_page.go_to_edit_organization_page()
        organization_page.fill_organization_form('New Organization')

        # Check Edited Organization
        self.assertEqual(organization_page.get_org_name(), 'New Organization')

    def test_delete_organization_without_users_linked(self):
        """
        Test deletion of organization with no users linked to it.
        """
        # Create org
        org = create_organization()

        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Navigate to Organization view
        organization_page.navigate_to_organization_view()

        # Delete Organization
        self.delete_organization_from_list()

        # Check Organization is deleted.
        with self.assertRaises(NoSuchElementException):
            organization_page.get_org_name()

    def test_delete_org_with_users_linked(self):
        """
        Test deletion of organization with users linked to it.
        """
        # Create volunteer
        volunteer = create_volunteer()

        self.organization_page.go_to_events_page()
        organization_page = self.organization_page
        organization_page.live_server_url = self.live_server_url

        # Navigate to organization view and Delete Organization
        organization_page.navigate_to_organization_view()
        self.delete_organization_from_list()

        # Check error message
        self.assertNotEqual(organization_page.get_danger_message(), None)
        self.assertEqual(
            organization_page.get_template_error_message(),
            'You cannot delete an organization that users '
            'are currently associated with.'
        )
