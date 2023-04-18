import time
from datetime import datetime
import vk_api
from VK_TOKEN import TOKEN
vk_session=vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

def getOnline(shortname):
    try:
        id = vk.utils.resolveScreenName(screen_name=shortname)['object_id']
        user=vk.users.get(user_ids=id,fields='online')
        return user
    except:
        return 'Произошла ошибка'

