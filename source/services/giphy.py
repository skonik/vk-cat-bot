import io
import re
import json

import aiohttp


class GiphyMethodsMeta(type):
    GIPHY_API_METHODS_URL = 'https://api.giphy.com/v1/'
    allowed_methods = re.compile(r'gifs')

    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if cls.allowed_methods.match(attr_name):
                dct[attr_name] = f'{cls.GIPHY_API_METHODS_URL}{attr_value}'
        return super().__new__(cls, name, bases, dct)


class GiphyMethods(metaclass=GiphyMethodsMeta):
    gifs_random = 'gifs/random'
    gifs_translate = 'gifs/translate'


class Giphy:

    def __init__(self, token):
        self.__token = token
        self.basic_params = {
            'api_key': token
        }

    async def get_random_gif(self, tag=None):
        query_params = self.basic_params.copy()
        if tag:
            query_params.update({'tag': tag.strip()})

        async with aiohttp.ClientSession() as session:
            async with session.get(GiphyMethods.gifs_random, params=query_params) as response:
                body = await response.text()
                response_json = json.loads(body)
                gif_url = response_json['data']['images']['downsized_medium']['url']
                async with session.get(gif_url) as resp:
                    gif_image = io.BytesIO(await resp.read())

        return gif_image

    async def get_translate(self, string):
        query_params = self.basic_params.copy()
        if not string:
            string = 'empty'
        query_params.update({'s': string.strip()})

        async with aiohttp.ClientSession() as session:
            async with session.get(GiphyMethods.gifs_translate, params=query_params) as response:
                body = await response.text()
                response_json = json.loads(body)
                gif_url = response_json['data']['images']['downsized_medium']['url']
                async with session.get(gif_url) as resp:
                    gif_image = io.BytesIO(await resp.read())

        return gif_image
