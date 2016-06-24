from django.conf.urls import url

from addressbook import views

app_name = 'addressbook'
urlpatterns = [
  url(r'^$', views.IndexView.as_view()),
  url(r'^rest/organization$', views.OrganizationRESTHandler.as_view()),
  url(r'^rest/organization/([0-9]+)$', views.OrganizationRESTHandler.as_view()),
  url(r'^rest/organization/all$', views.OrganizationListRESTHandler.as_view()),
  url(
      r'^rest/organization/([0-9]+)/member/([0-9]+)$',
      views.OrganizationMembershipRESTHandler.as_view()),
  url(r'^rest/person$', views.PersonRESTHandler.as_view()),
  url(r'^rest/person/([0-9]+)$', views.PersonRESTHandler.as_view()),
  url(r'^rest/person/all$', views.PersonListRESTHandler.as_view()),
]
