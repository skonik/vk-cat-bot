import re
import json
import random

import aiohttp


class VkApiMeta(type):
    VK_API_METHODS_URL = 'https://api.vk.com/method/'
    allowed_methods = re.compile(r'docs|messages')

    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if cls.allowed_methods.match(attr_name):
                dct[attr_name] = f'{cls.VK_API_METHODS_URL}{attr_value}'
        return super().__new__(cls, name, bases, dct)


class VkApiMethods(metaclass=VkApiMeta):
    docs_get_message_upload_server = 'docs.getMessagesUploadServer'
    docs_save = 'docs.save'
    messages_send = 'messages.send'


class VkApi:

    def __init__(self, api_token, version='5.101'):
        self.version = version
        self.__api_token = api_token
        self.basic_params = {
            'access_token': api_token,
            'v': version
        }

    async def get_upload_doc_server(self, session, peer_id):
        query_params = self.basic_params.copy()
        query_params.update(
            type='doc',
            peer_id=peer_id,
        )

        async with session.get(VkApiMethods.docs_get_message_upload_server, params=query_params) as response:
            body = await response.read()
            json_response = json.loads(body.decode('utf8'))
            return json_response

    async def upload_doc(self, session, upload_url, doc, filename='unknown.gif'):
        form = aiohttp.FormData()
        form.add_field('file', doc, filename=filename)
        async with session.post(
                upload_url,
                data=form
        ) as response:
            body = await response.read()
            response_json = json.loads(body)
            return response_json

    async def save_doc(self, session, file):
        query_params = self.basic_params.copy()
        query_params.update(
            {'file': file}
        )
        async with session.get(
                VkApiMethods.docs_save,
                params=query_params
        ) as response:
            body = await response.read()
            response_json = json.loads(body)
            return response_json

    async def send_message(self, session, peer_id, attachment=None):
        query_params = self.basic_params.copy()
        query_params.update({
            'peer_id': peer_id,
        })

        if attachment:
            query_params.update(
                attachment=attachment,
                random_id=random.randint(1000, 62000)
            )

        async with session.get(
                VkApiMethods.messages_send,
                params=query_params
        ) as response:
            body = await response.read()
            response_json = json.loads(body)

            return response_json
