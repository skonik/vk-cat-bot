[![Build Status](https://travis-ci.com/skonik/vk-cat-bot.svg?branch=master)](https://travis-ci.com/skonik/vk-cat-bot)

# vk-cat-bot

Aiohttp VK-bot for getting portion of gifs with cats. It uses vkontakte social network api and giphy api for getting gifs.

<p align="center"><img src="static/showcase.gif" width="220" height="480" /></p>

# How to use

Create a group and enable api integration in group settings. Create api_key and put it into `template.env`, create giphy api_key and put it in the same file. Confirm your server ip by adding confirmation code and running the bot. 

# Run in docker

`docker build -t cat-bot . && docker run cat-bot`
