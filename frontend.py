from fastapi import FastAPI
from nicegui import app, ui
import aiohttp


API_URL = 'http://127.0.0.1:8000/predict'


def build_payload(feature1, feature2, feature3, feature4):
    return {
            "feature1": feature1,
            "feature2": feature2,
            "feature3": feature3,
            "feature4": feature4,
            }


async def apicall(payload, method='post', headers=None):
    async with aiohttp.ClientSession() as session:
        if method.lower() == 'get':
            async with session.request(method, API_URL, params=payload, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        else:
            async with session.request(method, API_URL, json=payload, headers=headers) as response:
                response.raise_for_status()
                return await response.json()


def init(fastapi_app: FastAPI) -> None:
    # ############################### HOMEPAGE #######################################
    @ui.page('/')
    async def home():
        ui.markdown('## IRIS Dataset')

        # Immagine
        ui.separator()
        ui.image('https://www.embedded-robotics.com/wp-content/uploads/2022/01/Iris-Dataset-Classification.png'\
                ).classes('h-auto max-w-lg rounded-lg flex justify-center')

        # Campi di input
        feature1 = ui.number(label='Sepal Length', value=3, format='%.2f',)
        feature2 = ui.number(label='Sepal Width', value=3, format='%.2f',)
        feature3 = ui.number(label='Petal Length', value=3, format='%.2f',)
        feature4 = ui.number(label='Petal Width', value=3, format='%.2f',)

        async def handle_click(method):
            payload = build_payload(feature1.value, feature2.value, feature3.value, feature4.value)
            try:
                result = await apicall(payload, method=method)
                ui.notify(f'Result: {result}')
                markdown.content = f"### Result: {result}"
            except aiohttp.ClientError as e:
                ui.notify(f'Error: {e}')

        ui.button('Result POST', on_click=lambda: handle_click('post'))
        ui.button('Result GET', on_click=lambda: handle_click('get'))
        markdown = ui.markdown()

    # ############################### PAG2 #######################################
    @ui.page('/pag2')
    async def page2():
        ui.label('Hello, FastAPI! Pag2')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')
        ui.markdown('## Hello Guys, write something!!')
    # #################################################################################################

    ui.run_with(
                fastapi_app,
                mount_path='/',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
                storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
                )
