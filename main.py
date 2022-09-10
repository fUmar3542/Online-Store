import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Base import Session, engine, Base
from flask import Flask, session, render_template, request, url_for, redirect, jsonify
from Model import User, Order, Category, SubCategory, Product, OrderProduct, Wishlist, Cart
from sqlalchemy import or_
import os

adminUsername = 'Umar'
data = []             # For categories name with their subcategories list

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = "anony"

Base.metadata.create_all(engine)
db = Session()

def all_prod():
    prod = []
    dat = db.query(Product).filter().order_by(Product.id.desc()).all()
    for x in dat:
        prod.append(x.id)
    return prod

def new_arrival():
    dat = db.query(Product).filter().order_by(Product.id.desc()).limit(8)
    return dat

def refresh():
    cat = db.query(Category).all()
    data.clear()
    i = 0
    for x in cat:
        data.append({"name": x.name,
                     "subcat": []})
        sub = db.query(SubCategory).filter(SubCategory.catId == x.id)
        for y in sub:
            data[i]['subcat'].append(y.name)
        i = i+1

def updated_sub_category_list(value):
    sub_category = []
    sub_cat = db.query(SubCategory).filter(SubCategory.name == value).first()
    prod = db.query(Product).filter(Product.subCatId == sub_cat.id)
    for x in prod:
        sub_category.append(x)
    return sub_category

def return_collection(col,type):
    products = []
    cat1 = ""
    cat2 = ""
    if type == "trendy":
        cat1 = "Attire's"
        cat2 = "Cosmetics"
    elif type == "beauty":
        cat1 = "Fragrances"
        cat2 = "Cosmetics"
    elif type == "home":
        cat1 = "Home Decor"
        cat2 = "Grocery"
    else:
        cat1 = "Electronics"
        cat2 = "Accessories"
    if col == "Discount %":
        dat = db.query(Product
                ).join(
                SubCategory
                ).join(
                Category
                ).filter(
                ((Product.discount > 0) & (or_(Category.name == cat1, Category.name == cat2)))
        ).all()
    else:
        dat = db.query(Product
                ).join(
                SubCategory
                ).join(
                    Category
                ).filter(
                    (or_(Category.name == cat1, Category.name == cat2))
        ).order_by(Product.id.desc()).limit(12)
    for x in dat:
        products.append(x.id)
    return products

def add_to_cart(id,quantity):
    prod = db.query(Product).filter(Product.id == id).first()
    user = db.query(User).filter(User.username == session['username']).first()
    check = db.query(Cart).filter((Cart.userId == user.id) & (Cart.productId == prod.id)).first()
    if check == None:  # If product not present in cart
        if prod.stock < quantity:
            return render_template("error1.html", Message="Required quantity not available......")
        wish_product = db.query(Wishlist).filter((Wishlist.userId == user.id) & (Wishlist.productId == prod.id)).first()
        if wish_product != None:
            db.query(Wishlist).filter((Wishlist.userId == user.id) & (Wishlist.productId == prod.id)).delete()
            db.commit()
        total = quantity * prod.price
        obj = Cart(quantity, total, user, prod)
        db.add(obj)
        db.commit()
        return True
    else:       # update quantity
        check.quantity = quantity
        check.total = quantity * prod.price
        db.commit()
        return False

def return_wishlist_and_cart():
    cart2 = db.query(Product.id, Product.name, Product.price, Product.img, Cart.quantity, Cart.total).join(
        Cart).join(User).filter((User.username == session['username']) & (Product.stock >= Cart.quantity)).all()
    cart_total = 0
    for x in cart2:
        cart_total += x.total
    wish = db.query(Product).join(Wishlist).join(User).filter(User.username == session['username']).all()
    return cart2, wish, cart_total

@app.route('/api/<val>', methods=['get','post'])
def return_product(val):
    arr = []
    if request.method == 'GET':
        dat = db.query(Product).filter(Product.id == val).first()
        arr = [dat.id,dat.name,dat.price,dat.brand,dat.stock,dat.discount,dat.details]
    return jsonify(arr)

