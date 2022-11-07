# -*- coding: utf-8 -*-
# filename: handle.py
import web
import hashlib
import receive
import replay
import os
from func import get_replay_content

botIp = "127.0.0.1"  # 本机IP
botPort = "5002"
wxtoken = os.environ.get("WXTOKEN")


class Handle(object):
    # 改get请求用于验证Token
    def GET(self):
        try:
            data = web.input()
            print(data)
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = wxtoken

            li = [token, timestamp, nonce]
            li.sort()
            tmp_str = "".join(li).encode("utf-8")
            # 进行sha1加密
            hashcode = hashlib.sha1(tmp_str).hexdigest()

            # sha1 = hashlib.sha1()
            # map(sha1.update, li)
            # hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData.decode("utf-8"))
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            # 该模块是处理文本数据信息
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == "text":
                # 获取到并解析出来用户发送过来的数据信息
                recContent = recMsg.Content.decode("utf-8")
                print("user message:", recContent, type(recContent))
                replayContent = "QQ群：342950180"
                print("bot recContent: ", replayContent)
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                replayContent = get_replay_content(recContent, toUser)
                replyMsg = replay.TextMsg(toUser, fromUser, replayContent)
                return replyMsg.send()
            else:
                print("暂且不处理")
                return "success"
        except Exception as Argment:
            return Argment
