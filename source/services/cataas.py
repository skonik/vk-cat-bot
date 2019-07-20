import io

import aiohttp


class CatAAS:
    text_url = 'https://cataas.com/cat/says/'

    @classmethod
    async def cat_says(cls, text='', size='50', color='white'):
        query_params = {
            'size': size,
            'color': color
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(cls.text_url + text, params=query_params) as response:
                gif_image = io.BytesIO(await response.read())

        return gif_image
