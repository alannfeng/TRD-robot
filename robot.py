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
#def_return = read(os.path.join(os.path.dirname(__file__), "def_return.yaml"))
_log = logging.get_logger()
def_return = ["咕咕", 
              "屁都没有",
              "“长官，搀扶除了让一个废物变成两个废物还有什么用呢？”\n“你可以防止他逃走并且收到额外50%伤害”",
              "“跟随(xz)可以短期无视体积，超好用的”\n“所以那天xz把我挤进雷区的也是你咯？”",
              "单生10波11波14波跳下一波时间固定为3分30秒，如果熊提前死可能会提前",
              "单噩10波11波14波跳下一波时间固定为3分03秒，如果熊提前死可能会提前",
              "重装可以e、v连续切换快速耗蓝帮助工头升温",
              "找不到模块？瞧瞧无人机下面",
              "“真的，那天我真的遇到野生的好几个连锁叠一起”\n“你想没想过，也许~嗯~只是有人把捡起的雷下了上去~”",
              "“长官，身为队长的，匹到了十一个嫌简单而单走老登怎么办”\n“试试在2波末输入-vet，哦对-double也可以二波后开”",
              "上将  汪小白  已阵亡",
              "“左边e排撤离点都沙袋和车记得拍掉”QAQ将军一脸严肃的提醒新来的士官“别问为什么”",
              "“你觉得玩重装最大的幻觉是什么”\n“总觉得殿后的自己走的了”",
              ]


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
                                                                    content=f"\n{i})
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
                                                                    content=f"\n{i})
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
                                                                    content=f"\n{i})
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
                                                                    content=f"\n{i})
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前美服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        else:
            await message.reply(content=f"\n{def_return[ random.randint(0, len(def_return) - 1)]}")

    async def on_group_at_message_create(self, message: GroupMessage):
        content = message.content
        if "/TRD" in content:
            anw = await self.get_aqi("TRD")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0,msg_id=message.id,
                                                                          content=f"\n{i})
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
                                                                          content=f"\n{i})
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
                                                                          content=f"\n{i})
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
                                                                          content=f"\n{i}")
                    _log.info(messageResult)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前美服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        else:
            messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"\n{def_return[ random.randint(0, len(def_return) - 1)]}")
            _log.info(messageResult)

    @staticmethod
    async def get_aqi(region):
        """
        获取空气质量（aqi）数据

        :return: 返回空气质量数据的json���象
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