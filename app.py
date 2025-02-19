from fastapi import FastAPI, Request, Response
from config import CONFIRMATION
from responses_logic import message_handler
from methods import send_message
from actions_base import check_user_in_database_and_return_act

app = FastAPI()




@app.post('/callback')
async def callback(request: Request):
    data = await request.json()

    if 'type' in data:
        if data['type'] == 'confirmation':
            return Response(content=CONFIRMATION, media_type="text/plain")

        elif data['type'] == 'message_new':
            message_info = data['object']['message']
            user_id = message_info.get('from_id', 'Не указано')
            message = message_info.get('text', 'Не указано').lower()

            user_act = await check_user_in_database_and_return_act(user_id)








            return 'ok'
    return 'ok'


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
