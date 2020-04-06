from django.test import TestCase
from rest_framework.test import APIRequestFactory
from referral.models import (Page, Referrer)
from referral.api import (getTest, getPage, creditReferrer)

# Reusable function for populating database with page and referrer to test
def populateTestDatabase():
    Page.objects.create(name='test_page', owner='test_user')
    test_page = Page.objects.get(name='test_page')
    Referrer.objects.create(name='test_referrer', link='test_link', page=test_page)


# Test that Page and Referrer have a foreign key relationship
class ForeignKeyTestCase(TestCase):
    def setUp(self):
        """create foreign key relationship between test_page and test_referrer"""
        populateTestDatabase()
        
    def test_foriegn_key(self):
        """test_referrer is linked to test_page by a foreign key"""
        referrer = Referrer.objects.get(name='test_referrer')
        page = Page.objects.get(pk=referrer.page.pk)
        self.assertEqual(page.name, 'test_page')


# Test that the getTest endpoint returns a JSON message
class TestEndpointTestCase(TestCase):
    def setUp(self):
        """create an APIRequestFactory to GET from"""
        self.factory = APIRequestFactory()

    def testEndpoint(self):
        """getTest should return a JSON message about the API with status code 200"""
        request = self.factory.get('/api/referral/test')
        response = getTest(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'API is live'}
        )


# Test that the getPage endpoint returns a JSON message with page data
class PageEndpointTestCase(TestCase):
    def setUp(self):
        """create an APIRequestFactory to GET from and populate database"""
        self.factory = APIRequestFactory()
        populateTestDatabase()

    def testEndpoint(self):
        """getPage should return a message with page name, referrer name, count, and status code 200"""
        request = self.factory.get('/api/referral/page')
        response = getPage(request)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_page')
        self.assertContains(response, 'test_referrer')
        self.assertContains(response, 'count')


# Test that the creditReferrer endpoint increments affiliate count by 1
class CreditEndpointTestCase(TestCase):
    def setUp(self):
        """create an APIRequestFactory to POST and populate database"""
        self.factory = APIRequestFactory()
        populateTestDatabase()

    def testEndpoint(self):
        """creditReferrer should increment test_referrer count to 1"""
        # test that count is 0
        referrer = Referrer.objects.get(name='test_referrer')
        self.assertEqual(referrer.count, 0)
        # POST to creditReferrer
        request = self.factory.post('/api/referral/page', 
                                    {'page_id': 1, "link": "test_link"}, 
                                    format='json')
        response = creditReferrer(request)
        # test for positive response and increased count
        self.assertEqual(response.status_code, 200)
        referrer = Referrer.objects.get(name='test_referrer')
        self.assertEqual(referrer.count, 1)
