from sqlalchemy import Column, String, Integer, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from Base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    def __init__(self, nm, em, pas):
        self.username = nm
        self.email = em
        self.password = pas

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    def __init__(self,nm):
        self.name = nm

class SubCategory(Base):
    __tablename__ = "subcategories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    number = Column(Integer)
    catId = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE', onupdate='CASCADE'))
    cat = relationship('Category', backref='subcategories')
    def __init__(self,nm, cat1):
        self.name = nm
        self.number = 0
        self.cat = cat1

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
    details = Column(String(500))
    discount = Column(Float)
    stock = Column(Integer)
    brand = Column(String(50))
    img = Column(String(50))
    subCatId = Column(Integer, ForeignKey('subcategories.id', ondelete='CASCADE', onupdate='CASCADE'))
    subCat = relationship('SubCategory', backref='products')
    def __init__(self,pr, dis,stk, br, nm, img, subC, dtl):
        self.name = nm
        self.price = pr
        self.details = dtl
        self.stock = stk
        self.brand = br
        self.discount = dis
        self.img = img
        self.subCat = subC

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    orderId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    order = relationship('User', backref='cart')
    productId = Column(Integer, ForeignKey('products.id', ondelete='CASCADE', onupdate='CASCADE'))
    prod = relationship('Product', backref='cart')
    def __init__(self, quant, ord, prd):
        self.quantity = quant
        self.order = ord
        self.prod = prd

class Wishlist(Base):
    __tablename__ = "wish"
    id = Column(Integer, primary_key=True)
    orderId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    order = relationship('User', backref='wish')
    productId = Column(Integer, ForeignKey('products.id', ondelete='CASCADE', onupdate='CASCADE'))
    prod = relationship('Product', backref='wish')
    def __init__(self, ord, prd):
        self.order = ord
        self.prod = prd

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    noOfProducts = Column(Integer)
    dat = Column(Date)
    subTotal = Column(Float)
    total = Column(Integer)
    discount = Column(Float)
    userId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    use = relationship('User', backref='orders')
    def __init__(self,nm, dt, dis, subT, t,  cat1):
        self.noOfProducts = nm
        self.subTotal = subT
        self.total = t
        self.discount = dis
        self.dat = dt
        self.use = cat1

class OrderProduct(Base):
    __tablename__ = "orderProducts"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    orderId = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE', onupdate='CASCADE'))
    order = relationship('Order', backref='orderProducts')
    productId = Column(Integer, ForeignKey('products.id', ondelete='CASCADE', onupdate='CASCADE'))
    prod = relationship('Product', backref='orderProducts')
    def __init__(self, quant, ord, prd):
        self.quantity = quant
        self.order = ord
        self.prod = prd

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    address1 = Column(String(100))
    address2 = Column(String(100))
    phone = Column(String(14))
    zip = Column(Integer)
    type = Column(String(50))
    card = Column(Integer)
    cvc = Column(Integer)
    userId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    use = relationship('User', backref='payments')
    def __init__(self,nm, nm1, add1, add2, ph, z, tp, crd, cv, ct):
        self.firstName = nm
        self.lastName = nm1
        self.address1 = add1
        self.address2 = add2
        self.phone = ph
        self.zip = z
        self.type = tp
        self.card = crd
        self.cvc = cv
        self.use = ct