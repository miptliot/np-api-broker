# coding: utf-8
import datetime

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class AccountView(APIView):
    """
        **Где используется**

            Получить или изменить информацию о пользователе. Изменение происходит слиянием.

        **Получить информацию о пользователе**

            GET /api/user/v0/accounts/{username}/[?view=shared]

            Получить информацию о пользователе по имени. В зависимости от того, кто вызывает этот метод
            (обычный пользователь или администратор), и в отношении кого (для своей учетной записи,
            или учетной записи другого пользователя), состав полей может быть различным.
            Конкретный состав полей для каждого случая определяется системным администратором в настройках системы.
            При указании параметра view=shared и вызове метода в отношении другого пользователя,
            в результат включаются только те поля, значения которых совпадают со значениями соответствующих полей
            профиля вызывающего пользователя.

            Поля ответа:

            * username: Имя пользователя в системе.

            * name: ФИО пользователя.

            * email: Подтвержденная электронная почта пользователя.

            * date_joined: дата и время создания аккаунта.

            * gender: Пол. Возможные значения:

                * “m” - мужской
                * “f” - женский
                * “o” - другое
                * null

            * level_of_education: уровень образования. Возможные значения:

                * “p”: Кандидат или доктор наук, PhD
                * “m”: Магистр
                * “b”: Бакалавр
                * “s”: Специалист
                * “hs”: Полное общее образование
                * “jhs”:Основное общее образование
                * “el”: Начальное общее образование
                * “none”: Без образования
                * “o”: Другое
                * null: Пользователь не указал значение.

            * org: Университет пользователя (может быть null).

            * language: Предпочитаемый язык или null.

            * country: Код страны (ISO 3166) или null.

            * city:  Город

            * mailing_address: Почтовый адрес (текст).

            * goals: Цели пользователя (текст), null если пользователь не указал значения.


        **Изменить информацию о пользователе**

            PATCH /api/user/v0/accounts/{username}/{“key”:”value”} “application/merge-patch+json”

        **Вариант использования**

            Изменить информацию профиля пользователя.

        **Ответ**

            Пользователь может модифицировать только собственный профиль.
            При попытке внести изменения в чужой профиль возвращается ошибка 404.
            Поля профиля валидируются после изменения.
            В случае ошибки валидации возвращается ошибка 400, изменения в профиль не вносятся.
            В случае корректного изменения профиля возвращается код 204 без дополнительной информации.

    """
    # authentication_classes = (OAuth2AuthenticationAllowInactiveUser, SessionAuthenticationAllowInactiveUser)
    # permission_classes = (permissions.IsAuthenticated,)
    # parser_classes = (MergePatchParser,)

    def get(self, request, username):
        """
        GET /api/user/v1/accounts/{username}/
        """
        # try:
        #     account_settings = get_account_settings(request.user, username, view=request.QUERY_PARAMS.get('view'))
        #     # Account for possibly relative URLs.
        #     for key, value in account_settings['profile_image'].items():
        #         if key.startswith(PROFILE_IMAGE_KEY_PREFIX):
        #             account_settings['profile_image'][key] = request.build_absolute_uri(value)
        # except UserNotFound:
        #     return Response(status=status.HTTP_403_FORBIDDEN if request.user.is_staff else status.HTTP_404_NOT_FOUND)
        account_settings = dict()

        account_settings['username'] = username
        account_settings['name'] = u'Иванов Иван Иванович'
        account_settings['email'] = u'{0}@example.ru'.format(username)
        account_settings['date_joined'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account_settings['gender'] = u'm'
        account_settings['level_of_education'] = u'm'
        account_settings['language'] = u'Russian'
        account_settings['country'] = None
        account_settings['city'] = u'Долгопрудный'
        account_settings['mailing_address'] = u'На деревню дедушке'
        account_settings['goals'] = None

        return Response(account_settings)

    def patch(self, request, username):
        """
        PATCH /api/user/v1/accounts/{username}/

        Note that this implementation is the "merge patch" implementation proposed in
        https://tools.ietf.org/html/rfc7396. The content_type must be "application/merge-patch+json" or
        else an error response with status code 415 will be returned.
        """
        # try:
        #     with transaction.commit_on_success():
        #         update_account_settings(request.user, request.DATA, username=username)
        # except UserNotAuthorized:
        #     return Response(status=status.HTTP_403_FORBIDDEN if request.user.is_staff else status.HTTP_404_NOT_FOUND)
        # except UserNotFound:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # except AccountValidationError as err:
        #     return Response({"field_errors": err.field_errors}, status=status.HTTP_400_BAD_REQUEST)
        # except AccountUpdateError as err:
        #     return Response(
        #         {
        #             "developer_message": err.developer_message,
        #             "user_message": err.user_message
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        #
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_200_OK)


