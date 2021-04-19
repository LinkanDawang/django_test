import hmac
import time
import json
import urllib
import hashlib
import requests
import datetime
from user_agents import parse as ua_parse
from rest_framework_tracking.base_mixins import BaseLoggingMixin

from apps.api_log.models import RequestLog


def baidu_ip2location(ip):
    # 1.AK/SK、host、method、URL绝对路径、querystring
    app_key = "a1e4385b50f7403c84a18a7bbbed8798"
    app_secret = "c5249ef022ea48f682baacaf19a66edb"
    host = "ipapi.api.bdymkt.com"
    method = "POST"
    query = ""
    uri = "/ip2location/retrieve"

    # 2.x-bce-date
    x_bce_date = time.gmtime()
    x_bce_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', x_bce_date)
    # 3.header和signedHeaders
    header = {
        "Host": host,
        "content-type": "application/json;charset=utf-8",
        "x-bce-date": x_bce_date
    }
    signed_headers = "content-type;host;x-bce-date"
    # 4.认证字符串前缀
    auth_string_prefix = "bce-auth-v1" + "/" + app_key + "/" + x_bce_date + "/" + "1800"
    # 5.生成CanonicalRequest
    # 5.1生成CanonicalURI
    canonical_uri = urllib.parse.quote(uri)  # windows下为urllib.parse.quote，Linux下为urllib.quote
    # 5.2生成CanonicalQueryString
    canonical_query_string = query  # 如果您调用的接口的query比较复杂的话，需要做额外处理
    # 5.3生成CanonicalHeaders
    result = []
    for key, value in header.items():
        temp_str = str(urllib.parse.quote(key.lower(), safe="")) + ":" + str(urllib.parse.quote(value, safe=""))
        result.append(temp_str)
    result.sort()
    canonical_headers = "\n".join(result)
    # 5.4拼接得到CanonicalRequest
    canonical_request = method + "\n" + canonical_uri + "\n" + canonical_query_string + "\n" + canonical_headers
    # 6.生成signingKey
    signingkey = hmac.new(app_secret.encode('utf-8'), auth_string_prefix.encode('utf-8'), hashlib.sha256)
    # 7.生成Signature
    signature = hmac.new((signingkey.hexdigest()).encode('utf-8'), canonical_request.encode('utf-8'), hashlib.sha256)
    # 8.生成Authorization并放到header里
    header['X-Bce-Signature'] = auth_string_prefix + "/" + signed_headers + "/" + signature.hexdigest()
    # 9.发送API请求并接受响应

    body = {
        "ip": ip
    }

    url = "http://" + host + uri

    r = requests.post(url, headers=header, data=json.dumps(body))
    # {'country': '中国', 'province': '浙江', 'city': '杭州', 'county': '余杭', 'isp': '中国移动'}
    if r.status_code == 200:
        result = r.json()
        telco = result.pop("isp")
        address = "-".join([v for _, v in result.items()])
    else:
        address = None
        telco = None
    return address, telco


class LogRequestMixin(BaseLoggingMixin):
    need_log = False
    logging_actions = []

    def should_log(self, request, response):
        """
        Method that should return a value that evaluated to True if the request should be logged.
        By default, check if the request method is in logging_methods.
        """
        if self.need_log or self.action in self.logging_actions:
            return True
        return False

    def finalize_response(self, request, response, *args, **kwargs):
        ua = request.headers["User-Agent"]
        user_agent = ua_parse(ua)
        if user_agent.is_mobile:
            device_model = user_agent.device.family
            # print(device_model)  # Samsung SM-G900P
            self.log.update({"device_model": device_model})
            # print(user_agent.device.brand)  # Samsung
            # print(user_agent.device.model)  # SM-G900P
        response = super(LogRequestMixin, self).finalize_response(request, response, *args, **kwargs)
        # if "text/html" in response._headers["content-type"][1]:
        #     ...
        return response

    def _handle_ip(self):
        ip = self.log["remote_addr"]
        if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('172.16.'):
            ...
        else:
            ip_address, telco = baidu_ip2location(ip)
            self.log.update({"ip_address": ip_address, "telco": telco})

    def handle_log(self):
        """
        Hook to define what happens with the log.

        Defaults on saving the data on the db.
        """
        self._handle_ip()
        self.log["log_type"] = RequestLog.IN
        RequestLog(**self.log).save()

