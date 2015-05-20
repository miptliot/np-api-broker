from django.conf.urls import url
from . import fake_views as views

USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'
COURSE_KEY_PATTERN = r'(?P<course_key_string>[^/+]+(/|\+)[^/+]+(/|\+)[^/]+)'
COURSE_ID_PATTERN = COURSE_KEY_PATTERN.replace('course_key_string', 'course_id')

urlpatterns = [
    url(
        r'^api/user/v0/accounts/' + USERNAME_PATTERN + '$',
        views.AccountView.as_view(),
        name="accounts_api"
    ),
    url(
        r'^api/enrollment/v1/course/{course_key}$'.format(course_key=COURSE_ID_PATTERN),
        views.EnrollmentCourseDetailView.as_view(),
        name="courseenrollmentdetails"
    ),
    url(r'^api/enrollment/v1/enrollment$', views.EnrollmentListView.as_view(), name='courseenrollments'),
]
