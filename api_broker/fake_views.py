# coding: utf-8
import datetime

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
