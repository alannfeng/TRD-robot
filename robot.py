# -*- coding: utf-8 -*-
import asyncio
import os
import requests
import random

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import  GroupMessage, Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()
def_return = ["咕咕", "屁都没有","在蟑螂啃到队友前，搀扶他可以防止他逃走并且收到额外50%伤害","无视体积的跟随(xz)‘很’好用"]


class MyClient(botpy.Client):

    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        _log.info(message.author.username)
        content = message.content
        if "/TRD" in content:
            anw = await self.get_aqi("TRD")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前没有'the rising dead_汉译'公共房间")
                _log.info(messageResult)
        elif "/KR" in content:
            anw = await self.get_aqi("KR")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前亚服没有'the rising dead T'公共房间")
                _log.info(messageResult)
        elif "/EU" in content:
            anw = await self.get_aqi("EU")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前欧服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        elif "/US" in content:
            anw = await self.get_aqi("US")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前美服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        else:
            await message.reply(content=f"{def_return[ random.randint(0, len(def_return) - 1)]}")

    async def on_group_at_message_create(self, message: GroupMessage):
        content = message.content
        if "/TRD" in content:
            anw = await self.get_aqi("TRD")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0,msg_id=message.id,
                                                                          content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前没有'the rising dead_汉译'房间")
                _log.info(messageResult)
        elif "/KR" in content:
            anw = await self.get_aqi("KR")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0,msg_id=message.id,
                                                                          content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前亚服没有'the rising dead T'公共房间")
                _log.info(messageResult)
        elif "/EU" in content:
            anw = await self.get_aqi("EU")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0,msg_id=message.id,
                                                                          content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前欧服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        elif "/US" in content:
            anw = await self.get_aqi("US")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0,msg_id=message.id,
                                                                          content=i)
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前美服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        else:
            messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"{def_return[ random.randint(0, len(def_return) - 1)]}")
            _log.info(messageResult)

    @staticmethod
    async def get_aqi(region):
        """
        获取星际争霸二公开房间（aqi）数据

        :return: 返回星际争霸二目标公开房间的json列表
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
        if region == "KR":
            regionId = "3"
            mapBnetId = 135435
        elif region == "EU":
            regionId = "2"
            mapBnetId = 207565
        elif region == "US":
            regionId = "1"
            mapBnetId = 296886
        elif region == "TRD":
            regionId = "3"
            mapBnetId = 158546
        url = "https://api.sc2arcade.com/lobbies/active"
        payload = {
            "regionId": regionId,
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
        # # ark格式消息返回
        # req = []
        # for i in response.json():
        #     if i["mapBnetId"] == mapBnetId:
        #         payload = {
        #             "template_id": 23,
        #             "kv": [
        #                 {"key": "#DESC#", "value": f"房间名：{i['lobbyTitle']}"},
        #                 {"key": "#PROMPT#", "value": f"房主：{i['hostName']}\n人数：({i['slotsHumansTaken']}/{i['slotsHumansTotal']})\n"},
        #                 {"key": "#LIST#", "obj": [{"obj_kv": [{"key": "desc", "value": f"玩家：{j['name']}"}]} for j in i["slots"]]}
        #                 ]
        #                 }
        #         req.append(payload)
        req = []
        for i in response.json():
            if i["mapBnetId"] == mapBnetId:
                _log.info(i)
                txt = f"房名：{i['lobbyTitle']}\n房主：{i['hostName']}\n人数：({i['slotsHumansTaken']}/{i['slotsHumansTotal']})\n"
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
    client.run(appid=test_config["appid"], secret=test_config["secret"])
