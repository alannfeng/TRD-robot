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
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()



class MyClient(botpy.Client):

    # 职业基础加点 -> 对应的"加点更多"关键词映射
    SKILL_MORE_MAP = {
        "推荐突突加点": "突突加点更多",
        "推荐大夫加点": "大夫加点更多",
        "推荐重装加点": "重装加点更多",
        "推荐狙击加点": "狙击加点更多",
        "推荐爆破加点": "爆破加点更多",
        "推荐侦查加点": "侦查加点更多",
        "推荐火娃加点": "火娃加点更多",
        "推荐工头加点": "工头加点更多",
        "推荐通信加点": "通信加点更多",
    }

    # "加点更多"详细内容的关键词集合
    SKILL_MORE_DETAIL = {
        "突突加点更多", "大夫加点更多", "重装加点更多", "狙击加点更多",
        "爆破加点更多", "侦查加点更多", "火娃加点更多", "工头加点更多", "通信加点更多",
    }

    # 客户端不支持按钮时的提示文案
    BTN_UNSUPPORT_TIPS = "请升级 QQ 版本以使用按钮功能"

    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    # ==================== 加点按钮（回调）相关辅助方法 ====================
    def _build_skill_menu_message(self):
        """构建职业加点菜单：markdown + keyboard（回调按钮 type=1）"""
        markdown_content = {
            "content": "# 推荐加点查询\n请点击下方按钮选择职业查看加点推荐："
        }
        menu = [
            ("btn_tutu", "突击队员", "推荐突突加点"),
            ("btn_dafu", "医疗兵", "推荐大夫加点"),
            ("btn_zhongzhuang", "重装步兵", "推荐重装加点"),
            ("btn_juji", "精准射手", "推荐狙击加点"),
            ("btn_baopo", "爆破专家", "推荐爆破加点"),
            ("btn_zhencha", "侦查", "推荐侦查加点"),
            ("btn_huowa", "喷火兵", "推荐火娃加点"),
            ("btn_gongtou", "工程师", "推荐工头加点"),
            ("btn_tongxin", "通信观测员", "推荐通信加点"),
        ]
        rows = []
        for idx in range(0, len(menu), 3):
            buttons = []
            for btn_id, label, data in menu[idx:idx + 3]:
                buttons.append({
                    "id": btn_id,
                    "render_data": {"label": label, "visited_label": label, "style": 1},
                    "action": {
                        "type": 1,
                        "permission": {"type": 2},
                        "data": data,
                        "unsupport_tips": self.BTN_UNSUPPORT_TIPS,
                    },
                })
            rows.append({"buttons": buttons})
        keyboard_content = {"content": {"rows": rows}}
        return markdown_content, keyboard_content

    async def _build_skill_detail_message(self, skill_key):
        """构建某职业基础加点详情：markdown + keyboard（更多/返回 回调按钮）"""
        more_key = self.SKILL_MORE_MAP[skill_key]
        ans_dict = await self.load_case_ids("./def_anw.txt")
        ans = ans_dict.get(skill_key, "暂无该职业加点信息").replace('\\n', '\n')
        markdown_content = {"content": f"## {skill_key}\n{ans}"}
        keyboard_content = {
            "content": {
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "btn_more",
                                "render_data": {"label": "查看更多加点", "visited_label": "查看更多加点", "style": 1},
                                "action": {"type": 1, "permission": {"type": 2}, "data": more_key,
                                           "unsupport_tips": self.BTN_UNSUPPORT_TIPS},
                            },
                            {
                                "id": "btn_back",
                                "render_data": {"label": "返回职业列表", "visited_label": "返回职业列表", "style": 0},
                                "action": {"type": 1, "permission": {"type": 2}, "data": "推荐加点",
                                           "unsupport_tips": self.BTN_UNSUPPORT_TIPS},
                            },
                        ]
                    }
                ]
            }
        }
        return markdown_content, keyboard_content

    async def _build_skill_more_message(self, more_key):
        """构建某职业更多加点详情：markdown + keyboard（返回 回调按钮）"""
        ans_dict = await self.load_case_ids("./def_anw.txt")
        ans = ans_dict.get(more_key, "暂无更多加点信息").replace('\\n', '\n')
        markdown_content = {"content": f"## {more_key}\n{ans}"}
        keyboard_content = {
            "content": {
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "btn_back",
                                "render_data": {"label": "返回职业列表", "visited_label": "返回职业列表", "style": 1},
                                "action": {"type": 1, "permission": {"type": 2}, "data": "推荐加点",
                                           "unsupport_tips": self.BTN_UNSUPPORT_TIPS},
                            }
                        ]
                    }
                ]
            }
        }
        return markdown_content, keyboard_content

    async def on_interaction_create(self, interaction):
        """处理消息按钮回调事件（action.type=1）。

        收到回调后必须调用 on_interaction_result 进行回应，否则客户端会一直 loading 直到超时。
        """
        try:
            resolved = interaction.data.resolved if interaction.data else None
            button_data = resolved.button_data if resolved else None
        except AttributeError:
            button_data = None
        _log.info(f"收到按钮回调: data={button_data}, id={interaction.id}, "
                  f"event_id={interaction.event_id}, chat_type={interaction.chat_type}")

        # 根据回调数据构建对应的 markdown + keyboard 消息
        markdown_content = None
        keyboard_content = None
        if button_data == "推荐加点":
            markdown_content, keyboard_content = self._build_skill_menu_message()
        elif button_data in self.SKILL_MORE_MAP:
            markdown_content, keyboard_content = await self._build_skill_detail_message(button_data)
        elif button_data in self.SKILL_MORE_DETAIL:
            markdown_content, keyboard_content = await self._build_skill_more_message(button_data)

        # 必须先回应交互事件（ACK），消除客户端 loading 状态
        # 注意：该 PUT 接口仅用于"已收到"应答，本身不发送消息内容
        try:
            await interaction._api.on_interaction_result(interaction.id, 0)
        except Exception as e:
            _log.error(f"回应按钮回调事件失败: {e}")

        if markdown_content is None:
            _log.warning(f"未识别的按钮回调数据: {button_data}")
            return

        # 被动消息的 event_id 必须使用 ws 推送的顶层 id（interaction.event_id），
        # 而非业务事件 id（interaction.id，那个仅用于上面的 on_interaction_result ACK）。
        # 误用 interaction.id 会触发 40034025（请求参数 event_id 无效）。
        passive_event_id = interaction.event_id
        try:
            if interaction.chat_type == 1:  # 群聊
                await interaction._api.post_group_message(
                    group_openid=interaction.group_openid, msg_type=2,
                    event_id=passive_event_id,
                    markdown=markdown_content, keyboard=keyboard_content)
            elif interaction.chat_type == 2:  # 单聊
                await interaction._api.post_c2c_message(
                    openid=interaction.user_openid, msg_type=2,
                    event_id=passive_event_id,
                    markdown=markdown_content, keyboard=keyboard_content)
            elif interaction.chat_type == 0:  # 频道
                await interaction._api.post_message(
                    channel_id=interaction.channel_id, msg_type=2,
                    event_id=passive_event_id,
                    markdown=markdown_content, keyboard=keyboard_content)
        except Exception as e:
            # 被动消息失败（event_id 过期/无效等）时，降级为主动消息重试一次
            _log.error(f"按钮回调被动消息发送失败，尝试主动消息: {e}")
            try:
                if interaction.chat_type == 1:
                    await interaction._api.post_group_message(
                        group_openid=interaction.group_openid, msg_type=2,
                        markdown=markdown_content, keyboard=keyboard_content)
                elif interaction.chat_type == 2:
                    await interaction._api.post_c2c_message(
                        openid=interaction.user_openid, msg_type=2,
                        markdown=markdown_content, keyboard=keyboard_content)
                elif interaction.chat_type == 0:
                    await interaction._api.post_message(
                        channel_id=interaction.channel_id, msg_type=2,
                        markdown=markdown_content, keyboard=keyboard_content)
            except Exception as e2:
                _log.error(f"按钮回调主动消息发送也失败: {e2}")

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        _log.info(message.author.username)
        def_return_list = await  self.load_case_list("./def_return.txt")
        def_anw_ids = await  self.load_case_ids("./def_anw.txt")

        content = message.content.strip()
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
                matched = [item for item in def_return_list if content in item]
                pool = matched if matched else def_return_list
                ans = random.choice(pool)
                ans = ans.replace('\\n', '\n')
                await message.reply(content=f"\n{ans}")

    async def on_group_at_message_create(self, message: GroupMessage):
        content = message.content.strip()
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
                                                                      content=f"当前亚服没有'-the rising dead-'公共房间")
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
        elif "推荐加点" in content:
            # 发送职业加点菜单（回调按钮）
            markdown_content, keyboard_content = self._build_skill_menu_message()
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid, msg_type=2, msg_id=message.id,
                markdown=markdown_content, keyboard=keyboard_content)
            _log.info(messageResult)
        elif content in self.SKILL_MORE_MAP:
            # 文本兜底：发送某职业基础加点（含"更多/返回"回调按钮）
            markdown_content, keyboard_content = await self._build_skill_detail_message(content)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid, msg_type=2, msg_id=message.id,
                markdown=markdown_content, keyboard=keyboard_content)
            _log.info(messageResult)
        elif content in self.SKILL_MORE_DETAIL:
            # 文本兜底：发送某职业更多加点（含"返回"回调按钮）
            markdown_content, keyboard_content = await self._build_skill_more_message(content)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid, msg_type=2, msg_id=message.id,
                markdown=markdown_content, keyboard=keyboard_content)
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
                matched = [item for item in def_return_list if content in item] if content else []  # 如果content为空，则matched为空列表
                pool = matched if matched else def_return_list
                ans = random.choice(pool)
                ans = ans.replace('\\n', '\n')
                messageResult = await message._api.post_group_message(group_openid=message.group_openid,
                                                                  msg_type=0,msg_id=message.id,
                                                                  content=f"\n{ans}")
                _log.info(messageResult)

    async def on_c2c_message_create(self, message: C2CMessage):
        content = message.content.strip()
        def_return_list = await  self.load_case_list("./def_return.txt")
        def_anw_ids = await  self.load_case_ids("./def_anw.txt")
        if "/TRD" in content:
            anw, error = await self.get_aqi("TRD")
            if len(anw) > 0:
                seq = 1
                for i in anw:
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
                                                                    content=f"当前亚服没有'-the rising dead-'公共房间")
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

        elif "推荐加点" in content:
            markdown_content, keyboard_content = self._build_skill_menu_message()
            messageResult = await message._api.post_c2c_message(
                openid=message.author.user_openid, msg_type=2, msg_id=message.id,
                markdown=markdown_content, keyboard=keyboard_content)
            _log.info(messageResult)
        elif content in self.SKILL_MORE_MAP:
            markdown_content, keyboard_content = await self._build_skill_detail_message(content)
            messageResult = await message._api.post_c2c_message(
                openid=message.author.user_openid, msg_type=2, msg_id=message.id,
                markdown=markdown_content, keyboard=keyboard_content)
            _log.info(messageResult)
        elif content in self.SKILL_MORE_DETAIL:
            markdown_content, keyboard_content = await self._build_skill_more_message(content)
            messageResult = await message._api.post_c2c_message(
                openid=message.author.user_openid, msg_type=2, msg_id=message.id,
                markdown=markdown_content, keyboard=keyboard_content)
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
                matched = [item for item in def_return_list if content in item]
                pool = matched if matched else def_return_list
                ans = random.choice(pool)
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
            mapBnetId = 124551
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
        }
        headers = {
            'accept': '*/*'
        }
        response = requests.request("GET", url, headers=headers, params=payload)
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
    intents.interaction = True  # 开启互动事件监听，用于接收按钮回调（INTERACTION_CREATE）

    # 通过kwargs，设置需要监听的事件通道
    # intents = botpy.Intents.default()
    # client = MyClient(intents=intents, is_sandbox=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])