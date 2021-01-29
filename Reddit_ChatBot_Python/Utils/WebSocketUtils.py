from urllib.parse import urlencode
import requests
from .CONST import SB_User_Agent, SB_PROXY_CHATMEDIA


def get_ws_url(socket_base, params):
    return f"{socket_base}/?{urlencode(params)}"


def print_chat_(resp, channelid_sub_pairs):
    if resp.type_f == "MESG":
        print(f"{resp.user.name}@{channelid_sub_pairs.get(resp.channel_url)}: {resp.message}")


def get_current_channels(user_id, logi_key):
    headers = {
        'session-key': logi_key,
        'SB-User-Agent': SB_User_Agent,
        'User-Agent': None
    }
    params = {
        'show_member': 'true',
        'show_frozen': 'true',
        'public_mode': 'all',
        'member_state_filter': 'joined_only',
        'super_mode': 'all',
        'limit': '40',
        'show_empty': 'true'
    }
    response = requests.get(f'{SB_PROXY_CHATMEDIA}/v3/users/{user_id}/my_group_channels', headers=headers, params=params).json()
    channelid_sub_pairs = {}
    for channel in response.get('channels', {}):
        room_name = None
        if channel['custom_type'] == "direct":
            for member in channel['members']:
                if member['user_id'] != user_id:
                    room_name = member['nickname']
                    break
        else:
            room_name = channel['channel']['name']
        channelid_sub_pairs.update({channel['channel']['channel_url']: room_name})
    return channelid_sub_pairs
