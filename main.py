import os
import httpx
import json

os.system('cls; clear')

with open('config.json', 'r') as f:
    token: str = json.load(f)['Token']

if os.path.exists('deleted.txt'):
    os.remove('deleted.txt')


class FriendTypes:
    FRIENDS: int = 1
    SENT: int = 4
    INCOMING: int = 3


session: httpx.Client = httpx.Client(
    headers={
        'authorization': token
    }
)

data: list = session.get(
    'https://discord.com/api/v10/users/@me/relationships').json()

to_do: list = [item for item in data if item['type'] == 3]

print(f'(!) Users to delete: {len(to_do)}')
print('Continue? (y/n)')

if input('=> ').lower() != 'y':
    print('(!) Exiting')
    os._exit(1)

for user in to_do:
    session.delete(
        'https://discord.com/api/v10/users/@me/relationships/{}'.format(
            user['id'])
    )
    with open('deleted.txt', 'a+') as f:
        f.write('Name: {}#{} | ID: {}\n'.format(
            user['user']['username'],
            user['user']['discriminator'],
            user['id']
        ))
    print('(!) Removed {}'.format(user['user']['username']))
