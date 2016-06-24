"""Holds the HTTP handlers for the addressbook app."""

from django import db
from django import http
from django.views import generic
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from addressbook import models

JSON_XSSI_PREFIX = ")]}'\n"


def json_response(data, status_code=200):
  response = http.HttpResponse()
  response.status_code = status_code
  response['Content-Type'] = 'application/javascript'

  # These three lines needed to defeat XSSI attacks
  response['X-Content-Type-Options'] = 'nosniff'
  response['Content-Disposition'] = 'attachment'
  response.content = JSON_XSSI_PREFIX + json.dumps(data)

  return response


def _update_contact_details(has_contact_details, update_dict):
  has_contact_details.email = update_dict['email']
  has_contact_details.phone = update_dict['phone']
  has_contact_details.street_address = update_dict['streetAddress']
  has_contact_details.city = update_dict['city']
  has_contact_details.postal_code = update_dict['postalCode']


@method_decorator(login_required, name='get')
class IndexView(generic.base.TemplateView):
  """Renders the base index file."""

  template_name = 'index.html'


class LoginRequiredRESTHandler(generic.View):

  def dispatch(self, *args, **kwargs):
    """Require authenticated user for all REST requests."""
    if not self.request.user.is_authenticated():
      return json_response({'status': 'Unauthorized'}, status_code=401)
    self.user = self.request.user
    return super(LoginRequiredRESTHandler, self).dispatch(*args, **kwargs)


class OrganizationListRESTHandler(LoginRequiredRESTHandler):
  """REST handler for multiple organization requests."""

  def get(self, request):
    data = [
        {
            'id': organization.id,
            'name': organization.name,
            'email': organization.email,
            'phone': organization.phone,
            'streetAddress': organization.street_address,
            'city': organization.city,
            'postalCode': organization.postal_code,
            'members': [
                {
                  'id': person.id,
                  'firstName': person.first_name,
                  'lastName': person.last_name,
                }
                for person in organization.members.filter(
                    owner=self.user).order_by('last_name', 'first_name')
            ],
        }
        for organization in models.Organization.objects.filter(
            owner=self.user).order_by('name')
    ]
    return json_response(data)


class OrganizationMembershipRESTHandler(LoginRequiredRESTHandler):
  """REST handler to manage membership of an organization."""

  @db.transaction.atomic
  def put(self, request, organization_id, person_id):
    """Add a member to an organization."""
    # TODO(john): Better error handling - get() raises if not found, but there's
    # no messaging back to the client yet
    organization = models.Organization.objects.get(
        owner=self.user, id=organization_id)
    person = models.Person.objects.get(owner=self.user, id=person_id)

    organization.members.add(person)
    organization.save()

    return json_response({
        'type': 'membership',
        'organization_id': organization_id,
        'person_id': person_id,
        'action': 'added'})

  @db.transaction.atomic
  def delete(self, request, organization_id, person_id):
    """Remove a member from an organization."""
    # TODO(john): Better error handling - get() raises if not found, but there's
    # no messaging back to the client yet
    organization = models.Organization.objects.get(
        owner=self.user, id=organization_id)
    person = models.Person.objects.get(owner=self.user, id=person_id)

    organization.members.remove(person)
    organization.save()

    return json_response({
        'type': 'membership',
        'organization_id': organization_id,
        'person_id': person_id,
        'action': 'deleted'})


class OrganizationRESTHandler(LoginRequiredRESTHandler):
  """REST handler for single organization requests."""

  def get(self, request, organization_id):
    raise NotImplementedError()

  @db.transaction.atomic
  def post(self, request):
    """Adds a new organization."""
    organization = models.Organization(owner=self.user)

    # TODO(john): Server-side data validation before blindly copying the data
    # into the target object
    self._update_organization(organization, json.loads(request.body))

    return json_response(
        {'type': 'organization', 'id': organization.id, 'action': 'added'})

  @db.transaction.atomic
  def put(self, request, organization_id):
    """Receives updates to an existing organization."""
    # TODO(john): Better error handling - get() raises if not found, but there's
    # no messaging back to the client yet
    organization = models.Organization.objects.get(
        owner=self.user, id=organization_id)

    # TODO(john): Server-side data validation before blindly copying the data
    # into the target object
    self._update_organization(organization, json.loads(request.body))

    return json_response(
        {'type': 'organization', 'id': organization_id, 'action': 'updated'})

  @db.transaction.atomic
  def delete(self, request, organization_id):
    """Delete an organization."""
    organization = models.Organization.objects.get(
        owner=self.user, id=organization_id)
    organization.delete()

    return json_response(
        {'type': 'organization', 'id': organization_id, 'action': 'deleted'})

  def _update_organization(self, organization, update_dict):
    organization.name = update_dict['name']
    _update_contact_details(organization, update_dict)
    organization.save()


class PersonListRESTHandler(LoginRequiredRESTHandler):
  """REST handler for multiple person requests."""

  def get(self, request):
    data = [
        {
            'id': person.id,
            'firstName': person.first_name,
            'lastName': person.last_name,
            'email': person.email,
            'phone': person.phone,
            'streetAddress': person.street_address,
            'city': person.city,
            'postalCode': person.postal_code,
        }
        for person in models.Person.objects.filter(owner=self.user)
    ]
    return json_response(data)


class PersonRESTHandler(LoginRequiredRESTHandler):
  """REST handler for single person requests."""

  def get(self, request, person_id):
    raise NotImplementedError()

  @db.transaction.atomic
  def post(self, request):
    """Adds a new person."""
    person = models.Person(owner=self.user)

    # TODO(john): Server-side data validation before blindly copying the data
    # into the target object
    self._update_person(person, json.loads(request.body))

    return json_response(
        {'type': 'person', 'id': person.id, 'action': 'added'})

  @db.transaction.atomic
  def put(self, request, person_id):
    """Receives updates to an existing person."""
    # TODO(john): Better error handling - get() raises if not found, but there's
    # no messaging back to the client yet
    person = models.Person.objects.get(owner=self.user, id=person_id)

    # TODO(john): Server-side data validation before blindly copying the data
    # into the target object
    self._update_person(person, json.loads(request.body))

    return json_response(
        {'type': 'person', 'id': person_id, 'action': 'updated'})

  @db.transaction.atomic
  def delete(self, request, person_id):
    """Delete a person."""
    person = models.Person.objects.get(owner=self.user, id=person_id)
    person.delete()

    return json_response(
        {'type': 'person', 'id': person_id, 'action': 'deleted'})

  def _update_person(self, person, update_dict):
    person.first_name = update_dict['firstName']
    person.last_name = update_dict['lastName']
    _update_contact_details(person, update_dict)
    person.save()
