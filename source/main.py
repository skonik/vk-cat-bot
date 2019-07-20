import os
from commands import dispatch_msg

from aiohttp import web
from aiojobs.aiohttp import setup, spawn

from settings import VK_CONFIRMATION_CODE


async def webhook(request):
    data = await request.json()
    body = 'OK'
    msg_type = data.get('type')
    if msg_type == 'message_new':

        vk_object = data.get('object')
        peer_id = vk_object.get('peer_id')
        message = vk_object['text']
        await spawn(request, dispatch_msg(message, peer_id=peer_id))

    elif msg_type == 'confirmation':
        body = VK_CONFIRMATION_CODE

    return web.Response(body=body)


app = web.Application()
app.add_routes([web.post('/', webhook)])
setup(app)

if __name__ == '__main__':
    port = os.environ.get('WEBHOOK_PORT', 8000)
    web.run_app(app, port=port)