class ApiKeyPermissionMixIn(object):
    """
    This mixin is used to provide a convenience function for doing individual permission checks
    for the presence of API keys.
    """
    def has_api_key_permissions(self, request):
        """
        Checks to see if the request was made by a server with an API key.

        Args:
            request (Request): the request being made into the view

        Return:
            True if the request has been made with a valid API key
            False otherwise
        """
        #return ApiKeyHeaderPermission().has_permission(request, self)
        return True


def fake_course_details(course_id):
    course_detail = dict()
    course_detail['course_id'] = course_id
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    course_detail['enrollment_start'] = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    course_detail['enrollment_end'] = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
    course_detail['invite_only'] = False
    course_modes = dict()
    course_modes['slug'] = 'honor'
    course_modes['name'] = 'Honor Code Certificate'
    course_modes['expiration_datetime'] = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
    course_modes['description'] = u'Самый лучший курс'
    course_detail['course_modes'] = [course_modes]
    return course_detail


class EnrollmentCourseDetailView(APIView, ApiKeyPermissionMixIn):
    """

        **Получить детали записи на курс**

            GET /api/enrollment/v1/course/{course_id}

        **Вариант использования**

            Получить детали записи на курс по ID курса.
            Аутентификация не требуется.

        **Поля ответа**

            * course_id: Уникальный идентификатор курса.

            * enrollment_end: Дата и время, после которого запись на курс будет закрыта.

            * enrollment_start: Дата и время, начиная с которого можно записываться на курс.

            * invite_only: Требуется ли для записи на курс приглашение, булево значение.

            * course_modes: Список режимов записи на курс. Каждый режим включает следующие поля:

                * slug: Короткое имя режима записи на курс.
                * name: Полное имя режима записи.
                * expiration_datetime: Дата и время, после которого пользователь не может быть записан на курс
                в выбранном режиме.
                * description: Описание режима записи на курс.
    """
    def get(self, request, course_id=None):
        """Read enrollment information for a particular course.

        HTTP Endpoint for retrieving course level enrollment information.

        Args:
            request (Request): To get current course enrollment information, a GET request will return
                information for the specified course.
            course_id (str): URI element specifying the course location. Enrollment information will be
                returned.

        Return:
            A JSON serialized representation of the course enrollment details.

        """
        # try:
        #     return Response(api.get_course_enrollment_details(course_id))
        # except CourseNotFoundError:
        #     return Response(
        #         status=status.HTTP_400_BAD_REQUEST,
        #         data={
        #             "message": (
        #                 u"No course found for course ID '{course_id}'"
        #             ).format(course_id=course_id)
        #         }
        #     )
        return Response(fake_course_details(course_id))


