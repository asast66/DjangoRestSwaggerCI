from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from datetime import datetime
from django.conf import settings

current_date = datetime.now()
current_date_str = datetime.strftime(current_date, '%d.%m.%Y %H:%M:%S')

user_response = openapi.Response('response_description', schema=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'type': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, enum=[18, 19, 20, 21, 22, 23, 24, 'UNDEFINED']),
            'name': openapi.Schema(type=openapi.TYPE_STRING, enum=[
                'Следование в акваторию СМП',
                'Выход из морского порта РФ',
                'Вход в акваторию СМП из внутренних водных путей',
                'Вход в акваторию СМП',
                'Выход из акватории СМП',
                'Заход в Морской порт РФ',
                'Плавание в акватории СМП',
                'UNDEFINED'
            ])
        }),
        'lang': openapi.Schema(type=openapi.TYPE_STRING, enum=['RU', 'EN', 'UNDEFINED']),
        'quality': openapi.Schema(type=openapi.TYPE_NUMBER, default=0.9),
        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'parsing_time': openapi.Schema(type=openapi.TYPE_NUMBER, default=0.56),
        'createDate': openapi.Schema(type=openapi.TYPE_STRING, default='DD.MM.YYYY hh:mm:ss'),
        'attrs': openapi.Schema(type=openapi.TYPE_OBJECT),
    }
))

@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message-id': openapi.Schema(type=openapi.TYPE_STRING, description='Id сообщения'),
            'message_content': openapi.Schema(type=openapi.TYPE_STRING, description='Содержимое ДИСПа = содержимое email-письма как есть/точь-в-точь'),
            'message-subject': openapi.Schema(type=openapi.TYPE_STRING, description='Тема email-письма с содержимым сообщения'),
            'message-from': openapi.Schema(type=openapi.TYPE_STRING, description='Отправитель email-письма с содержимым сообщения', default='email-to-from@test.com'),
            'message-to': openapi.Schema(type=openapi.TYPE_STRING, description='Получатели email-письма с содержимым сообщения', default='email-to-first@test.com,email-to-second@test.com'),
            'message-date-sending': openapi.Schema(type=openapi.TYPE_STRING, description='Дата отправки email-письма с содержимым сообщения в формате DD.MM.YYYY HH:mi:ss', default=current_date_str),
            'message-date-receiving': openapi.Schema(type=openapi.TYPE_STRING, description='Дата получения email-письма с содержимым сообщения в формате DD.MM.YYYY HH:mi:ss', default=current_date_str),
            'threshold': openapi.Schema(type=openapi.TYPE_NUMBER, description='Пороговое значение качества распознования из промежутка (0, 1.0]', default=0.87)
        },
        required=['message-content', 'message-date-sending']
), responses={200: user_response})

@api_view(['POST'])
def test(request):
    """
    Сервис для парсинга текста сообщения
    """
    data = request.data
    return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', auto_schema=None)
@api_view(['GET'])
def another_test(request):
    return Response('OK', status=status.HTTP_200_OK)


@api_view(['GET'])
# @renderer_classes([TemplateHTMLRenderer])
def static(request, **kwargs):
    """
    Сервис для получения static-файлов при функционировании приложения в prod-режиме
    """
    file_path = kwargs.get('file_path', None)
    file_path = f'{settings.STATIC_ROOT}/{file_path}' if file_path else ''
    print(f'{file_path = }')
    ext = file_path.split('.')[-1]
    content_type = {
        'js': 'text/javascript',
        'css': 'text/css',
        'html': 'text/html',
        'png': 'image/png'
    }
    content_type = content_type.get(ext, None)
    if not file_path or not content_type:
        return Response('Not found', status=status.HTTP_404_NOT_FOUND)
    with open(file_path, 'r') as file:
        data = file.read()
    return Response(data, status=status.HTTP_200_OK, content_type=content_type)

