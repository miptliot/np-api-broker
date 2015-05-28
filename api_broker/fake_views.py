# coding: utf-8
import datetime

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
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


class CourseViewMixin(object):
    pass


class CourseList(CourseViewMixin, APIView):
    """
        **Варианты использования**

            Получить список всех курсов на платформе; список разбит на части по 10 курсов в каждой.

            Получить информацию о курсах с заданными ID.

        **Примеры запросов**

            GET /api/course_structure/v1/courses/

            GET /api/course_structure/v1/courses/?course_id={course_id1},{course_id2}


        **Поля ответа**

            * count: Количество курсов на платформе (всего курсов).

            * next: Адрес (URI) следующей страницы с курсами.

            * previous: Адрес (URI) предыдущей страницы курсов

            * num_pages: Количество страниц.

            * results: Список курсов, описание каждого из которого включает.

                * id: Уникальный идентификатор курса.

                * name: Название курса.

                * category: Тип контента, в данном случае “course”.

                * org: Организация (университет-участник), добавившая курс.

                * run: Идентификатор сессии курса.

                * course: Номер курса (в кодировании университета-участника).

                * uri: Адрес для получения деталей курса.

                * image_url: Адрес изображения-обложки курса.

                * start: Дата и время начала курса.

                * end: Дата и время окончания, если не определена то NULL.

    """
    # paginate_by = 10
    # paginate_by_param = 'page_size'
    # pagination_serializer_class = PaginationSerializer
    # serializer_class = serializers.CourseSerializer


    def get(self, request):
        import requests
        from django.conf import settings
        requests.post('http://edx.mipt.ru/oauth2/access_token/')
        result = requests.get(
            '{0}/api/course_structure/v0/courses/?{1}'.format(
                settings.PLATFORM_URL,
                '9e819bf8d746ea95a136'
            ),
        )
        return Response(result)
        course_ids = self.request.QUERY_PARAMS.get('course_id', None)
        if not course_ids:
            result = {
                "count": 2,
                "next": "https://courses.edx.org/api/course_structure/v0/courses/?page=3",
                "previous": "https://courses.edx.org/api/course_structure/v0/courses/?page=1",
                "num_pages": 1,
                "results": [
                    {
                        "id": "ANUx/ANU-ASTRO1x/1T2014",
                        "name": "Greatest Unsolved Mysteries of the Universe",
                        "category": "course",
                        "org": "ANUx",
                        "run": "1T2014",
                        "course": "ANU-ASTRO1x",
                        "uri": "https://courses.edx.org/api/course_structure/v0/courses/ANUx/ANU-ASTRO1x/1T2014/",
                        "image_url": "/c4x/ANUx/ANU-ASTRO1x/asset/dome_dashboard.jpg",
                        "start": "2014-03-24T18:30:00Z",
                        "end": None
                    },
                    {
                        "id": "ANUx/ANU-ASTRO4x/1T2015",
                        "name": "COSMOLOGY",
                        "category": "course",
                        "org": "ANUx",
                        "run": "1T2015",
                        "course": "ANU-ASTRO4x",
                        "uri": "https://courses.edx.org/api/course_structure/v0/courses/ANUx/ANU-ASTRO4x/1T2015/",
                        "image_url": "/c4x/ANUx/ANU-ASTRO4x/asset/ASTRO4x_dashboard_image.jpeg",
                        "start": "2015-02-03T00:00:00Z",
                        "end": "2015-04-28T23:30:00Z"
                    }
                ]
            }
        return Response(result)

    # def get_queryset(self):
    #     course_ids = self.request.QUERY_PARAMS.get('course_id', None)
    #
    #     results = []
    #     if course_ids:
    #         course_ids = course_ids.split(',')
    #         for course_id in course_ids:
    #             # course_key = CourseKey.from_string(course_id)
    #             # course_descriptor = courses.get_course(course_key)
    #             results.append(course_descriptor)
    #     else:
    #         results = modulestore().get_courses()
    #
    #     # Ensure only course descriptors are returned.
    #     results = (course for course in results if course.scope_ids.block_type == 'course')
    #
    #     # Ensure only courses accessible by the user are returned.
    #     results = (course for course in results if self.user_can_access_course(self.request.user, course))
    #
    #     # Sort the results in a predictable manner.
    #     return sorted(results, key=lambda course: unicode(course.id))


