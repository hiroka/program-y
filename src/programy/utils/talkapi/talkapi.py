from programy.utils.logging.ylogger import YLogger
import json
import requests
import urllib.request

# docomo zatsudan API

class TalkAPI(object):

    BASE_URL ="https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY=%s"
    APP_URL = "https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/registration?APIKEY=%s"

    def __init__(self, license_keys, talk_api_api=None):

        if license_keys is None:
            raise Exception("Missing license keys")

        if license_keys.has_key('TALKAPI_API_KEY'):
            self.api_key = license_keys.get_key('TALKAPI_API_KEY')
        else:
            raise Exception("No valid license key TALKAPI_API_KEY found")

    @staticmethod
    def _format_url(api_key):
        return TalkAPI.BASE_URL%(api_key)

    @staticmethod
    def _format_url_app(api_key):
        return TalkAPI.APP_URL%(api_key)

    def get_headlines(self, source, max_articles=0, sort=False, reverse=False):

         #GET APP_ID
         url = TalkAPI._format_url_app(self.api_key)
         method = "POST"
         headers = {"Content-Type" : "application/json"}
         obj = { "botId" : "Chatting",
                 "appKind" : "CDI"}
         json_data = json.dumps(obj).encode("utf-8")
         request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
         with urllib.request.urlopen(request) as response:
             response_body = response.read().decode("utf-8")
         body = json.loads(response_body)
         appId = body['appId']

         #Get Response
         url = TalkAPI._format_url(self.api_key)
         method = "POST"
         headers = {"Content-Type" : "application/json"}
         obj = {"language" : "ja-JP" ,
                 "botId" : "Chatting",
                 "appId" : appId,
                 "voiceText": source,
                 "appRecvTime": "2015-05-05 13:30:00",
                 "appSendTime": "2015-05-05 13:31:00"}
         json_data = json.dumps(obj).encode("utf-8")

         request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
         with urllib.request.urlopen(request) as response:
             response_body = response.read().decode("utf-8")

         utt_body = json.loads(response_body)
         utt = utt_body['systemText']['expression']
         return utt
