from fastapi import FastAPI, Request, Response
from config import CONFIRMATION
from actions_base import check_user_in_database_and_return_act, user_act_handler, change_act_after_callback
from base import database_implementation
import asyncio

app = FastAPI()


@app.post('/callback')
async def callback(request: Request):
    data = await request.json()
    print(data)

    try:
        if 'type' in data:
            if data['type'] == 'confirmation':
                return Response(content=CONFIRMATION, media_type="text/plain")

            elif data['type'] == 'message_new':
                message_info = data['object']['message']
                user_id = message_info.get('from_id', 'Не указано')
                message_incoming = message_info.get('text', 'Не указано').lower()
                user_act = await check_user_in_database_and_return_act(user_id)

                asyncio.create_task(user_act_handler(user_id, user_act, message_incoming))
                return Response(content='ok', media_type="text/plain")

            elif data['type'] == 'message_event':
                message_info = data['object']
                user_id = message_info.get('peer_id', 'Не указано')
                payload = data['object']['payload']
                payload_user_act = payload.get('command', 'Не указано')
                user_act = await change_act_after_callback(user_id, payload_user_act)

                asyncio.create_task(user_act_handler(user_id, user_act))
                return Response(content='ok', media_type="text/plain")

        return Response(content='ok', media_type="text/plain")

    except Exception as e:
        print(f"Ошибка: {e}")
        return None


if __name__ == '__main__':
    import uvicorn
    asyncio.run(database_implementation())
    uvicorn.run(app, host="127.0.0.1", port=8080)