@app.route('/order', methods=['get', 'post'])
def place_order():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone_no")
        email = request.form.get("email")
        country = request.form.get("country")
        city = request.form.get("city")
        address1 = request.form.get("address2")
        address2 = request.form.get("address2")
        district = request.form.get("district")
        zip = request.form.get("zip")
        main_address = address1 + " " + city + " " + district + " " + country
        tp = "Card payment"
        discount = 0
        temp_address = ""
        if address2 != "":
            temp_address = address2 + " " + city + " " + district + " " + country
        cart, wish, cart_total = return_wishlist_and_cart()
        order_total = cart_total + 10
        user = db.query(User).filter(User.username == session['username']).first()
        obj = Order(first_name, last_name, main_address, temp_address, phone, email, zip, tp, discount, cart_total, order_total, user)
        db.add(obj)
        db.commit()
        order = db.query(Order).join(User).filter(User.username == session['username']).order_by(Order.id.desc()).first()
        for x in cart:
            product = db.query(Product).filter(Product.id == x.id).first()
            ord = OrderProduct(x.quantity,order,product)
            db.add(ord)
        db.query(Cart).filter(Cart.userId == user.id).delete()
        db.commit()
        message = "Your order has been placed\n Order will arrive in between 7-10 working days.\n Thanks for purchasing ....."
        return render_template("error1.html", Message=message)

@app.route('/checkout', methods=['get', 'post'])
def checkout():
    cart1, wish1, cart_total1 = return_wishlist_and_cart()
    order_total = cart_total1 + 10
    return render_template("checkout.html", login=True, admin=False, data=data, wish=wish1, cart=cart1,
                           cart_total=cart_total1, order_total=order_total)

@app.route('/faq.html', methods=['get', 'post'])
def faq():
    new_arrive = new_arrival()
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("faq.html", login=True, admin=True, data=data, new=new_arrive)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("faq.html", login=True, admin=False, data=data, wish=wish, cart=cart,
                               cart_total=cart_total, new=new_arrive)
    else:
        return render_template("faq.html", login=False, admin=False, data=data, new=new_arrive)

@app.route('/wish-list', methods=['get', 'post'])
def wish_list():
    if 'username' in session:
        cart, wish, cart_total = return_wishlist_and_cart()
        wish_total = 0
        for x in wish:
            wish_total += x.price
        return render_template("wish-list.html", login=True, admin=False, data=data, wish=wish, cart=cart,
                               wish_total=wish_total)
    return redirect(url_for("logout"))

@app.route('/cart-list', methods=['get', 'post'])
def cart_list():
    if 'username' in session:
        cart, wish, cart_total = return_wishlist_and_cart()
        return render_template("cart-list.html", login=True, admin=False, data=data, wish=wish, cart=cart,
                               cart_total=cart_total)
    return redirect(url_for("logout"))

@app.route('/update', methods=['get', 'post'])
def update():
    if request.method == "POST":
        qtc_data = request.get_json()
        prod = db.query(Product).join(Cart).join(User).filter(User.username == session['username']).all()
        crt = db.query(Cart).join(User).filter((User.username == session['username'])).all()
        index = 0
        for x in crt:
            x.quantity = int(qtc_data[index])
            x.total = x.quantity * (prod[index].price)
            index = index + 1
        db.commit()
    results = {'processed': 'true'}
    return jsonify(results)

@app.route('/added-to-cart/<id>/<quantity>', methods=['get', 'post'])
def add_cart(id, quantity):
    if 'username' in session:
        if (session['username'] != adminUsername):
            f = add_to_cart(id,int(quantity))
        return redirect(request.referrer)
    return redirect(url_for("logout"))

@app.route('/removed-from-cart/<id>', methods=['get', 'post'])
def remove_cart(id):
    prod = db.query(Product).filter(Product.id == id).first()
    user = db.query(User).filter(User.username == session['username']).first()
    db.query(Cart).filter((Cart.userId == user.id) & (Cart.productId == prod.id)).delete()
    db.commit()
    return redirect(request.referrer)

@app.route('/Added-To-WishList/<id>', methods=['get', 'post'])
def add_wishlist(id):
    if 'username' in session:
        if (session['username'] == adminUsername):
            return redirect(request.referrer)
        else:
            prod = db.query(Product).filter(Product.id == id).first()
            user = db.query(User).filter(User.username == session['username']).first()
            check = db.query(Wishlist).filter((Wishlist.userId == user.id) & (Wishlist.productId == prod.id)).first()
            cart_check = db.query(Cart).filter((Cart.userId == user.id) & (Cart.productId == prod.id)).first()
            if (check == None) & (cart_check == None):     # Not present in wishlist and cart
                obj = Wishlist(user, prod)
                db.add(obj)
                db.commit()
            return redirect(request.referrer)
    return redirect(url_for("logout"))

