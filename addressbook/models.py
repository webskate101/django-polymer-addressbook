"""Holds the ORM models for the address book."""

from django.contrib.auth import models as auth_models
from django.db import models

DEFAULT_MAX_CHAR_FIELD_LEN = 255
DEFAULT_OPTIONAL_CHAR_FIELD_OPTS = {
  'blank': True,
  'max_length': DEFAULT_MAX_CHAR_FIELD_LEN,
  'null': True,
}
DEFAULT_REQUIRED_CHAR_FIELD_OPTS = {
  'blank': True,
  'max_length': DEFAULT_MAX_CHAR_FIELD_LEN,
  'null': True,
}


class HasContactDetails(models.Model):
  """Models the contact details used by a person or organization."""

  email = models.EmailField(**DEFAULT_OPTIONAL_CHAR_FIELD_OPTS)
  phone = models.CharField(**DEFAULT_OPTIONAL_CHAR_FIELD_OPTS)

  # Addresses, like names, dates, and times, are very hard to get right. If at
  # all possible the best thing is to find a well-maintained library which has
  # thought through all the hard issues which you probably don't want to have to
  # touch. This model here isn't even remotely good enough to model all UK
  # addresses, never mind other countries'.
  # See: https://www.mjt.me.uk/posts/falsehoods-programmers-believe-about-addresses/

  street_address = models.CharField(**DEFAULT_OPTIONAL_CHAR_FIELD_OPTS)
  city = models.CharField(**DEFAULT_OPTIONAL_CHAR_FIELD_OPTS)
  postal_code = models.CharField(**DEFAULT_OPTIONAL_CHAR_FIELD_OPTS)


class Person(HasContactDetails):
  """Models a person."""

  # Names are notoriously difficult to get right and in any real production
  # system this simple (first_name, last_name) structure will not do. In a toy
  # system like this, it's tempting to just have a single "name" field, but I
  # decided to split it into two fields here because that way we at least have
  # the possibility of sorting by last name, which is a desirable feature.
  # See: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/

  owner = models.ForeignKey(
      auth_models.User, null=False,on_delete=models.CASCADE)
  first_name = models.CharField(**DEFAULT_REQUIRED_CHAR_FIELD_OPTS)
  last_name = models.CharField(**DEFAULT_REQUIRED_CHAR_FIELD_OPTS)


class Organization(HasContactDetails):
  """Models an orgnaization."""

  owner = models.ForeignKey(
      auth_models.User, null=False,on_delete=models.CASCADE)
  name = models.CharField(**DEFAULT_REQUIRED_CHAR_FIELD_OPTS)
  members = models.ManyToManyField(Person, related_name='organization')
