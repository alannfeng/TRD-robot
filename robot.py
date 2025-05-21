# -*- coding: utf-8 -*-
import asyncio
import os
import requests
import random
from datetime import datetime
import pytz

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, C2CMessage, Message

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
        def_return_list = await  self.load_case_list("./def_return.txt")
        def_anw_ids = await  self.load_case_ids("./def_anw.txt")

        content = message.content
        if "/TRD" in content:
            anw, error = await self.get_aqi("TRD")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=f"\n{i}")
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_message(channel_id=message.channel_id,
                                                msg_id=message.id,
                                                content=error)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前没有'the rising dead_汉译'公共房间")
                _log.info(messageResult)
        elif "/KR" in content:
            anw, error = await self.get_aqi("KR")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=f"\n{i}")
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_message(channel_id=message.channel_id,
                                                msg_id=message.id,
                                                content=error)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前亚服没有'the rising dead T'公共房间")
                _log.info(messageResult)
        elif "/EU" in content:
            anw, error = await self.get_aqi("EU")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=f"\n{i}")
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_message(channel_id=message.channel_id,
                                                msg_id=message.id,
                                                content=error)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前欧服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        elif "/US" in content:
            anw, error = await self.get_aqi("US")
            if len(anw) > 0:
                for i in anw:
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=f"\n{i}")
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_message(channel_id=message.channel_id,
                                                msg_id=message.id,
                                                content=error)
            else:
                messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                msg_id=message.id,
                                                                content=f"当前美服没有'-the rising dead-'公共房间")
                _log.info(messageResult)

        elif "车开走了吗" in content:
            anw, error = await self.get_history_aqi("TRD")
            if error != "":
                anw = error
            messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                            msg_id=message.id,
                                                            content=anw)
            _log.info(messageResult)
        else:
            def_return_open = 0
            for que, ans in def_anw_ids.items():
                if que in content:
                    ans = ans.replace('\\n', '\n')
                    messageResult = await message._api.post_message(channel_id=message.channel_id,
                                                                    msg_id=message.id,
                                                                    content=ans)
                    _log.info(messageResult)
                    def_return_open = 1
                    break
            if def_return_open == 0:
                ans = def_return_list[random.randint(0, len(def_return_list) - 1)]
                ans = ans.replace('\\n', '\n')
                await message.reply(content=f"\n{ans}")

    async def on_group_at_message_create(self, message: GroupMessage):
        content = message.content
        def_return_list = await  self.load_case_list("./def_return.txt")
        def_anw_ids = await  self.load_case_ids("./def_anw.txt")
        if "/TRD" in content:
            anw, error = await self.get_aqi("TRD")
            if len(anw) > 0:
                seq = 1
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0, msg_id=message.id, msg_seq=seq,
                                                                          content=f"\n{i}")
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_group_message(group_openid=message.group_openid,
                                                      msg_type=0, msg_id=message.id,
                                                      content=error)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前没有'the rising dead_汉译'房间")
                _log.info(messageResult)
        elif "/KR" in content:
            anw, error = await self.get_aqi("KR")
            if len(anw) > 0:
                seq = 1
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0, msg_id=message.id, msg_seq=seq,
                                                                          content=f"\n{i}")
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_group_message(group_openid=message.group_openid,
                                                      msg_type=0, msg_id=message.id,
                                                      content=error)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前亚服没有'the rising dead T'公共房间")
                _log.info(messageResult)
        elif "/EU" in content:
            anw, error = await self.get_aqi("EU")
            if len(anw) > 0:
                seq = 1
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0, msg_id=message.id, msg_seq=seq,
                                                                          content=f"\n{i}")
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_group_message(group_openid=message.group_openid,
                                                      msg_type=0, msg_id=message.id,
                                                      content=error)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前欧服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        elif "/US" in content:
            anw, error = await self.get_aqi("US")
            if len(anw) > 0:
                seq = 1
                for i in anw:
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0, msg_id=message.id, msg_seq=seq,
                                                                          content=f"\n{i}")
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_group_message(group_openid=message.group_openid,
                                                      msg_type=0, msg_id=message.id,
                                                      content=error)
            else:
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                      msg_type=0,msg_id=message.id,
                                                                      content=f"当前美服没有'-the rising dead-'公共房间")
                _log.info(messageResult)
        elif "车开走了吗" in content:
            anw, error = await self.get_history_aqi("TRD")
            if error != "":
                anw = error
            messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                  msg_type=0, msg_id=message.id,
                                                                  content=anw)
            _log.info(messageResult)
        else:
            def_return_open = 0
            for que, ans in def_anw_ids.items():
                if que in content:
                    ans = ans.replace('\\n', '\n')
                    messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                          msg_type=0,msg_id=message.id,
                                                                          content=f"\n{ans}")
                    _log.info(messageResult)
                    def_return_open = 1
                    break
            if def_return_open == 0:
                ans = def_return_list[random.randint(0, len(def_return_list) - 1)]
                ans = ans.replace('\\n', '\n')
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                  msg_type=0,msg_id=message.id,
                                                                  content=f"\n{ans}")
                _log.info(messageResult)

    async def on_c2c_message_create(self, message: C2CMessage):
        content = message.content
        def_return_list = await  self.load_case_list("./def_return.txt")
        def_anw_ids = await  self.load_case_ids("./def_anw.txt")
        if "/TRD" in content:
            anw, error = await self.get_aqi("TRD")
            if len(anw) > 0:
                for i in anw:
                    seq = 1
                    str_seq = str(seq)
                    _log.info("发送/TRD房间私信")
                    messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                        msg_id=message.id, msg_seq=str_seq, content=i)
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                    msg_id=message.id,
                                                    content=error)
            else:
                messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                    msg_id=message.id,
                                                                    content=f"当前没有'the rising dead_汉译'房间")
                _log.info(messageResult)

        elif "/KR" in content:
            anw, error = await self.get_aqi("KR")
            if len(anw) > 0:
                seq = 1
                for i in anw:
                    str_seq = str(seq)
                    _log.info("发送/KR房间私信")
                    messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                        msg_id=message.id, msg_seq=str_seq, content=i)
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                    msg_id=message.id,
                                                    content=error)
            else:
                messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                    msg_id=message.id,
                                                                    content=f"当前亚服没有'the rising dead T'公共房间")
                _log.info(messageResult)

        elif "/EU" in content:
            anw, error = await self.get_aqi("EU")
            if len(anw) > 0:
                seq = 1
                for i in anw:
                    str_seq = str(seq)
                    _log.info("发送/EU房间私信")
                    messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                        msg_id=message.id, msg_seq=str_seq, content=i)
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                    msg_id=message.id,
                                                    content=error)
            else:
                messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                    msg_id=message.id,
                                                                    content=f"当前欧服没有'-the rising dead-'公共房间")
                _log.info(messageResult)

        elif "/US" in content:
            anw, error = await self.get_aqi("US")
            if len(anw) > 0:
                seq = 1
                for i in anw:
                    str_seq = str(seq)
                    _log.info("发送/US房间私信")
                    messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                        msg_id=message.id, msg_seq=str_seq, content=i)
                    seq += 1
                    _log.info(messageResult)
            elif error != "":
                await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                    msg_id=message.id,
                                                    content=error)
            else:
                messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                    msg_id=message.id,
                                                                    content=f"当前美服没有'-the rising dead-'公共房间")
                _log.info(messageResult)

        elif "车开走了吗" in content:
            anw, error = await self.get_history_aqi("TRD")
            if error != "":
                anw = error
            _log.info("发送正在进行的车的私信")
            messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                msg_id=message.id, content=anw)
            _log.info(messageResult)

        else:
            def_return_open = 0
            for que, ans in def_anw_ids.items():
                if que in content:
                    ans = ans.replace('\\n', '\n')
                    messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                        msg_id=message.id, content=ans)
                    _log.info(messageResult)
                    def_return_open = 1
                    break
            if def_return_open == 0:
                ans = def_return_list[random.randint(0, len(def_return_list) - 1)]
                ans = ans.replace('\\n', '\n')
                messageResult = await message._api.post_c2c_message(openid=message.author.user_openid, msg_type=0,
                                                                    msg_id=message.id,
                                                                    content=ans)
                _log.info(messageResult)


    @staticmethod
    async def get_aqi(region):
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
        error = ""
        if response.status_code != 200:
            error = "数据网站异常，暂不可用"
        elif len(response.json()) == 0:
            error = "数据网站异常，暂不可用"
        else:
            for i in response.json():
                if i["mapBnetId"] == mapBnetId:
                    txt = f"房名：{i['lobbyTitle']}\n房主：{i['hostName']}\n人数：({i['slotsHumansTaken']}/{i['slotsHumansTotal']})\n"
                    num = 0
                    for j in i["slots"]:
                        num += 1
                        if j["kind"] == "human":
                            txt += f"玩家{num}：{j['name']}\n"
                    req.append(txt)
        return req, error

    @staticmethod
    async def get_history_aqi(region):
        if region == "KR":
            regionId = "3"
            mapBnetId = "135435"
        elif region == "EU":
            regionId = "2"
            mapBnetId = "207565"
        elif region == "US":
            regionId = "1"
            mapBnetId = "296886"
        elif region == "TRD":
            regionId = "3"
            mapBnetId = "158546"
        else:
            regionId = "3"
            mapBnetId = "158546"
        url = "https://api.sc2arcade.com/lobbies/history"
        payload = {
            "regionId": regionId,
            "mapId": mapBnetId,
            "includeMatchResult": "true",
            "limit": "20"
        }
        headers = {
            'accept': '*/*'
        }
        response = requests.request("GET", url, headers=headers, params=payload)
        req = []
        error = ""
        if response.status_code != 200:
            error = "数据网站异常，暂不可用"
        elif len(response.json()) == 0:
            error = "数据网站异常，暂不可用"
        else:
            for i in response.json()["results"]:
                if i["status"] == "started":
                    date_string = i["closedAt"]
                    timestamp = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() + 28800
                    current_timestamp = datetime.now().timestamp()
                    if int(current_timestamp) - int(timestamp) > 6000:
                        break
                    if not i["match"]:
                        beijing_tz = pytz.timezone('Asia/Shanghai')
                        beijing_time = datetime.fromtimestamp(timestamp).astimezone(beijing_tz)
                        formatted_time = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
                        txt = f"{formatted_time}开走一车，里面有{i['slotsHumansTotal']}人"
                        req.append(txt)

        answer = ""
        if len(req) > 0:
            for i in req:
                answer += "\n" + i
        else:
            answer = "没有开走的车"
        return answer, error

    @staticmethod
    async def load_case_ids(filename) -> dict:
        case_ids = {}
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',,,,')
                    if len(parts) == 2:
                        case_ids[parts[0].strip()] = parts[1].strip()
        return case_ids

    @staticmethod
    async def load_case_list(filename):
        case_list = []
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip()
                    case_list.append(parts)
        return case_list

if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    intents = botpy.Intents.none()
    intents.public_guild_messages = True
    intents.public_messages = True

    # 通过kwargs，设置需要监听的事件通道
    # intents = botpy.Intents.default()
    # client = MyClient(intents=intents, is_sandbox=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
