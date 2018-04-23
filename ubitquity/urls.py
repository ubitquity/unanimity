from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .ubitquity.views import BillOfSaleListView, DocumentOnchainView, ApplicationForRegistrationListView, SecurityGuaranteeListView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^sale/$', BillOfSaleListView.as_view(), name="create"),
    url(r'^registration/$', ApplicationForRegistrationListView.as_view(), name="create"),
    url(r'^guarantee/$', SecurityGuaranteeListView.as_view(), name="create"),
    url(r'^onchain/(?P<tx_hash>.+)/$', DocumentOnchainView.as_view()),
    url(r'', include_docs_urls(title='Ubitquity Aircraft')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
