import re

import aiohttp

from settings import VK_ACCESS_TOKEN, GIPHY_ACCESS_TOKEN
from services.giphy import Giphy
from services.cataas import CatAAS
from services.vk_api import VkApi

vk_api = VkApi(api_token=VK_ACCESS_TOKEN, version='5.101')
giphy_api = Giphy(token=GIPHY_ACCESS_TOKEN)


async def send_cat_gif(peer_id):
    await send_gif_with_tag(peer_id, tag='cat')


async def send_gif_with_tag(peer_id, tag):

    random_gif = await giphy_api.get_random_gif(tag=tag)
    await send_gif(peer_id, random_gif)


async def send_gif_translate(peer_id, string):
    sauce_gif = await giphy_api.get_translate(string)
    await send_gif(peer_id, sauce_gif)


async def send_cat_says(peer_id, string):
    doc = await CatAAS.cat_says(text=string)
    await send_gif(peer_id, doc, filename='test.png')


async def send_gif(peer_id, doc, filename='test.gif'):
    async with aiohttp.ClientSession() as session:
        upload_doc_server_response = await vk_api.get_upload_doc_server(session, peer_id)
        upload_doc_url = upload_doc_server_response['response']['upload_url']

        upload_doc_response = await vk_api.upload_doc(session, upload_url=upload_doc_url, doc=doc,  filename=filename)
        file = upload_doc_response['file']
        save_doc_response = await vk_api.save_doc(session, file)
        media_id = save_doc_response['response']['doc']['id']
        owner_id = save_doc_response['response']['doc']['owner_id']
        doc_string = f'doc{owner_id}_{media_id}'
        await vk_api.send_message(session, peer_id, attachment=doc_string)


# TODO: refactor message dispatcher
def dispatch_msg(msg, *args, **kwargs):
    cat_command = re.search(r'(?P<preifx>котики)', msg, re.U + re.I)
    gif_command = re.search(r'(?P<prefix>гифку)\s*(?P<tag>.*)', msg, re.U + re.I)
    translate_command = re.search(r'(?P<prefix>изфразы)\s(?P<string>[a-zа-я\d ]+)', msg, re.U + re.I)
    cat_says_command = re.search(r'(?P<prefix>фраза)\s*(?P<string>[\w ]+)', msg, re.U + re.I)
    if cat_command:
        return send_cat_gif(kwargs['peer_id'])
    elif gif_command:
        tag = gif_command.group('tag')
        return send_gif_with_tag(kwargs['peer_id'], tag)
    elif translate_command:
        string = translate_command.group('string')
        return send_gif_translate(kwargs['peer_id'], string)
    elif cat_says_command:
        string = cat_says_command.group('string')
        return send_cat_says(kwargs['peer_id'], string)
    return None
