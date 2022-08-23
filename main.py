from Base import Session, engine, Base
from flask import Flask, session, render_template, make_response, request, url_for, redirect
from Model import User, Order, Category, SubCategory, Product, OrderProduct, Payment

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = "anony"

Base.metadata.create_all(engine)
db = Session()

adminUsername = 'Umar'


@app.route('/', methods=['post','get'])
def main():
    return redirect('index.html')

@app.route('/index.html', methods=['post','get'])
def home():
    if 'username' in session:
        if(session['username'] == adminUsername):
            return render_template("index.html", log=True, admin=True)
        else:
            return render_template("index.html", log=True, admin=False)
    return render_template("index.html", log=False, admin=False)

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

@app.route('/admin-panel.html', methods=['get', 'post'])
def admin_panel():
    return render_template("admin-panel.html", login=True, admin=True)

@app.route('/view-products.html', methods=['get', 'post'])
def view_product():
    return render_template("view-product.html", login=True, admin=True)

@app.route('/add-product.html', methods=['get', 'post'])
def add_product():
    return render_template("add-product.html")

@app.route('/remove-product.html', methods=['get', 'post'])
def remove_product():
    return render_template("remove-product.html")

@app.route('/add-category.html', methods=['get', 'post'])
def add_category():
    return render_template("add-category.html")

@app.route('/remove-category.html', methods=['get', 'post'])
def remove_category():
    return render_template("remove-category.html")

@app.route('/search', methods=['get', 'post'])
def search():
    if request.method == 'POST':
        return render_template("faq.html")

@app.route('/email', methods=['get', 'post'])
def email():
    if request.method == 'POST':
        return render_template("error1.html", Message="Your response has been submitted..")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
