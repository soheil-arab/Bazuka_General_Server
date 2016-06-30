# import requests
#
#
# # r = requests.post('http://localhost:8000/rest-auth/login/',{
# #     "username": "behzad",
# #     "password": "e100603ebfd7bc525059cfd2dac33a25"
# # })
# #
# # print(r.json()['key'])
# url = 'http://localhost:8000/rest-auth/user/'
# # print(r.cookies.get_dict())
#
# r2 = requests.get(url,cookies={'csrftoken': 'yiYKeKoOzusgbxo9nUqkojdbg3fYS7q7', 'sessionid': '3sdprsg90gwd6z75cf2bk4inib5zlmhk'})
# print(r2.json())


import uuid
import base64
from baseconv import base36
# uuid = base64.b64encode(uuid.uuid4().bytes).replace('=', '')
print(uuid.uuid4().hex)