def fake_enrollments_list(username):
    created = datetime.datetime.now() - datetime.timedelta(days=15)
    mode = 'honor'
    is_active = True
    enrollments_list = []
    for course_number in xrange(3):
        enrollment_info = dict()
        enrollment_info['created'] = created
        enrollment_info['mode'] = mode
        enrollment_info['is_active'] = is_active

        course_id = 'mipt/{0}/best'.format(course_number)
        enrollment_info['course_details'] = fake_course_details(course_id)
        enrollment_info['user'] = username

        enrollments_list.append(enrollment_info)
    return enrollments_list


def fake_add_enrollment(user_id, course_id, mode='honor', is_active=True):
    created = datetime.datetime.now() - datetime.timedelta(days=15)
    enrollment_info = dict()
    enrollment_info['created'] = created
    enrollment_info['mode'] = mode
    enrollment_info['is_active'] = is_active
    enrollment_info['course_details'] = fake_course_details(course_id)
    enrollment_info['user'] = user_id
    return enrollment_info


class EnrollmentListView(APIView, ApiKeyPermissionMixIn):

    """
        **Варианты использования**

            1. Просмотреть курсы, на которые записан пользователь

            2. Записать пользователя на курс

        **Примеры запросов**

            GET /api/enrollment/v1/enrollment

            POST /api/enrollment/v1/enrollment{“mode”: “honor”, “course_details”:{“course_id”: “edX/DemoX/Demo_Course”}}

        **Параметры POST запроса**

            * mode: режим записи на курс (короткое имя режима)

            * course details: Список курсов:

                * course_id: Уникальный идентификатор курса в рамках платформы.

            * email_opt_in: Опциональный флаг, показывающий согласен ли пользователь получать уведомления
            по электронной почте от авторов курса, может быть 1 или 0;

        **Поля ответа**

            Список курсов, на которые подписан пользователь (для GET запроса) или
            подробности только что оформленной подписки (для POST запроса):

                * created: Дата создания аккаунта пользователя.

                * mode: Режим записи пользователя на курс.

                * is_active: Активна ли подписка на курс.

                * course_details: Список, который включает следующие поля:

                    * course_id: Уникальный идентификатор курса.

                    * enrollment_end: Дата и время, после которого запись на курс будет закрыта.

                    * enrollment_start: Дата и время, начиная с которого можно записываться на курс.

                    * invite_only: Требуется ли для записи на курс приглашение, булево значение.

                    * course_modes: Список режимов записи на курс. Каждый режим включает следующие поля:

                        * slug: Короткое имя режима записи на курс.
                        * name: Полное имя режима записи.
                        * expiration_datetime: Дата и время, после которого пользователь не может быть записан на курс в выбранном режиме.
                        * description: Описание режима записи на курс.

                * user: Уникальный идентификатор пользователя.

    """

    # Since the course about page on the marketing site
    # uses this API to auto-enroll users, we need to support
    # cross-domain CSRF.
    # @method_decorator(ensure_csrf_cookie_cross_domain)
    def get(self, request):
        """
            Gets a list of all course enrollments for the currently logged in user.
        """
        username = request.GET.get('user', request.user.username)
        if request.user.username != username and not self.has_api_key_permissions(request):
            # Return a 404 instead of a 403 (Unauthorized). If one user is looking up
            # other users, do not let them deduce the existence of an enrollment.
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            return Response(fake_enrollments_list(username))
            # return Response(api.get_enrollments(username))
        # except CourseEnrollmentError:
        #     return Response(
        #         status=status.HTTP_400_BAD_REQUEST,
        #         data={
        #             "message": (
        #                 u"An error occurred while retrieving enrollments for user '{username}'"
        #             ).format(username=username)
        #         }
        #     )
        except:
            pass

    def post(self, request):
        print(request.DATA)
        username = request.DATA.get('user', request.user.username)
        if not username:
            username = request.user.username
        course_id = request.DATA.get('course_details', {}).get('course_id')
        if not course_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": u"Course ID must be specified to create a new enrollment."}
            )
        mode = request.DATA.get('mode', 'honor')

        return Response(fake_add_enrollment(username, unicode(course_id), mode))
