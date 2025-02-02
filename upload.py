from bots_init import vk_ms
import asyncio
import logging
import vk_api


async def attachment():
    upload = vk_api.VkUpload(vk_ms)
    photo = None
    while not photo:
        try:
            photo = upload.photo_messages('prices.jpg')
            logging.info(f"Фото загружено: {photo}")
        except KeyboardInterrupt:
            logging.error(f"Программа была прервана: {KeyboardInterrupt}")
            await asyncio.sleep(10)

    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment_ph = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment_ph
