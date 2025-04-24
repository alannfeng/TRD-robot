# -*- coding: utf-8 -*-
import asyncio
import os
import requests

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import  GroupMessage, Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):

    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        _log.info(message.author.username)
        url = "https://api.sc2arcade.com/lobbies/active"
        payload = {
            "regionId": "3",
            "includeMapInfo": "false",
            "includeSlots": "true",
            "includeSlotsProfile": "true",
            "includeSlotsJoinInfo": "true",
            "includeJoinHistory": "false",
            "recentlyClosedThreshold": "200"
        }
        headers = {
            'accept': '*/*'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        req = []
        for i in response.json():
            if i["mapBnetId"] == 158546:
                _log.info(i)
                txt = f"房名：{i['lobbyTitle']}\n房主：{i['hostName']}\n人数：{i['slotsHumansTaken']}/{i['slotsHumansTotal']}\n"
                num = 0
                for j in i["slots"]:
                    num += 1
                    if j["kind"] == "human":
                        txt += f"玩家{num}：{j['name']}\n"
                req.append(txt)
        if len(req) > 0:
            anw = ""
            for i in req:
                anw += "\n"+i+"\n"
        else:
            anw = "没有'the rising dead_汉译'房间"
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了:\n{anw}")

    async def on_group_at_message_create(self, message: GroupMessage):
        url = "https://api.sc2arcade.com/lobbies/active"
        payload = {
            "regionId": "3",
            "includeMapInfo": "false",
            "includeSlots": "true",
            "includeSlotsProfile": "true",
            "includeSlotsJoinInfo": "true",
            "includeJoinHistory": "false",
            "recentlyClosedThreshold": "20"
        }
        headers = {
            'accept': '*/*'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        req = []
        for i in response.json():
            if i["mapBnetId"] == 158546:
                txt = f"房名：{i['lobbyTitle']}\n房主：{i['hostName']}\n人数：{i['slotsHumansTaken']}/{i['slotsHumansTotal']}\n"
                for j in i["slots"]:
                    if j["kind"] == "human":
                        txt += f"玩家：{j['name']}\n"
                req.append(txt)
        if len(req) > 0:
            anw = ""
            for i in req:
                anw += "\n" + i + "\n"
        else:
            anw = "没有'the rising dead_汉译'房间"

        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0,
              msg_id=message.id,
              content=f"收到了消息：{anw}")
        _log.info(messageResult)

    @staticmethod
    async def get_aqi():
        """
        获取空气质量（aqi）数据

        :return: 返回空气质量数据的json对象
        返回示例
        {
    "regionId": 3,
    "bnetBucketId": 1742601645,
    "bnetRecordId": 6638440,
    "createdAt": "2025-04-24T09:58:08.564Z",
    "closedAt": null,
    "snapshotUpdatedAt": "2025-04-24T11:43:52.304Z",
    "slotsUpdatedAt": "2025-04-24T11:30:04.702Z",
    "status": "open",
    "mapBnetId": 157899,
    "extModBnetId": null,
    "multiModBnetId": null,
    "mapVariantIndex": 0,
    "mapVariantMode": "test 3.01",
    "lobbyTitle": "",
    "hostName": "特别行动队情报员",
    "slotsHumansTotal": 12,
    "slotsHumansTaken": 1,
    "slots": [
      {
        "slotNumber": 1,
        "team": 1,
        "kind": "human",
        "name": "特别行动队情报员",
        "profile": {
          "regionId": 3,
          "realmId": 1,
          "profileId": 8013265,
          "name": "特别行动队情报员",
          "discriminator": 606,
          "avatar": "15-0"
        },
        "joinInfo": {
          "joinedAt": "2025-04-24T09:58:08.818Z",
          "leftAt": null
        }
      }
    ]
  }
        """
        url = "https://api.sc2arcade.com/lobbies/active"
        payload = {
            "regionId": "3",
            "includeMapInfo": "false",
            "includeSlots": "true",
            "includeSlotsProfile": "true",
            "includeSlotsJoinInfo": "true",
            "includeJoinHistory": "false",
            "recentlyClosedThreshold": "200"
        }
        headers = {
            'accept': '*/*'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        req = []
        for i in response.json():
            if i["mapBnetId"] == 158546:
                payload = {
                    "template_id": 37,
                    "kv": [
                        {"key": "#METATITLE#", "value": "通知提醒"},
                        {"key": "#PROMPT#", "value": "标题"},
                        {"key": "#TITLE#", "value": "标题"},
                        {"key": "#METACOVER#", "value": "https://vfiles.gtimg.cn/vupload/20211029/bf0ed01635493790634.jpg"},
                    ],
                }
                _log.info(i)
                txt = f"房名：{i['lobbyTitle']}\n房主：{i['hostName']}\n人数：{i['slotsHumansTaken']}/{i['slotsHumansTotal']}\n"
                num = 0
                for j in i["slots"]:
                    num += 1
                    if j["kind"] == "human":
                        txt += f"玩家{num}：{j['name']}\n"
                req.append(txt)
        return req

if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    intents = botpy.Intents.none()
    intents.public_guild_messages=True
    intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    # intents = botpy.Intents.default()
    client = MyClient(intents=intents)
    client.run(appid="102089878", secret="C2sjaRI90skcUMF81ungaUOIC61wrmhc")
