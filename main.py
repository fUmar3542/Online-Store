from Base import Session, engine, Base
from flask import Flask, session, render_template, render_template, make_response, request, url_for, redirect

app = Flask(__name__)

Base.metadata.create_all(engine)
session = Session()

@app.route('/', methods=['post','get'])
def main():
    return render_template("index.html")

@app.route('/index.html', methods=['post','get'])
def home():
    return render_template("index.html")

@app.route('/about.html', methods=['get'])
def about():
    return render_template("about.html")

@app.route('/blog-details.html', methods=['get'])
def blog_details():
    return render_template("blog-details.html")

@app.route('/blog-list.html', methods=['get'])
def blog_list():
    return render_template("blog-list.html")

@app.route('/cart-list.html', methods=['get'])
def cart_list():
    return render_template("cart-list.html")

@app.route('/categories-page1.html', methods=['get'])
def categories_page1():
    return render_template("categories-page1.html")

@app.route('/categories-page2.html', methods=['get'])
def categories_page2():
    return render_template("categories-page2.html")

@app.route('/categories-page4.html', methods=['get'])
def categories_page4():
    return render_template("categories-page4.html")

@app.route('/checkout.html', methods=['get'])
def checkout():
    return render_template("checkout.html")

@app.route('/collection-page1.html', methods=['get'])
def collection_page1():
    return render_template("collection-page1.html")

@app.route('/collection-page2.html', methods=['get'])
def collection_page2():
    return render_template("collection-page2.html")

@app.route('/contact.html', methods=['get'])
def contact():
    return render_template("contact.html")

@app.route('/error1.html', methods=['get'])
def error():
    return render_template("error1.html")

@app.route('/faq.html', methods=['get'])
def faq():
    return render_template("faq.html")

@app.route('/logout.html', methods=['get'])
def logout():
    return render_template("logout.html")

@app.route('/myaccount.html', methods=['get'])
def myaccount():
    return render_template("myaccount.html")

@app.route('/search-result.html', methods=['get'])
def search_result():
    return render_template("search-result.html")

@app.route('/wish-list.html', methods=['get'])
def wish_list():
    return render_template("wish-list.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
