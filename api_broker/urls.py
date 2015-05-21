from django.conf.urls import url
from . import fake_views as views

USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'
COURSE_KEY_PATTERN = r'(?P<course_key_string>[^/+]+(/|\+)[^/+]+(/|\+)[^/]+)'
COURSE_ID_PATTERN = COURSE_KEY_PATTERN.replace('course_key_string', 'course_id')

urlpatterns = [
    # API accounts
    url(
        r'^api/user/v0/accounts/' + USERNAME_PATTERN + '$',
        views.AccountView.as_view(),
        name="accounts_api"
    ),

    # API enrollment
    url(
        r'^api/enrollment/v1/course/{course_key}$'.format(course_key=COURSE_ID_PATTERN),
        views.EnrollmentCourseDetailView.as_view(),
        name="courseenrollmentdetails"
    ),
    url(
        r'^api/enrollment/v1/enrollment$',
        views.EnrollmentListView.as_view(),
        name='courseenrollments'
    ),

    # API course structure
    url(
        r'^api/course_structure/v1/courses/$',
        views.CourseList.as_view(),
        name='list'
    ),
    url(
        r'^api/course_structure/v1/courses/{}/$'.format(COURSE_ID_PATTERN),
        views.CourseDetail.as_view(),
        name='detail'
    ),
    url(
        r'^api/course_structure/v1/course_structures/{}/$'.format(COURSE_ID_PATTERN),
        views.CourseStructure.as_view(),
        name='structure'
    ),
    url(
        r'^api/course_structure/v1/grading_policies/{}/$'.format(COURSE_ID_PATTERN),
        views.CourseGradingPolicy.as_view(),
        name='grading_policy'
    ),
]
