from Base import Session, engine, Base
from flask import Flask, session, render_template, make_response, request, url_for, redirect
from Model import User, Order, Category, SubCategory, Product, OrderProduct, Payment

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = "anony"

Base.metadata.create_all(engine)
db = Session()

@app.route('/', methods=['post','get'])
def main():
    return redirect('index.html')

@app.route('/index.html', methods=['post','get'])
def home():
    if 'username' in session:
        return render_template("index.html", log=True)
    return render_template("index.html", log=False)

@app.route('/about.html', methods=['get', 'post'])
def about():
    if 'username' in session:
        return render_template("about.html", login=True)
    else:
        return render_template("about.html", login=False)

@app.route('/blog-details.html', methods=['get'])
def blog_details():
    if 'username' in session:
        return render_template("blog-details.html", login=True)
    else:
        return render_template("blog-details.html", login=False)

@app.route('/blog-list.html', methods=['get'])
def blog_list():
    if 'username' in session:
        return render_template("blog-list.html", login=True)
    else:
        return render_template("blog-list.html", login=False)

@app.route('/cart-list.html', methods=['get'])
def cart_list():
    if 'username' in session:
        return render_template("cart-list.html", login=True)
    else:
        return render_template("cart-list.html", login=False)

@app.route('/categories-page1.html', methods=['get'])
def categories_page1():
    if 'username' in session:
        return render_template("categories-page1.html", login=True)
    else:
        return render_template("categories-page1.html", login=False)

@app.route('/categories-page2.html', methods=['get'])
def categories_page2():
    if 'username' in session:
        return render_template("categories-page2.html", login=True)
    else:
        return render_template("categories-page2.html", login=False)

@app.route('/categories-page4.html', methods=['get'])
def categories_page4():
    if 'username' in session:
        return render_template("categories-page4.html", login=True)
    else:
        return render_template("categories-page4.html", login=False)

@app.route('/checkout.html', methods=['get'])
def checkout():
    if 'username' in session:
        return render_template("checkout.html", login=True)
    else:
        return render_template("checkout.html", login=False)

@app.route('/collection-page1.html', methods=['get'])
def collection_page1():
    if 'username' in session:
        return render_template("collection-page1.html", login=True)
    else:
        return render_template("collection-page1.html", login=False)

@app.route('/collection-page2.html', methods=['get'])
def collection_page2():
    if 'username' in session:
        return render_template("collection-page2.html", login=True)
    else:
        return render_template("collection-page2.html", login=False)

@app.route('/contact.html', methods=['get'])
def contact():
    if 'username' in session:
        return render_template("contact.html", login=True)
    else:
        return render_template("contact.html", login=False)

@app.route('/error1.html', methods=['get'])
def error():
    return render_template("error1.html")

@app.route('/faq.html', methods=['get'])
def faq():
    if 'username' in session:
        return render_template("faq.html", login=True)
    else:
        return render_template("faq.html", login=False)

@app.route('/login', methods=['post'])
def login():
    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        if (name == "" or password == ""):
            return redirect('error1.html')
        dono = db.query(User).filter(User.username == name).first()
        if dono == None:  # if username doesn't exist
            return redirect('error1.html')
        session['username'] = name
        return redirect('index.html')

@app.route('/register', methods=['post'])
def register():
    if request.method == 'POST':
        name = request.form.get("username1")
        email = request.form.get("email1")
        password = request.form.get("password1")
        if (name == "" or email == "" or password == ""):
            return redirect('error1.html')
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

@app.route('/myaccount.html', methods=['get'])
def myaccount():
    if 'username' in session:
        return render_template("myaccount.html", login=True)
    else:
        return render_template("myaccount.html", login=False)

@app.route('/search-result.html', methods=['get'])
def search_result():
    if 'username' in session:
        return render_template("search-result.html", login=True)
    else:
        return render_template("search-result.html", login=False)

@app.route('/wish-list.html', methods=['get'])
def wish_list():
    if 'username' in session:
        return render_template("wish-list.html", login=True)
    else:
        return render_template("wish-list.html", login=False)

@app.route('/admin-panel.html', methods=['get', 'post'])
def admin_panel():
    return render_template("admin-panel.html")

@app.route('/view-products.html', methods=['get', 'post'])
def view_product():
    return render_template("view-product.html")

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

def checkCredentials(self):
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
