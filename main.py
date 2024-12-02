from fastapi import FastAPI, Query, Body
import uvicorn

# если плохо подгружается документация
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()

# если плохо подгружается документация
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'}
]

@app.get('/hotels',
         summary="Получить все отели",
         description="<h1>Здесь можно посмотреть список всех отелей в базе</h1>")
def get_hotels():
    return hotels


@app.get("/hotel", summary="Получить отель по названию")
def get_hotel(
        title: str | None = Query(None, description="Название отеля"),
):

    return [hotel for hotel in hotels if title == hotel['title']]


@app.delete('/delete/{hotel_id}', summary="Удаление отеля")
def del_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'Ok'}

@app.post("/hotels", summary="Добавление отеля")
def create_hotel(
    title: str = Body(embed=True),
    name: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}", summary="Редактирование отеля")
def put_hotel(hotel_id: int,
               title: str = Body(embed=True),
               name: str = Body(embed=True)
               ):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]

    hotel['name'] = name
    hotel['title'] = title

    return {"status": "OK"}

@app.patch("/hotels/{hotel_id}", summary="Частичное редактирование отеля")
def patch_hotel(hotel_id: int,
               title: str | None = Body(None),
               name: str | None = Body(None)
               ):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]

    if name:
        hotel['name'] = name
    if title:
        hotel['title'] = title

    return {"status": "OK"}



if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)

