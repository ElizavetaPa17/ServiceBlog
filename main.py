from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import redis
import datetime, random

# redis creation
r = redis.Redis()
app = FastAPI()

@app.get("/view")
def view(user_id: int):
    return r.hgetall(f"user_blog{user_id}")

@app.post("/create")
def create(author: str = Query(min_length=2, max_length=30),
           text: str = Query(min_length=1)):
    current_date = datetime.datetime.now()
    new_id = random.randint(0, 1e5) + current_date.toordinal()
    new_post = {"blog_ID": new_id, "author": author, "post_data": current_date.strftime("%H:%M:%S:%Y"),
                "text": text}
    r.hmset(f"user_blog{new_id}", new_post)

    return r.hgetall(f"user_blog{new_id}")

@app.put("/update")
def update(user_id: int,
           text: str = Query(min_length=1)):
    r.hset(f"user_blog{user_id}", "blog_ID", user_id)
    r.hset(f"user_blog{user_id}", "post_data", datetime.datetime.now().strftime("%H:%M:%S:%Y"))
    r.hset(f"user_blog{user_id}", "text", text)

    return r.hgetall(f"blogs:{user_id}")

@app.delete("/delete")
def delete(user_id: int):
    r.delete(f"blogs:{user_id}")

    return JSONResponse(content=f"Blog with{user_id} was deleted")


"""
Задание:
Реализовать сервис блога.

Требования к функционалу:
- Ендпоинты для работы с блогом 
(/create, /update, /view, /delete)

Требования к реализации:
- данные хранить в Redis

Минимальные требования к коду:
- Код на github
- Кодстайл по PEP

"""