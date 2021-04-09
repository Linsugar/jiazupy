from qiniu import Auth, put_file, etag
import qiniu.config
q = Auth(access_key='cyIcJU0RXy1nD1t0I6DauqqCblEcFX1npjtld5Ky',secret_key='Vt7Yw39U3COUnW1uavsLMRpPiSCtQ8mdJ0Hl2vmK')
#要上传的空间
bucket_name = 'familytang'
#上传后保存的文件名
key = 'my.png'
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
#要上传文件的本地路径
localfile = './image/uimage.jpg'
ret, info = put_file(token, key, localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)