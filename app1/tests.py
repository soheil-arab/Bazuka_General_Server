import requests

username = "ede11ff8c4124de5812dd3bd3ea31"
password = "d9e92ab060cda44ce50c220650a5d265"

r = requests.post('http://localhost:8000/rest-auth/login/',{
    "username": username,
    "password": password
})


cookies = r.cookies.get_dict()
# url = 'http://localhost:8000/rest/v2/username/?format=json'
# r2 = requests.post(url, {'username': 'soheil1'}, cookies=cookies, headers={'X-CSRFToken': cookies['csrftoken']})
# print(r2.json())

# url = 'http://localhost:8000/rest/v2/?format=json'
# r2 = requests.get(url, cookies=cookies, headers={'X-CSRFToken': cookies['csrftoken']})
# print(r2.json())

url = 'http://localhost:8000/rest/v2/?format=json'
r2 = requests.get(url, headers={'X-CSRFToken': cookies['csrftoken']})
print(r2.status_code)