@app.route('/removed-from-wishlist/<id>', methods=['get', 'post'])
def remove_wishlist(id):
    prod = db.query(Product).filter(Product.id == id).first()
    user = db.query(User).filter(User.username == session['username']).first()
    db.query(Wishlist).filter((Wishlist.userId == user.id) & (Wishlist.productId == prod.id)).delete()
    db.commit()
    return redirect(request.referrer)

@app.route('/hidden', methods=['get', 'post'])
def reload():
    return redirect(request.referrer)

@app.route('/search', methods=['get', 'post'])
def search():
    if request.method == 'POST':
        value = request.form.get("value").upper().split()   # Splitting each keyword
        prod = []
        dat = db.query(Product).filter().order_by(Product.id.desc()).all()
        for x in dat:
            name = x.name.upper().split()
            brand = x.brand.upper().split()
            for i in value:
                if (i in name) or (i in brand):
                    prod.append(x.id)
        session['list_product_ids'] = list(dict.fromkeys(prod))   # Removing duplicates
        session['list_product_name'] = request.form.get("value")
        return redirect(url_for("list_product"))

@app.route('/all/products', methods=['get', 'post'])
def all_products():
    products = all_prod()
    session['list_product_ids'] = products
    session['list_product_name'] = "All Products"
    return redirect(url_for("list_product"))

@app.route('/<value>', methods=['get', 'post'])
def main_category(value):
    session['main_category'] = value
    return redirect(url_for("categories_page2"))

