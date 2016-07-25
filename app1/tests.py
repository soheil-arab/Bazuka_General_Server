import requests

# username = "ede11ff8c4124de5812dd3bd3ea31"
# password = "d9e92ab060cda44ce50c220650a5d265"
#
# r = requests.post('http://localhost:8000/api-token-auth/', {
#     "username": username,
#     "password": password
# })
#
# print(r.text)
# token = r.json()['token']
# url = 'http://localhost:8000/rest/v2/username/?format=json'
# r2 = requests.post(url, {'username': 'soheil1'}, cookies=cookies, headers={'X-CSRFToken': cookies['csrftoken']})
# print(r2.json())

# url = 'http://localhost:8000/rest/v2/me/?format=json'
# r2 = requests.get(url, cookies=cookies, headers={'X-CSRFToken': cookies['csrftoken']})
# print(r2.json())

# url = 'http://localhost:8000/rest/v2/me/pack/1?format=json'
# r2 = requests.post(url, headers={'X-CSRFToken': cookies['csrftoken']}, cookies=cookies)
# print(r2.text)
# print(r2.status_code)

# url = 'http://localhost:8000/rest/v2/cards/1/?format=json'
# headers = {
#     'authorization': 'JWT '+token
# }
# r2 = requests.post(url, headers=headers)
# print(r2.json())


auth_id = "5795af35e4b0781338a4efa7"

url = "https://api.backtory.com/auth/users"
headers = {
    "X-Backtory-Authentication-Id": auth_id,
    "Content-Type": "application/json"
}
data = {
    "firstName": "",
    "lastName": "",
    "username": "rezausername2",
    "password": "salamreza2",
    "email": "",
    "phoneNumber": ""
}
r1 = requests.post(url, json=data, headers=headers)
print(r1.status_code)
print(r1.json())
