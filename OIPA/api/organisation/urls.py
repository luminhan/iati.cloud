from django.conf.urls import url

from api.organisation import views

app_name = 'api'
urlpatterns = [
    # BEGIN: Endpoint of the Organisation File
    # - Organisation Document Link
    url(
        r'^organisation-file/(?P<organisation_identifier>[^@$&+,/:;=?]+)'
        r'/organisation-document-link-list/$',
        views.OrganisationFileOrganisationDocumentLinkList.as_view(),
        name='organisation-file-organisation-document-link-list'
    ),
    # END
    url(r'^$', views.OrganisationList.as_view(), name='organisation-list'),
    url(
        r'^(?P<pk>[^@$&+,:;=?]+)/$',
        views.OrganisationDetail.as_view(),
        name='organisation-detail'
    ),
    url(
        r'^(?P<pk>[^@$&+,/:;=?]+)/reported-activities/$',
        views.ReportedActivities.as_view(),
        name='organisation-reported-activities'
    ),
    url(
        r'^(?P<pk>[^@$&+,/:;=?]+)/participated-activities/$',
        views.ParticipatedActivities.as_view(),
        name='organisation-participated-activities'
    ),
    url(
        r'^(?P<pk>[^@$&+,/:;=?]+)/provided-transactions/$',
        views.ProvidedTransactions.as_view(),
        name='organisation-provided-transactions'
    ),
    url(
        r'^(?P<pk>[^@$&+,/:;=?]+)/received-transactions/$',
        views.ReceivedTransactions.as_view(),
        name='organisation-received-transactions'
    ),
]
