from database import SessionLocal, engine, Base
from models import Category, Product, User, Customer, Order, OrderDetail
from datetime import datetime

db = SessionLocal()
import os
print("DB Path =", os.path.abspath("mydb.sqlite3"))


def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)


def run_seed():
    db.add_all([
        Category(name='นิยาย'),
        Category(name='การ์ตูน'),
        Category(name='เกษตร'),
        Category(name='คอมพิวเตอร์'),
    ])
    db.commit()

    db.add_all([
        Product(name='เดอะลอร์ดออฟเดอะริงส์', price=400, category_id=1),
        Product(name='ซึบาสะ', price=150, category_id=2),
        Product(name='สร้าง Frontend ด้วย Next.js', price=350, category_id=4),
        Product(name='เรียนรู้การทำ API ด้วย FastAPI', price=550, category_id=4),
    ])
    db.commit()

    db.add_all([
        User(name='Admin' ,email = 'admin@gmail.com' , role_id = 1 , role_name = 'Admin'),
        User(name='User1' ,email = 'user1@gmail.com' , role_id = 2 , role_name = 'Manager'),
        User(name='User2' ,email = 'user2@gmail.com' , role_id = 3, role_name = 'Staff'),
        User(name='User3' ,email = 'user3@gmail.com' , role_id = 3, role_name = 'Staff'),
        User(name='User4' ,email = 'user4@gmail.com' , role_id = 3, role_name = 'Staff'),
    ])
    db.commit()

    db.add_all([
        Customer(name='ร้านตัวอย่าง'),
        Customer(name='คุณสมชาย'),
        Customer(name='คุณสุพิชยา'),
    ])
    db.commit()

    db.add_all([
        Order(
            order_no='X001',
            user_id=1,
            customer_id=1,
            amount_untaxed=93.46,
            amount_tax=6.54,
            amount_total=100,
        ),

        Order(
            order_no='X002',
            user_id=1,
            customer_id=2,
            amount_untaxed=373.83,  # A = C x (100/107)
            amount_tax=26.16, # B = C - A
            amount_total=400,  #ตัวแปรc
        )

    ])
    db.commit()

    db.add_all([
        OrderDetail(
            order_id=1,
            product_id=1,
            qty=1,
            price=100,
            amount=100,
        )
    ])
    db.commit()

db.add_all([
    Order(
        order_no="X001",
        amount_total=200,
        order_date=datetime(2021, 7, 10, 15, 10),
        state="Draft"
    ),
    Order(
        order_no="X002",
        amount_total=200,
        order_date=datetime(2021, 7, 10, 15, 25),
        state="Draft"
    ),
    Order(
        order_no="X003",
        amount_total=500,
        order_date=datetime(2021, 7, 10, 16, 0),
        state="Draft"
    ),
])
db.commit()

# def reset_database():
#     print("Dropping all tables...")
#     Base.metadata.drop_all(bind=engine)
#     print("Creating tables...")
#     Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
    run_seed()
