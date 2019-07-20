import os
import re

import aiohttp
from aiohttp import web
from aiojobs.aiohttp import setup, spawn

from settings import VK_ACCESS_TOKEN, GIPHY_ACCESS_TOKEN, VK_CONFIRMATION_CODE
from services.giphy import Giphy
from services.vk_api import VkApi

vk_api = VkApi(api_token=VK_ACCESS_TOKEN, version='5.101')
giphy_api = Giphy(token=GIPHY_ACCESS_TOKEN)


async def send_cat_gif(peer_id):

    random_cat_gif = await giphy_api.get_random_gif(tag='cat')

    async with aiohttp.ClientSession() as session:
        upload_doc_server_response = await vk_api.get_upload_doc_server(session, peer_id)
        upload_doc_url = upload_doc_server_response['response']['upload_url']

        upload_doc_response = await vk_api.upload_doc(session, upload_url=upload_doc_url, doc=random_cat_gif)
        file = upload_doc_response['file']
        save_doc_response = await vk_api.save_doc(session, file)
        media_id = save_doc_response['response']['doc']['id']
        owner_id = save_doc_response['response']['doc']['owner_id']
        doc_string = f'doc{owner_id}_{media_id}'
        await vk_api.send_message(session, peer_id, attachment=doc_string)


async def webhook(request):
    data = await request.json()
    body = 'OK'

    msg_type = data.get('type')
    if msg_type == 'message_new':

        vk_object = data.get('object')
        peer_id = vk_object.get('peer_id')
        message = vk_object['text']
        if re.search(r'котики', message, re.U + re.I):
            await spawn(request, send_cat_gif(peer_id))

    elif msg_type == 'confirmation':
        body = VK_CONFIRMATION_CODE

    return web.Response(body=body)


app = web.Application()
app.add_routes([web.post('/', webhook)])
setup(app)

if __name__ == '__main__':
    port = os.environ.get('WEBHOOK_PORT', 8000)
    web.run_app(app, port=port)
