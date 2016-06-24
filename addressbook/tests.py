from django import test
import json

from addressbook import models;

JSON_XSSI_PREFIX = ")]}'\n"


class ServiceTests(test.TestCase):

  def setUp(self):
    # Set up two organizations ans three people, two of whome are members of
    # organization 1.
    organization_1 = self._add_organization(1)
    organization_2 = self._add_organization(2)

    person_1 = self._add_person(1)
    person_2 = self._add_person(2)
    person_3 = self._add_person(3)

    organization_1.members.add(person_1)
    organization_1.members.add(person_2)
    organization_1.save()

    self._organization_1_id = organization_1.id
    self._organization_2_id = organization_2.id

    self._person_1_id = person_1.id
    self._person_2_id = person_2.id
    self._person_3_id = person_3.id

  def _add_organization(self, i):
    contact_details = models.ContactDetails(
        email='organization%s@example.com' % i,
        phone='031-%s-%s' % (str(i) * 3, str(i) * 4),
        street_address='%s Any Street' % i,
        city='Edinburgh',
        postal_code='EH%d 1A1' % i)
    contact_details.save()

    organization = models.Organization(
        name='organization_%s' % i, contact_details=contact_details)
    organization.save()

    return organization

  def _add_person(self, i):
    contact_details = models.ContactDetails(
        email='organization%s@example.com' % i,
        phone='031-%s-%s' % (str(i) * 3, str(i) * 4),
        street_address='%s Any Road' % i,
        city='Edinburgh',
        postal_code='EH%d 1A1' % i)
    contact_details.save()

    person = models.Person(
        first_name='first_%s' % i, last_name='last_%s' % i,
        contact_details=contact_details)
    person.save()

    return person

  def _get_json_response(self, response):
    self.assertEquals(200, response.status_code)
    self.assertEquals('application/javascript', response['Content-Type'])
    self.assertTrue(response.content.startswith(JSON_XSSI_PREFIX))
    return json.loads(response.content[len(JSON_XSSI_PREFIX):])

  def _put_json(self, url, data):
    return self.client.put(url, data=json.dumps(data),
        content_type='application/javascript')

  def test_csrf_protection(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')

  def test_login_protection(self):
    # TODO(john): Implement this test
    # Note: Login protection not implemented yet
    self.fail('Implement this test')

  def test_add_member(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')

  def test_add_organization(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')

  def test_add_person(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')

  def test_delete_member(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')

  def test_delete_organization(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')

  def test_delete_person(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')

  def test_get_organization_list(self):
    response = self.client.get('/addressbook/rest/organization/all')
    data = self._get_json_response(response)
    self.assertEquals(2, len(data))
    self.assertEquals(
        [self._organization_1_id, self._organization_2_id],
        [organization['id'] for organization in data])

  def test_get_person_list(self):
    response = self.client.get('/addressbook/rest/person/all')
    data = self._get_json_response(response)
    self.assertEquals(3, len(data))
    self.assertEquals(
        [self._person_1_id, self._person_2_id, self._person_3_id],
        [person['id'] for person in data])

  def test_update_organization(self):
    expected_name = 'organization_test'
    expected_email = 'organization_test@example.com'
    expected_phone = '031-999-9999'
    expected_street_address = '1 Test Street'
    expected_city = 'Edinburgh'
    expected_postal_code = 'EH1 1T1'

    response = self._put_json(
        '/addressbook/rest/organization/%d' % self._organization_1_id,
        {
          'name': expected_name,
          'email': expected_email,
          'phone': expected_phone,
          'streetAddress': expected_street_address,
          'city': expected_city,
          'postalCode': expected_postal_code})
    self.assertEquals(
        {
            'id': str(self._organization_1_id),
            'action': 'updated', 'type': 'organization'},
        self._get_json_response(response))

    # Check the update worked
    organization = models.Organization.objects.get(id=self._organization_1_id)
    self.assertEquals(expected_name, organization.name)
    self.assertEquals(expected_email, organization.contact_details.email)
    self.assertEquals(expected_phone, organization.contact_details.phone)
    self.assertEquals(
        expected_street_address, organization.contact_details.street_address)
    self.assertEquals(expected_city, organization.contact_details.city)
    self.assertEquals(
        expected_postal_code, organization.contact_details.postal_code)

  def test_update_person(self):
    # TODO(john): Implement this test
    self.fail('Implement this test')
