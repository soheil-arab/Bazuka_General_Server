import requests
user1 = {
    'username': "ede11ff8c4124de5812dd3bd3ea31",
    'password': "d9e92ab060cda44ce50c220650a5d265"
}
user2 = {
    "username": "92aa1c62dad644198d885ffa175b3",
    "password": "24edd1b1014e93c8efbd20065103f1bb"
}

def joinClan(token, clanid):
    url = 'http://localhost:8000/rest/v2/clans/{0}/join/?format=json'.format(clanid)
    headers = {'authorization': 'JWT '+token}
    r = requests.post(url, headers=headers)
    print(r.json())

def donateRequest(token, cardid):
    url = 'http://localhost:8000/rest/v2/donates/?format=json'
    headers = {'authorization': 'JWT '+token}
    r = requests.post(url, {"card_type_id": cardid}, headers=headers)
    print(r.json())

def doDonate(token, donateid):
    url = 'http://localhost:8000/rest/v2/donates/{0}/?format=json'.format(donateid)
    headers = {'authorization': 'JWT '+token}
    r = requests.post(url, headers=headers)
    print(r.json())

def login(user):
    r = requests.post('http://localhost:8000/rest/api-token-auth/', {
        "username": user['username'],
        "password": user['password']
    })
    token = r.json()['token']
    return token

def unpack(token, packid):
    url = 'http://localhost:8000/rest/v2/packs/{0}/unpack/?format=json'.format(packid)
    headers = {'authorization': 'JWT '+token}
    r = requests.post(url, headers=headers)
    print(r.json())

def unpack(token, packid):
    url = 'http://localhost:8000/rest/v2/packs/{0}/unpack/?format=json'.format(packid)
    headers = {'authorization': 'JWT '+token}
    r = requests.post(url, {'unpack_type': 'gem'}, headers=headers)
    print(r.json())

def unlock(token, packid):
    url = 'http://localhost:8000/rest/v2/packs/{0}/unlock/?format=json'.format(packid)
    headers = {'authorization': 'JWT '+token}
    r = requests.post(url, headers=headers)
    print(r.json())




token1 = login(user1)
token2 = login(user2)
unlock(token1, 1)
unpack(token1, 1)
