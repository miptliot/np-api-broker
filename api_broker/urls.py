from django.conf.urls import url
from . import fake_views as views

USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'

urlpatterns = [
    url(
        r'^api/user/v0/accounts/' + USERNAME_PATTERN + '$',
        views.AccountView.as_view(),
        name="accounts_api"
    ),
]
