'''
document example:
{
    'user_uuid': '1234567890',
    'auth': {
        'type': 'access_token',
        'value': {
            'access_token': '...'
        }
    },
    'conversation': {
        'last_conversation_id': '1234567890',
    },
    'config': {
        'paid': True,
    }
}
'''
import pymongo

'''
Constant Configuration
'''
DATABASE_NAME = 'chatgpt-discord-V1'

def connect_to_database(server_url: str) -> pymongo.MongoClient:
    client = pymongo.MongoClient(server_url)
    return client


def get_user_data(client: pymongo.MongoClient, user_uuid: str):
    user_data = client[DATABASE_NAME]['user'].find_one(
        {'user_uuid': user_uuid}
    )
    return user_data

def set_user_data(client: pymongo.MongoClient, user_uuid: str, user_data: dict) -> None:
    client[DATABASE_NAME]['user'].update_one(
        {'user_uuid': user_uuid},
        {'$set': user_data},
        upsert=True
    )

'''
auth getter/setter
'''
def get_user_auth(client: pymongo.MongoClient, user_uuid: str):
    if (user_data := get_user_data(client, user_uuid)) is None:
        return None
    return user_data['auth']

def set_user_auth(client: pymongo.MongoClient, user_uuid: str, user_auth: dict) -> None:
    set_user_data(client, user_uuid, {
        'auth': user_auth
    })

'''
last conversation getter/setter
'''
def get_last_conversation(client: pymongo.MongoClient, user_uuid: str):
    if (user_data := get_user_data(client, user_uuid)) is None:
        return None
    return user_data.get('conversation', {}).get('last_convarsation_id')

def set_last_conversation(client: pymongo.MongoClient, user_uuid: str, conversation_id: str) -> None:
    set_user_data(client, user_uuid, {
        'conversation': {
            'last_conversation_id': conversation_id
        }
    })
