from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from choice_db import get_dbms


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/choice-db/')
async def root(
    data_must_always_be_correct: Optional[bool] = False,
    cant_lose_data: Optional[bool] = False,
    high_access_differentiation: Optional[bool] = False,
    analyze_big_data: Optional[bool] = False,
    analyze_huge_data: Optional[bool] = False,
    fast_response: Optional[bool] = False,
    store_big_data: Optional[bool] = False,
    geo_independency: Optional[bool] = False,
    must_be_free: Optional[bool] = False,
    working_with_texts: Optional[bool] = False,
    works_from_box: Optional[bool] = False,
    no_needs_server: Optional[bool] = False,
    dbms_count: Optional[int] = 3,
):
    requirements = []
    if data_must_always_be_correct:
        requirements.append('data_must_always_be_correct')
    if cant_lose_data:
        requirements.append('cant_lose_data')
    if high_access_differentiation:
        requirements.append('high_access_differentiation')
    if analyze_big_data:
        requirements.append('analyze_big_data')
    if analyze_huge_data:
        requirements.append('analyze_huge_data')
    if fast_response:
        requirements.append('fast_response')
    if store_big_data:
        requirements.append('store_big_data')
    if geo_independency:
        requirements.append('geo_independency')
    if must_be_free:
        requirements.append('must_be_free')
    if working_with_texts:
        requirements.append('working_with_texts')
    if works_from_box:
        requirements.append('works_from_box')
    if no_needs_server:
        requirements.append('no_needs_server')

    return get_dbms(requirements, dbms_count=dbms_count)


@app.get('/', response_class=HTMLResponse)
async def root():
    return """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Программа</title>
            <link rel="stylesheet" href="static/style.css">
            <script src="static/script.js" defer></script>
        </head>
        <body>
            <main>
                <form id="form">
                </form>
                <div id="databases_text">
                </div>
            </main>
        </body>
        </html>
    """
