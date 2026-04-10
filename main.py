from fastapi import FastAPI, Depends, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime



import os
import shutil

from api.api import router
from api.users_api import router as user_router
from api.product_api import router as product_router

import models
from models import Product, Category
from database import engine, SessionLocal
from datetime import datetime
import easyocr
from models import Order
from datetime import timedelta



# create tables
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

import easyocr
import re
reader = easyocr.Reader(['th','en'])
app = FastAPI()

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="secret123")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
app.include_router(user_router)
app.include_router(product_router)


@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Hello World"
    })


@app.get("/admin/product", response_class=HTMLResponse)
def admin_product(request: Request):
    return templates.TemplateResponse("index.html", {
        'request': request,
        'username': 'Somchai',
        'email': 'somchai@mail.com',
        'score': 76,
        'activities': ['Football', 'Running', 'Badminton']
    })


@app.get("/products", response_class=HTMLResponse)
def product_list(request: Request):
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        return templates.TemplateResponse("product_list.html", {
        "request": request,
        "products": products
        })
    finally:
        db.close()


@app.get("/products/create", response_class=HTMLResponse)
def create_form(request: Request):
    db = SessionLocal()
    try:
        categories = db.query(Category).all()
        return templates.TemplateResponse("product_form.html", {
            "request": request,
            "categories": categories
        })
    finally:
        db.close()


@app.post("/products/create")
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None)
):
    db = SessionLocal()

    filename = None
    if image:
        filename = image.filename
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    product = Product(
        name=name,
        price=price,
        category_id=category_id,
        image=filename
    )

    db.add(product)
    db.commit()
    db.close()

    return RedirectResponse("/products", status_code=303)


@app.get("/products/edit/{id}", response_class=HTMLResponse)
def edit_form(request: Request, id: int):
    db = SessionLocal()
    product = db.get(Product, id)
    categories = db.query(Category).all()
    db.close()

    return templates.TemplateResponse("product_form.html", {
        "request": request,
        "product": product,
        "categories": categories
    })


@app.post("/products/edit/{id}")
def update_product(
    id: int,
    name: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None)
):
    db = SessionLocal()

    product = db.get(Product, id)
    product.name = name
    product.price = price
    product.category_id = category_id

    if image and image.filename:
        filename = image.filename
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        product.image = filename

    db.commit()
    db.close()

    return RedirectResponse("/products", status_code=303)


@app.get("/products/delete/{id}")
def delete_product(id: int):
    db = SessionLocal()

    product = db.get(Product, id)
    db.delete(product)
    db.commit()
    db.close()

    return RedirectResponse("/products", status_code=303)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sales")
def get_sales(db: Session = Depends(get_db)):
    return db.query(
        Product.customer_id,
        func.sum(Product.price).label("total_sales")
    ).group_by(Product.customer_id).all()


@app.get("/api/servertime")
def get_datetime():
    return {
    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/products/search", response_class=HTMLResponse)
def product_search(request: Request):
    return templates.TemplateResponse("product_search.html", {
        "request": request,
    })


@app.get("/api/products/search")
def product_search_api(search: str = ""):
    db = SessionLocal()
    try:
        return db.query(Product).filter(
            Product.name.like(f"%{search}%")
        ).all()
    finally:
        db.close()
@app.get("/pvs/upload", response_class=HTMLResponse)
def pvs_upload(request: Request):
    return templates.TemplateResponse("pvs_upload.html", {
        "request": request,
    })

@app.post("/api/pvs/upload-ocr")
async def upload_ocr(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = process_ocr(filepath)
    return result

def process_ocr(image_path):
    result = reader.readtext(image_path)
    text = " ".join([r[1] for r in result])
    # Extract amount
    amount_match = re.search(r'\d+\.\d{2}', text)
    amount = float(amount_match.group()) if amount_match else 0
    # Extract date
    date_match = parse_thai_datetime(text)
    return {
        "text": text,
        "amount": amount,
        "datetime": date_match,
    }

def parse_thai_datetime(text):
    thai_months = {
        "ม.ค.": 1, "ก.พ.": 2, "มี.ค.": 3,
        "เม.ย.": 4, "พ.ค.": 5, "มิ.ย.": 6,
        "ก.ค.": 7, "ส.ค.": 8, "ก.ย.": 9,
        "ต.ค.": 10, "พ.ย.": 11, "ธ.ค.": 12
    }

    match = re.search(
        r'(\d{1,2})\s+([^\s]+)\s+(\d{2})(?:.*?(\d{1,2}):(\d{2}))?',
        text
    )

    if not match:
        raise ValueError("Invalid date format")

    day = int(match.group(1))
    month = thai_months.get(match.group(2), 1)
    year_ad = int(match.group(3)) + 2500 - 543

    time_match = re.search(r'(\d{1,2}):(\d{2})', text)
    hour = int(time_match.group(1))
    minute = int(time_match.group(2))
    return datetime(year_ad, month, day, hour, minute)

@app.get("/api/pvs/orders")
def get_orders():
    db = SessionLocal()
    try:
        orders = db.query(Order).all()
        return [
            {
                "id": o.id,
                "order_no": o.order_no,
                "amount_total": o.amount_total,
                "order_date": str(o.order_date),
                "state": o.state
            }
            for o in orders
        ]
    finally:
        db.close()

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str =
Form(...)):
    if username == "admin" and password == "1234":
        request.session["user"] = username
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Login failed"
    })

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    return user