@app.route('/categories', methods=['get', 'post'])
def categories_page2():
    name = session['main_category']
    cat = db.query(Category).filter(Category.name == name).first()
    if cat != None:
        sub_categories = db.query(SubCategory).filter(SubCategory.catId == cat.id).all()
    else:
        sub_categories= []
    if 'username' in session:
        if session['username'] == adminUsername:
            return render_template("categories-page2.html", login=True, admin=True, data=data, categories=sub_categories, main=name)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("categories-page2.html",login=True, admin=False, data=data, categories=sub_categories, main=name, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("categories-page2.html", login=False, admin=False,data=data, categories=sub_categories, main=name)

@app.route('/Main/<value>', methods=['get', 'post'])
def show_category_products(value):
    products = []
    t = db.query(Product.id).join(SubCategory).filter(SubCategory.name == value).all()
    for x in t:
        products.append(x.id)
    session['list_product_ids'] = products
    session['list_product_name'] = value
    return redirect(url_for("list_product"))

@app.route('/collection/<value>', methods=['get', 'post'])
def collection(value):
    session['collection'] = value
    return redirect(url_for("collection_page"))

@app.route('/collection/<col>/<type>', methods=['get','post'])
def collect(col,type):
    t = return_collection(col,type)
    session['list_product_ids'] = t
    session['list_product_name'] = col
    return redirect(url_for("list_product"))

@app.route('/products', methods=['get', 'post'])
def list_product():
    products = []
    name = session['list_product_name']
    for x in session['list_product_ids']:
        products.append(db.query(Product).filter(Product.id == x).first())
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("list-product.html", login=True, admin=True, data=data, items=products, name=name)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("list-product.html", login=True, admin=False, data=data, items=products, name=name, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("list-product.html", login=False, admin=False, data=data, items=products, name=name)

@app.route('/products/<id>', methods=['get', 'post'])
def show_details(id):
    session['detail_product_id'] = id
    return redirect(url_for("detail_product"))

@app.route('/details', methods=['get', 'post'])
def detail_product():
    id = session['detail_product_id']
    details = db.query(Product).filter(Product.id == id).first()
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("detail-product.html", login=True, admin=True, data=data, item=details)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("detail-product.html", login=True, admin=False, data=data, item=details, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("detail-product.html", login=False, admin=False, data=data, item=details)

@app.route('/collection', methods=['get', 'post'])
def collection_page():
    value = session['collection']
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("collection-page2.html", login=True, admin=True, data=data, collection=value)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("collection-page2.html", login=True, admin=False, data=data, collection=value, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("collection-page2.html", login=False, admin=False, data=data, collection=value)

@app.route('/add-category', methods=['get','post'])
def add_category():
    if request.method == 'POST':
        n = request.form.get("nm")
        m = request.form.get("name")
        uploaded_file = request.files['img']
        subcat = db.query(SubCategory).filter(SubCategory.name == m).first()
        if subcat != None:
            return render_template("error1.html", Message="Sub Category already exist....")
        cat = db.query(Category).filter(Category.name == n).first()
        uploaded_file.filename = m
        current_directory = "static/assets/img/" + n + "/"
        uploaded_file.save(os.path.join(current_directory, uploaded_file.filename))
        p = current_directory + uploaded_file.filename
        obj = SubCategory(m, p, cat)
        db.add(obj)
        db.commit()
        refresh()  # Refreshing Data from database
        # Creating respective folder
        current_directory = os.getcwd() + "\static\\assets\img"
        final_directory = os.path.join(current_directory, m)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
    return redirect(url_for("admin_panel"))

@app.route('/admin/<value>', methods=['get','post'])
def delete_category(value):
    db.query(SubCategory).filter(SubCategory.name == value).delete()
    db.commit
    # Removing respective folder
    current_directory = os.getcwd() + "\static\\assets\img"
    final_directory = os.path.join(current_directory, value)
    if os.path.exists(final_directory):
        os.rmdir(final_directory)
    refresh()  # Refreshing Data from database
    return redirect(url_for("admin_panel"))

@app.route('/admin1/<value>', methods=['get','post'])
def view_category(value):
    session['sub_category_name'] = value
    return redirect(url_for("view_product"))

@app.route('/view-products.html', methods=['get', 'post'])
def view_product():
    value = session['sub_category_name']
    sub_category = updated_sub_category_list(value)
    return render_template("view-product.html", login=True, admin=True, data=data, sub_cat_name=value, items=sub_category)

@app.route('/update-product', methods=['get', 'post'])
def update_product():
    if request.method == 'POST':
        id1 = request.form.get("nm")
        prod = db.query(Product).filter(Product.id == id1).first()
        n = request.form.get("sub")
        prod.name = request.form.get("name")
        prod.price = request.form.get("price")
        prod.detail = request.form.get("detail")
        prod.brand = request.form.get("brand")
        prod.stock = request.form.get("stock")
        prod.discount = request.form.get("discount")
        db.commit()
        session['sub_category_name'] = n
    return redirect(url_for("view_product"))

@app.route('/add-product', methods=['get', 'post'])
def add_product():
    if request.method == 'POST':
        n = request.form.get("nm")
        name = request.form.get("name")
        price = request.form.get("price")
        detail = request.form.get("detail")
        brand = request.form.get("brand")
        stock = request.form.get("stock")
        discount = request.form.get("discount")
        uploaded_file = request.files['img']
        subcat = db.query(SubCategory).filter(SubCategory.name == n).first()
        prod = db.query(Product).filter((Product.name == name) & (Product.brand == brand)).first()
        if prod != None:
            return render_template("error1.html", Message="Product already exist....")
        number = subcat.number + 1
        subcat.number = number
        uploaded_file.filename = str(number) + ".jpeg"
        current_directory = "static/assets/img/" + n + "/"
        uploaded_file.save(os.path.join(current_directory, uploaded_file.filename))
        p = current_directory + uploaded_file.filename
        obj = Product(price, discount, stock, brand, name, p, subcat, detail)
        db.add(obj)
        db.commit()
        session['sub_category_name'] = n
    return redirect(url_for("view_product"))

@app.route('/admin/<id>/<sub_cat_name>', methods=['get','post'])
def delete_product(id,sub_cat_name):
    db.query(Product).filter(Product.id == id).delete()
    db.commit
    session['sub_category_name'] = sub_cat_name
    return redirect(url_for("view_product"))

@app.route('/admin-panel.html', methods=['get', 'post'])
def admin_panel():
    refresh()
    return render_template("admin-panel.html", login=True, admin=True, data=data)


@app.route('/', methods=['post','get'])
def main():
    return redirect('index.html')

@app.route('/index.html', methods=['post','get'])
def home():
    refresh()  # Refreshing Data from database
    new_arrive = new_arrival()
    wish = []
    cart = []
    cart_total = 0
    if 'username' in session:
        if(session['username'] == adminUsername):
            return render_template("index.html", log=True, admin=True, data=data, new=new_arrive, wish=wish, cart=cart, cart_total=cart_total)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("index.html", log=True, admin=False, data=data, new=new_arrive, wish=wish, cart=cart, cart_total=cart_total)
    return render_template("index.html", log=False, admin=False, data=data, new=new_arrive, wish=wish, cart=cart, cart_total=cart_total)

# --------------------------------------------------------------------------------

@app.route('/about', methods=['get', 'post'])
def about():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("about.html", login=True, admin=True, data=data)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("about.html", login=True, admin=False, data=data, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("about.html", login=False, admin=False, data=data)

@app.route('/blog-details', methods=['get', 'post'])
def blog_details():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("blog-details.html", login=True, admin=True, data=data)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("blog-details.html", login=True, admin=False, data=data, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("blog-details.html", login=False, admin=False, data=data)

@app.route('/blogs', methods=['get', 'post'])
def blog_list():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("blog-list.html", login=True, admin=True, data=data)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("blog-list.html", login=True, admin=False, data=data, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("blog-list.html", login=False, admin=False, data=data)

@app.route('/contact', methods=['get', 'post'])
def contact():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("contact.html", login=True, admin=True, data=data)
        else:
            cart, wish, cart_total = return_wishlist_and_cart()
            return render_template("contact.html", login=True, admin=False, data=data, wish=wish, cart=cart,
                               cart_total=cart_total)
    else:
        return render_template("contact.html", login=False, admin=False, data=data)

@app.route('/error1.html', methods=['get', 'post'])
def error():
    return render_template("error1.html", Message="")

@app.route('/login', methods=['post'])
def login():
    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        dono = db.query(User).filter(User.username == name).first()
        if dono == None:  # if username doesn't exist
            return render_template('error1.html', Message="Username doesn't exist. Signup first...")
        if(dono.password != password):
            return render_template('error1.html', Message="Wrong password...")
        session['username'] = name
        return redirect('index.html')

@app.route('/register', methods=['post'])
def register():
    if request.method == 'POST':
        name = request.form.get("username1")
        email = request.form.get("email1")
        password = request.form.get("password1")
        dono = db.query(User).filter(or_(User.username == name,User.email == email)).first()
        if dono != None:  # if username already exists
            return render_template('error1.html', Message="User already exists...")
        d = User(name, email, password)
        db.add(d)
        db.commit()
        session['username'] = name
        return redirect('index.html')

@app.route('/logout.html', methods=['post', 'get'])
def logout():
    session.pop('username',None)
    return render_template("logout.html")

@app.route('/myaccount.html', methods=['get', 'post'])
def myaccount():
    cart, wish, cart_total = return_wishlist_and_cart()
    user = db.query(User).filter(User.username == session['username']).first()
    order1 = db.query(Order).filter(Order.use == user).all()
    return render_template('myaccount.html', login=True, admin=False, data=data, wish=wish, cart=cart,
                               cart_total=cart_total, password=user.password, orders=order1)

@app.route('/change_password', methods=['get', 'post'])
def change_password():
    if request.method == 'POST':
        password = request.form.get('new_password')
        password1 = request.form.get('confirm_password')
        if(password != password1):
            return render_template("error1.html", Message="Passwords don't match...")
        user = db.query(User).filter(User.username == session['username']).first()
        user.password = password
        db.commit()
    return redirect(request.referrer)


@app.route('/email', methods=['get', 'post'])
def email():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        mail_content = ("Name: " + name + "\nEmail: " + email +"\nMessage: " + message)

        sender_address = 'fumar3542@gmail.com'
        sender_pass = 'pcjbqvrpdxkougpq'
        receiver_address = 'fumar3542@gmail.com'
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        try:
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            # session.quit()
            msg = "Your response has been submitted.."
            print("Message sent")
            return render_template("error1.html", Message=msg)
        except Exception as x:
            return render_template("error1.html", Message="Something wrong happened....")

refresh()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
