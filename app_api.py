#!/usr/bin/env python
# -*- coding:utf-8 -*-
# fileName: app_api.py
from run_method import RunMethod
from read_info import ReadYaml
from get_log import get_log
from deal_token import write_token
import json
 
 
class AllApi(object):
    def __init__(self):
        self.run = RunMethod()
        self.read = ReadYaml()
        self.logger = get_log()
 
    # 登录，获取token
    def login(self, api_name):
        try:
            # 获取接口请求参数
            method = self.read.get_method(api_name)
            url = self.read.get_url(api_name)
            data = self.read.get_data(api_name)
            headers = self.read.get_headers(api_name)
            response = self.run.run_main(method, url, headers, data)
 
            # 把token值写到配置文件access_token.yml中，供其他接口调用
            write_token(response)
 
            print(json.dumps(response, indent=2, ensure_ascii=False, sort_keys=False))
            return response
        except Exception as e:
            self.logger.info("接口访问出错啦~ %s" % e)
 
    # 其他接口请求封装
    def send_request(self, api_name):
        try:
            # 获取接口请求参数
            method = self.read.get_method(api_name)
            url = self.read.get_url(api_name)
            headers = self.read.get_headers(api_name)
            # 区分Get和Post方法
            if method == "Get":
                response = self.run.run_main(method, url, headers)
            elif method == "Post":
                data = self.read.get_data(api_name)
                response = self.run.run_main(method, url, headers, data)
                # print(json.dumps(response, indent=2, ensure_ascii=False, sort_keys=False))
 
            print(json.dumps(response, indent=2, ensure_ascii=False, sort_keys=False))
            print(response["success"])
            return response
        except Exception as e:
            self.logger.info("接口访问出错啦~ %s" % e)
 
    # 获取预期结果，方便断言时直接使用
    def get_expect(self, api_name):
        try:
            # 获取配置文件中的预期结果
            expect = self.read.get_expected(api_name)
            # print(expect)
            return expect
        except Exception as e:
            self.logger.info("获取预期结果出错啦~ %s" % e)