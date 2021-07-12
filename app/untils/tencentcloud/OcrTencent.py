import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

SecretId = 'AKID3sRM3U4bkeQwSajT4YoqnVgdOsUhdQsn'
SecretKey = 'oOhldGdNwoTs0tWtSl5B1cY5MRFn57tV'
try:
    cred = credential.Credential(SecretId, SecretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

    req = models.GeneralAccurateOCRRequest()
    params = {
        "ImageUrl": "http://qtr6xp7uf.hn-bkt.clouddn.com/ocrtest.jpg"
    }
    req.from_json_string(json.dumps(params))

    resp = client.GeneralAccurateOCR(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)