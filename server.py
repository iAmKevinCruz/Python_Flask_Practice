import json
from flask import Flask, render_template, abort, request
from mock_data import mock_data
from flask_cors import CORS
from config import db, parse_json

app = Flask(__name__)
CORS(app)

# put dict here
me = {
    "name": "Kevin",
    "last": "Cruz",
    "email": "test@gmail.com",
    "age": 28,
    "hobbies": [],
    "address": {
        "street": "main",
        "number": 42
    }
}


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return f"{me['name']} {me['last']} {'Age: '} {me['age']}"


@app.route("/about/email")
def email():
    return f"{me['email']}"


@app.route("/about/address")
def address():
    address = me["address"]
    print(type(address))
    return f"{address['number']} {address['street']}"


# API Methods

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    # read products from database and run it
    cursor = db.products.find({})  # get all records/documents
    catalog = []
    for prod in cursor:
        # print(prod)
        catalog.append(prod)

    return parse_json(catalog)
    # return json.dumps(catalog)

    # No longer used due to DB usage
    # print(request.headers)
    # return json.dumps(mock_data)


@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()

    if not "price" in product or product["price"] <= 0:
        abort(400, "Price is required and should be greater than 0")

    if not "title" in product or len(product["title"]) < 5:
        abort(400, "Title is required and must be at least 5 characters long")

    # mock_data.append(product)
    # product["_id"] = len(product["title"])
    # return json.dumps(product)
    # return json.dumps(mock_data)

    # save product into the DB
    # MongoDB add a _id with a uniqe value
    db.products.insert_one(product)
    return parse_json(product)


@app.route("/api/categories")
def get_categories():
    # categories = []
    # for product in mock_data:
    #     category = product["category"]
    #     if category not in categories:
    #         categories.append(category)
    # return json.dumps(categories)

    # return a list with the uniqe categories [string, string]
    cursor = db.products.find({})
    categories = []
    for cat in cursor:
        if cat['category'] not in categories:
            categories.append(cat['category'])
    return parse_json(categories)



@app.route("/api/product/<id>")
def get_by_id(id):
    # found = False
    # for product in mock_data:
    #     if product["_id"] == id:
    #         found = True
    #         return json.dumps(product)
    # if not found:
    #     abort(404)

    product = db.products.find_one({"_id" : id})
    if not product:
        abort(404)

    return parse_json(product)


@app.route("/api/catalog/<cat>")
def get_by_category(cat):
    # found = False
    # categories = []
    # for product in mock_data:
    #     if product["category"].lower() == cat.lower():
    #         found = True
    #         categories.append(product)
    # return json.dumps(categories)

    cursor = db.products.find({"category" : cat.lower()})
    products = []
    for prod in cursor:
        products.append(prod)
        
    return parse_json(products)




@app.route("/api/product/cheapest")
def get_cheapest():
    # cheap = mock_data[0]
    # for product in mock_data:
    #     if product["price"] < cheap["price"]:
    #         cheap = product
    # print(cheap)
    # return json.dumps(cheap)

    cursor = db.products.find()
    cheap = cursor[0]
    for prod in cursor:
        if prod["price"] < cheap["price"]:
            cheap = prod

    return parse_json(cheap)


"""
if "blah" not in somestring: 
    continue
"""


@app.route("/api/test/loadData")
def load_data():

    return "Data Already Loaded"

    # load every product in mock_data into the database
    for prod in mock_data:
        db.products.insert_one(prod)

    return "Data loaded"

@app.route("/api/couponCode", methods=["POST"])
def save_coupon():
    coupon = request.get_json()
    if not "code" in coupon:
        abort(400, "Title is required")

    if not "discount" in coupon or coupon["discount"] <= 0:
        abort(400, "Discount is required and must be more than 0")
    
    db.couponCodes.insert_one(coupon)
    return parse_json(coupon)

@app.route("/api/couponCode")
def get_coupon():
    cursor = db.couponCodes.find({})
    codes = []
    for code in cursor:
        codes.append(code)
    return parse_json(codes)


app.run(debug=True)