class CourseDetail(CourseViewMixin, APIView):
    """
        **Вариант использования**

            Получить информацию о курсе по его ID.

        **Примеры запросов**

            GET /api/course_structure/v1/courses/{course_id}/


        ** Внимание!!!**

            Есть изменения по отношению к API Open edX!

            Для этого метода данные предоставляет модуль PLP (каталог курсов)

        **Поля ответа**

            * id: Уникальный идентификатор курса.

            * name: Название курса.

            * category: Тип контента, в данном случае “course”.

            * org: Организация (университет-участник), добавившая курс.

            * run: Идентификатор сессии курса.

            * course: Номер курса (в кодировании университета-участника).

            * uri: Адрес для получения деталей курса.

            * image_url: Адрес изображения-обложки курса.

            * prerequisites: Требования к начальному уровню знаний

            * areas: Предполагаемые целевые УГСН

            * competencies: Компетенции, на получение которых рассчитан курс.

            * learn_results: Планируемые результаты обучения.

            * start: Дата и время начала курса.

            * end: Дата и время окончания, если не определена то NULL.
    """
    # serializer_class = serializers.CourseSerializer

    def get(self, request, course_id=None):
        if course_id:
            result = {
                "id": course_id,
                "name": "Greatest Unsolved Mysteries of the Universe",
                "category": "course",
                "org": "ANUx",
                "run": "1T2014",
                "course": "ANU-ASTRO1x",
                "uri": "https://courses.edx.org/api/course_structure/v0/courses/ANUx/ANU-ASTRO1x/1T2014/",
                "image_url": "/c4x/ANUx/ANU-ASTRO1x/asset/dome_dashboard.jpg",
                "prerequisites": u'Требования к начальному уровню знаний',
                "areas": u'Предполагаемые целевые УГСН',
                "competencies": u'Компетенции, на получение которых рассчитан курс',
                "learn_results": u'Планируемые результаты обучения',
                "start": "2014-03-24T18:30:00Z",
                "end": None
            }
        else:
            return Response(status.HTTP_200_OK)
        return Response(result)


