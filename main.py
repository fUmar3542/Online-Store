import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Base import Session, engine, Base
from flask import Flask, session, render_template, make_response, request, url_for, redirect
from Model import User, Order, Category, SubCategory, Product, OrderProduct, Payment
from pathlib import Path
import os

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = "anony"

Base.metadata.create_all(engine)
db = Session()

adminUsername = 'Umar'
data = []

@app.route('/add-category', methods=['get','post'])
def add_category():
    if request.method == 'POST':
        n = request.form.get("nm")
        m = request.form.get("name")
        subcat = db.query(SubCategory).filter(SubCategory.name == m).first()
        if subcat != None:
            return render_template("error1.html", Message="Sub Category already exist....")
        cat = db.query(Category).filter(Category.name == n).first()
        obj = SubCategory(m,cat)
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
    return render_template("view-product.html", login=True, admin=True, sub_cat_name=value, items=sub_category)

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

# --------------------------------------------------------------------------------

@app.route('/', methods=['post','get'])
def main():
    return redirect('index.html')

@app.route('/index.html', methods=['post','get'])
def home():
    refresh()  # Refreshing Data from database
    if 'username' in session:
        if(session['username'] == adminUsername):
            return render_template("index.html", log=True, admin=True, data=data)
        else:
            return render_template("index.html", log=True, admin=False,data=data)
    return render_template("index.html", log=False, admin=False,data=data)

@app.route('/list-product.html', methods=['get', 'post'])
def list_product():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("list-product.html", log=True, admin=True)
        else:
            return render_template("list-product.html", log=True, admin=False)
    else:
        return render_template("list-product.html", login=False, admin=False)

@app.route('/detail-product.html', methods=['get', 'post'])
def detail_product():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("detail-product.html", log=True, admin=True)
        else:
            return render_template("detail-product.html", log=True, admin=False)
    else:
        return render_template("detail-product.html", login=False, admin=False)

@app.route('/about.html', methods=['get', 'post'])
def about():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("about.html", log=True, admin=True)
        else:
            return render_template("about.html", log=True, admin=False)
    else:
        return render_template("about.html", login=False, admin=False)

@app.route('/blog-details.html', methods=['get', 'post'])
def blog_details():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("blog-details.html", login=True, admin=True)
        else:
            return render_template("blog-details.html", login=True, admin=False)
    else:
        return render_template("blog-details.html", login=False, admin=False)

@app.route('/blog-list.html', methods=['get', 'post'])
def blog_list():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("blog-list.html", login=True, admin=True)
        else:
            return render_template("blog-list.html", login=True, admin=False)
    else:
        return render_template("blog-list.html", login=False, admin=False)

@app.route('/cart-list.html', methods=['get', 'post'])
def cart_list():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("cart-list.html", login=True, admin=True)
        else:
            return render_template("cart-list.html", log=True, admin=False)
    return redirect('/index.html')

@app.route('/add-cart.html', methods=['get', 'post'])
def add_cart():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("add-cart.html", login=True, admin=True)
        else:
            return render_template("add-cart.html", login=True, admin=False)
    return redirect('/index.html')

@app.route('/remove-cart.html', methods=['get', 'post'])
def remove_cart():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("remove-cart.html", login=True, admin=True)
        else:
            return render_template("remove-cart.html", login=True, admin=False)
    return redirect('/index.html')


@app.route('/categories-page1.html', methods=['get', 'post'])
def categories_page1():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("categories-page1.html", login=True, admin=True)
        else:
            return render_template("categories-page1.html", login=True, admin=False)
    else:
        return render_template("categories-page1.html", login=False, admin=False)

@app.route('/categories-page2.html', methods=['get', 'post'])
def categories_page2():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("categories-page2.html", login=True, admin=True)
        else:
            return render_template("categories-page2.html",login=True, admin=False)
    else:
        return render_template("categories-page2.html", login=False, admin=False)

@app.route('/categories-page4.html', methods=['get', 'post'])
def categories_page4():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("categories-page4.html", login=True, admin=True)
        else:
            return render_template("categories-page4.html", login=True, admin=False)
    else:
        return render_template("categories-page4.html", login=False, admin=False)

