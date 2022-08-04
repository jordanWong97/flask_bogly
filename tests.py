from unittest import TestCase
from urllib import response

from app import app, db
from models import DEFAULT_IMAGE_URL, User

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Checks user page status code, and checks if test_first and test_last
        are in response html"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_process_add_form(self):
        """ Tests if new user is added into blogly_test db """
        with self.client as c:
            resp = c.post('/users/new', follow_redirects=True, data = {'first_name': 'Jor',
                                                'last_name': 'Wong',
                                                'image_url': ''})
            html = resp.get_data(as_text=True)

            user = User.query.filter_by(first_name = 'Jor').first() # need to do .first() to get actual answer!
            self.assertEqual(resp.status_code, 200) #follow redirects and check text for 'Wong'
            # self.assertEqual(user.last_name, 'Wong') instead of looking at db, check html
            self.assertIn('Wong', html)


    def test_show_add_user_form(self):
        """ Tests if we reach new user form """
        with self.client as c:
            resp = c.get('/users/new')
            html = resp.get_data(as_text= True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add New User</h1>',html)

    def test_show_user_information(self):
        """ Tests if we reach user page for test_two """
        with self.client as c:
            # id = User.query.filter_by(first_name = "test_first").first().id
            # use self.user_id instead because it's already set

            resp = c.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("test_first", html)

    def test_show_edit_page(self):
        """ Tests edit page for specified user """
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
