
from flask import  Flask,request, jsonify 
from datetime import datetime
import uuid
import re
import math

app = Flask(__name__)
receipts_data = {}

@app.route('/receipts/process', methods=['POST'])
def ProcessReceipts():
    receipt = request.get_json()
    if  is_valid_receipt(receipt):
        receipt_id = generate_receipt_id()
        points = calculate_points(receipt)
        receipts_data[receipt_id] = points
        return jsonify({"id": receipt_id})
    else:
        return jsonify({"error": "The receipt is invalid"}), 400
    

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = receipts_data.get(receipt_id)
    if points is not None:
        return jsonify({"points": points})
    else:
        return jsonify({"error": "No receipt found for that id"}), 404   


def generate_receipt_id():
    return str(uuid.uuid4())

def calculate_points(receipt):
    points = 0

    # Rule 1
    retailer_name = receipt["retailer"]
    points += sum(1 for char in retailer_name if char.isalnum())

    # Rule 2
    total = float(receipt["total"])
    if total.is_integer():
        points += 50

    # Rule 3
    if total % 0.25 == 0:
        points += 25

    # Rule 4
    items = receipt["items"]
    points += (len(items) // 2) * 5

    # Rule 5
    for item in items:
        description = item["shortDescription"].strip()
        if len(description) % 3 == 0:
            item_price = float(item["price"])
            points += math.ceil(item_price * 0.2) 

    # Rule 6
    purchase_date = receipt["purchaseDate"]
    try:
        day = int(datetime.strptime(purchase_date, "%Y-%m-%d").day)
        if day % 2 == 1:
            points += 6
    except ValueError:
        pass

    # Rule 7: 10 points if the purchase time is between 2:00pm and 4:00pm
    purchase_time = receipt.get("purchaseTime", "")
    try:
        purchase_time_obj = datetime.strptime(purchase_time, "%H:%M")
        if purchase_time_obj.hour == 14 or (purchase_time_obj.hour == 15 and purchase_time_obj.minute == 0):
            points += 10
    except ValueError:
        pass

    return points



def is_valid_receipt(receipt):
    if not isinstance(receipt, dict):
        return False

    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    for field in required_fields:
        if field not in receipt:
            return False

    if not isinstance(receipt["retailer"], str) or not re.match(r"^[\w\s\-&]+$", receipt["retailer"]):
        return False
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", receipt["purchaseDate"]):
        return False
    if not re.match(r"^\d{2}:\d{2}$", receipt["purchaseTime"]):
        return False
    if not re.match(r"^\d+\.\d{2}$", receipt["total"]):
        return False

    if not isinstance(receipt["items"], list) or len(receipt["items"]) < 1:
        return False
    for item in receipt["items"]:
        if not isinstance(item, dict):
            return False
        if "shortDescription" not in item or "price" not in item:
            return False
        if not isinstance(item["shortDescription"], str) or not re.match(r"^[\w\s\-]+$", item["shortDescription"]):
            return False
        if not re.match(r"^\d+\.\d{2}$", item["price"]):
            return False

    return True
    

if __name__ == '__main__':
    app.run(debug=True)