class CourseStructure(CourseViewMixin, APIView):
    """
        **Варианты использования**

            Возвращает структуру курса и список его содержимого,
            который доступен пользователю на текущем этапе обучения.

        **Примеры запросов**

            GET /api/course_structure/v1/course_structures/{course_id}/

        **Поля ответа**

            * root: Идентификатор корневого элемента.

            * blocks: Список элементов курса, описание каждого из которого включает:

            * id: Идентификатор элемента.

            * type: Тип блока, возможные варианты: sequential, vertical, html, problem, video, и discussion.
            Кроме того, может быть использован тип блока, который создан автором курса при добавлении курса.

            * display_name: Название элемента.

            * graded: Оценивается ли этот блок (булево).

            * format: Тип задания (если graded == false, то null).

            * children: Если у элемента есть потомки, то список идентификаторов элементов-потомков.
    """

    def get(self, request, **kwargs):
        result = {
            "root": "i4x://ANUx/ANU-INDIA1x/course/1T2014",
            "blocks": {
                "i4x://ANUx/ANU-INDIA1x/html/834f845ae8b944f1882f14ce6417c9d1": {
                    "id": "i4x://ANUx/ANU-INDIA1x/html/834f845ae8b944f1882f14ce6417c9d1",
                    "type": "html",
                    "display_name": "",
                    "graded": False,
                    "format": None,
                    "children": []
                },
                "i4x://ANUx/ANU-INDIA1x/html/c3493aaebaba4ab6a0499fbc27ac3b0e": {
                    "id": "i4x://ANUx/ANU-INDIA1x/html/c3493aaebaba4ab6a0499fbc27ac3b0e",
                    "type": "problem",
                    "display_name": "Check your learning - Part 1",
                    "graded": True,
                    "format": None,
                    "children": []
                },
                "i4x://ANUx/ANU-INDIA1x/sequential/3731eee6a39c473c98ef6a5c3f56c04c": {
                    "id": "i4x://ANUx/ANU-INDIA1x/sequential/3731eee6a39c473c98ef6a5c3f56c04c",
                    "type": "sequential",
                    "display_name": "Reflective project",
                    "graded": True,
                    "format": "Reflective Project",
                    "children": [
                        "i4x://ANUx/ANU-INDIA1x/vertical/efe3f47a5bc24894b726c229d6bf5968",
                        "i4x://ANUx/ANU-INDIA1x/vertical/9106a1b1fad040858bad56fe5d48074e",
                        "i4x://ANUx/ANU-INDIA1x/vertical/27d2cf635bd44038a1207461b761a63a",
                        "i4x://ANUx/ANU-INDIA1x/vertical/94b719b765b046e2a811f1c4e4f84e5b"
                    ]
                },
                "i4x://ANUx/ANU-INDIA1x/vertical/0a3cd583cb1d4108bfbdaf57c511da3a": {
                    "id": "i4x://ANUx/ANU-INDIA1x/vertical/0a3cd583cb1d4108bfbdaf57c511da3a",
                    "type": "vertical",
                    "display_name": "What you need to do this week",
                    "graded": False,
                    "format": None,
                    "children": [
                        "i4x://ANUx/ANU-INDIA1x/html/a20abbba4a0f4a578d96cbdd4b34307b"
                    ]
                },
            }
        }
        return Response(result)
        # try:
        #     return Response(api.course_structure(self.course_key))
        # except CourseStructureNotAvailableError:
        #     # If we don't have data stored, we will try to regenerate it, so
        #     # return a 503 and as them to retry in 2 minutes.
        #     return Response(status=503, headers={'Retry-After': '120'})


class CourseGradingPolicy(CourseViewMixin, APIView):
    """
        **Варианты использования**

            Получить политику оценивания курса

            Возвращает типы тестовых заданий, их вклад в общую оценку и их дополнительные параметры для заданного курса.

        **Примеры запросов**

            GET /api/course_structure/v1/grading_policies/{course_id}/

        **Поля ответа**

            Список значений, содержащих следующие поля:

            * assignment_type: Тип задания в виде, который определил автор курса, например,
            “домашнее задание”, “опрос”, “финальный экзамен”.

            * count: Количество возможных попыток для прохождения задания данного типа.

            * dropped: Количество худших попыток, отбрасываемых для заданий данного типа.

            * weight:  Вес результата заданий данного типа в общей оценке пользователя.
    """

    allow_empty = False

    def get(self, request, **kwargs):

        result = [
            {
                "assignment_type": "Week 1 Survey",
                "count": 2,
                "dropped": 1,
                "weight": 0.03
            },
            {
                "assignment_type": "Week 5 Survey",
                "count": 2,
                "dropped": 1,
                "weight": 0.03
            },
            {
                "assignment_type": "Reflective Project",
                "count": 1,
                "dropped": 0,
                "weight": 0.2
            },
        ]

        return Response(result)
        # return Response(api.course_grading_policy(self.course_key))

"""
Получить обновления  курса
GET /api/course_structure/v1/updates/{course_id}/
Возвращает блоки курса, которые стали доступны после последнего вызова метода.
Поля ответа
·         root: Идентификатор корневого элемента.
id: Идентификатор элемента.
type: Тип блока, возможные варианты: sequential, vertical, html, problem, video, и discussion. Кроме того, может быть использован тип блока, который создан автором курса при добавлении курса.
display_name: Название элемента.
graded: Оценивается ли этот блок (булево).
format: Тип задания (если graded == false, то null).
children: Если у элемента есть потомки, то список идентификаторов элементов-потомков.
"""
