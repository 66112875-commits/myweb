from fastapi import APIRouter
from database import SessionLocal
from models import Product , Category
from schemas.product import ProductSchema
from sqlalchemy import or_
from sqlalchemy import func


router = APIRouter()

ENDPOINT = '/api/v1'

@router.get(ENDPOINT + '/products', response_model=list[ProductSchema])
async def product_list(): 
    db = SessionLocal()     # connect db
    try:
        # products = db.query(Product).all()
        products = db.query(Product).filter(Product.price > 390)
        # products = db.query(Product).filter( or_(Product.price < 200, Product.price > 500) ).all()
        # products = db.query(Product).filter(Product.category_id.in_([1, 4])).all()
        # products = db.query(Product).filter(Product.name.contains("API")).all()
        # products = db.query(Product).order_by(Product.name.asc()).limit(2)
        return products
    finally:        #เลิกใช้
        db.close()
    return 