@app.route('/checkout.html', methods=['get', 'post'])
def checkout():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("checkout.html", login=True, admin=True)
        else:
            return render_template("checkout.html", login=True, admin=False)
    else:
        return render_template("checkout.html", login=False, admin=False)

@app.route('/collection-page1.html', methods=['get', 'post'])
def collection_page1():
    if 'username' in session:
        if(session['username'] == adminUsername):
            return render_template("collection-page1.html", login=True, admin=True)
        else:
            return render_template("collection-page1.html", login=True, admin=False)
    else:
        return render_template("collection-page1.html", login=False, admin=False)

@app.route('/collection-page2.html', methods=['get', 'post'])
def collection_page2():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("collection-page2.html", login=True, admin=True)
        else:
            return render_template("collection-page2.html", login=True, admin=False)
    else:
        return render_template("collection-page2.html", login=False, admin=False)

@app.route('/contact.html', methods=['get', 'post'])
def contact():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("contact.html", login=True, admin=True)
        else:
            return render_template("contact.html", login=True, admin=False)
    else:
        return render_template("contact.html", login=False, admin=False)

@app.route('/error1.html', methods=['get', 'post'])
def error():
    return render_template("error1.html", Message="")

@app.route('/faq.html', methods=['get', 'post'])
def faq():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("faq.html", login=True, admin=True)
        else:
            return render_template("faq.html", login=True, admin=False)
    else:
        return render_template("faq.html", login=False, admin=False)

@app.route('/login', methods=['post'])
def login():
    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        dono = db.query(User).filter(User.username == name).first()
        if dono == None:  # if username doesn't exist
            return render_template('error1.html', Message="Username doesn't exist. Signup first...")
        session['username'] = name
        return redirect('index.html')

@app.route('/register', methods=['post'])
def register():
    if request.method == 'POST':
        name = request.form.get("username1")
        email = request.form.get("email1")
        password = request.form.get("password1")
        dono = db.query(User).filter(User.username == name).first()
        if dono != None:  # if username already exists
            return redirect('error1.html')
        d = User(name, email, password)
        db.add(d)
        db.commit()
        session['username'] = name
        return redirect('index.html')

@app.route('/logout.html', methods=['post', 'get'])
def logout():
    session.clear()
    return render_template("logout.html")

@app.route('/myaccount.html', methods=['get', 'post'])
def myaccount():
    if 'username' in session:
        return render_template("index.html", log=True, admin=False)
    return redirect('/index.html')

@app.route('/search-result.html', methods=['get', 'post'])
def search_result():
    if 'username' in session:
        return render_template("index.html", log=True, admin=False)
    return redirect('/index.html')

@app.route('/wish-list.html', methods=['get', 'post'])
def wish_list():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("index.html", log=True, admin=True)
        else:
            return render_template("index.html", log=True, admin=False)
    return redirect('/index.html')

@app.route('/add-wishlist.html', methods=['get', 'post'])
def add_wishlist():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("index.html", log=True, admin=True)
        else:
            return render_template("index.html", log=True, admin=False)
    return redirect('/index.html')

@app.route('/remove-wishlist.html', methods=['get', 'post'])
def remove_wishlist():
    if 'username' in session:
        if (session['username'] == adminUsername):
            return render_template("index.html", log=True, admin=True)
        else:
            return render_template("index.html", log=True, admin=False)
    return redirect('/index.html')

# @app.route('/add-product.html', methods=['get', 'post'])
# def add_product():
#     return render_template("add-product.html")

# @app.route('/remove-product.html', methods=['get', 'post'])
# def remove_product():
#     return render_template("remove-product.html")

# @app.route('/add-category.html', methods=['get', 'post'])
# def add_category():
#     return render_template("add-category.html")

# @app.route('/remove-category.html', methods=['get', 'post'])
# def remove_category():
#     return render_template("remove-category.html")

@app.route('/search', methods=['get', 'post'])
def search():
    if request.method == 'POST':
        return render_template("faq.html")

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
