#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: sheng-jie
@contact: hi121073215@gmail.com
@date: 2023-01-19
@version: 0.0.1
@license:
@copyright:
"""
import json
import requests
import time

from elastalert.alerts import Alerter, BasicMatchString
from elastalert.util import elastalert_logger, EAException
from requests.exceptions import RequestException


class FeishuAlert(Alerter):

    required_options = frozenset(
        ['feishualert_botid'])

    def __init__(self, rule):
        super(FeishuAlert, self).__init__(rule)
        self.url = self.rule.get(
            "feishualert_url", "https://open.feishu.cn/open-apis/bot/v2/hook/")
        self.bot_id = self.rule.get("feishualert_botid", "")
        self.skip = self.rule.get("feishualert_skip", {})
        if self.bot_id == "" :
            raise EAException("Configure botid is invalid")

    def get_info(self):
        return {
            "type": "FeishuAlert"
        }

    def create_default_title(self, matches):
        subject = 'ElastAlert: %s' % (self.rule['name'])
        return subject

    def alert(self, matches):
        now = time.strftime("%H:%M:%S", time.localtime())
        if "start" in self.skip and "end" in self.skip:
            if self.skip["start"] <= now and self.skip["end"] >= now:
                print("Skip match in silence time...")
                return

        headers = {
            "Content-Type": "application/json;",
        }

        postBody = self.create_alert_body(matches)
        body = {
            "msg_type": "text",
            "content": {
                "text": postBody
            }
        }

        try:
            url = self.url + self.bot_id
            res = requests.post(data=json.dumps(
                body), url=url, headers=headers)
            res.raise_for_status()            
            elastalert_logger.info("send message to %s" % (postBody))

        except RequestException as e:
            raise EAException("Error request to feishu: {0}".format(str(e)))
