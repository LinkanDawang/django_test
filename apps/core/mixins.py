import json
import requests
import datetime
from user_agents import parse as ua_parse
from rest_framework_tracking.base_mixins import BaseLoggingMixin

from apps.api_log.models import RequestLog


class LogRequestMixin(BaseLoggingMixin):
    need_log = False
    logging_actions = []

    def baidu_ip(self, ip):
        datetime.datetime.utcnow()
        url = "https://ipapi.api.bdymkt.com/ip2location/retrieve"
        headers = {
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81"
        }
        x = requests.post(url, data={"ip": ip})
        print(x.json())

    def get_address_from_ip(self, ip):
        """
        根据IP解析出地址
        :param ip: ip
        :return: 解析出来的地址
         {
         'status': '1', 'info': 'OK', 'infocode': '10000',
          'province': '上海市', 'city': '上海市', 'adcode': '310000',
          'rectangle': '120.8397067,30.77980118;122.1137989,31.66889673'}
          ip,ip_country,ip_province,ip_city,ip_county,
          lat,lon,gps_country,gps_province,gps_city,
          gps_county,gps_address
        """

        format_result = {'country': None, 'province': None, 'city': None}
        base_url = 'https://restapi.amap.com/v3/ip?'
        params = {
            'key': "19041ae76e39ddd949a2f895a78e399d",
            'ip': ip,
            'sign': None,
            'output': 'json'
        }
        format_result['country'] = '中国'
        if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('172.16.'):
            format_result['province'] = '上海市'
            format_result['city'] = '上海市'
        else:
            response = requests.get(base_url, params=params)
            add_info = json.loads(response.text)
            format_result['province'] = add_info.get('province')
            format_result['city'] = add_info.get('city')
            if add_info.get('province') == []:
                format_result['country'] = '外国'
        return format_result['province'] + "-" + format_result['city'] if format_result['province'] else format_result['city']

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
        remote_addr = self._get_ip_address(request)
        ip_address = self.get_address_from_ip(remote_addr)
        self.log.update({"ip_address": ip_address})
        response = super(LogRequestMixin, self).finalize_response(request, response, *args, **kwargs)
        return response

    def handle_log(self):
        """
        Hook to define what happens with the log.

        Defaults on saving the data on the db.
        """
        self.log["log_type"] = RequestLog.IN
        RequestLog(**self.log).save()

