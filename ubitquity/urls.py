from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from .ubitquity.views import BillOfSaleListView, DocumentOnchainView, ApplicationForRegistrationListView, \
    SecurityGuaranteeListView, DocumentView, DocumentListCreateView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^sale/$', BillOfSaleListView.as_view(), name="create"),
    url(r'^registration/$', ApplicationForRegistrationListView.as_view(), name="create"),
    url(r'^guarantee/$', SecurityGuaranteeListView.as_view(), name="create"),
    url(r'^onchain/(?P<tx_hash>.+)/$', DocumentOnchainView.as_view()),
    url(r'^files/$', DocumentListCreateView.as_view()),
    url(r'^files/(?P<pk>.+)/$', DocumentView.as_view()),
    url(r'', include_docs_urls(title='Ubitquity Aircraft')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
