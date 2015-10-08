from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.test import TestCase


class AccountTest(TestCase):
    def test_account(self):
        # Check not fully filled data
        data = {
            'number': 100, 'name': 'fake', 'account': 100, 'bank': 1
        }
        response = self.client.post(reverse('account'), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(content, {'currency': ['This field is required.']})
        # Check create account
        data['currency'] = 'rub'
        response = self.client.post(reverse('account'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json.loads(response.content), {})
        # Check list account
        response = self.client.get(reverse('accounts'))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['items']), 1)
        # Check 404 detail account
        response = self.client.get(reverse('account', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)
        # Check detail account
        response = self.client.get(reverse('account', kwargs={'pk': 1}))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(content['fields'], data)
        # Check update account without key
        response = self.client.put(reverse('account'), data=data)
        self.assertEqual(response.status_code, 400)
        # Check 404 update account
        response = self.client.put(
            reverse('account', kwargs={'pk': 100}), data=data
        )
        self.assertEqual(response.status_code, 404)
        # Check update account
        data['currency'] = 'usd'
        response = self.client.put(
            reverse('account', kwargs={'pk': 1}), data=data
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(content, {})
        # Check is data changed
        response = self.client.get(reverse('account', kwargs={'pk': 1}))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(content['fields'], data)
        self.assertEqual(content['fields']['currency'], 'usd')
        # Check delete account without key
        response = self.client.delete(reverse('account'))
        self.assertEqual(response.status_code, 400)
        # Check 404 delete account
        response = self.client.delete(reverse('account', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)
        # Check delete account
        response = self.client.delete(reverse('account', kwargs={'pk': 1}))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(content, {})
        # Check is account deleted
        response = self.client.get(reverse('account', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('accounts'))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['items']), 0)

    def test_search_account(self):
        data_one = {
            'number': 100,
            'name': 'fake',
            'account': 100,
            'bank': 1,
            'currency': 'rub'
        }
        data_two = {
            'number': 101,
            'name': 'fake',
            'account': 100,
            'bank': 1,
            'currency': 'usd'
        }
        self.client.post(reverse('account'), data=data_one)
        self.client.post(reverse('account'), data=data_two)
        # AND
        response = self.client.get(
            reverse('accounts'), data={'fl[currency]': 'usd'}
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['items']), 1)
        # OR
        response = self.client.get(
            reverse('accounts'), data={
                'fl[currency]': 'usd', 'fl[number]': 100, 'fl[_op]': 'or'
            }
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content['items']), 2)
