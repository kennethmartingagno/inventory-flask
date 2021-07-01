from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MMCAXcUQxV'

@app.route("/")
def orders():
    conn = sqlite3.connect("storage.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Coffee")
    data_coffee = cur.fetchall()
    cur.execute("SELECT * FROM Sales")
    data_sales = cur.fetchall()
    return render_template("orders.html", coffees=data_coffee, sales=data_sales)

@app.route("/add-order", methods=['POST'])
def add_order():
    if request.method == 'POST':
        size = request.form['size']
        type = request.form['type']
        quantity = int(request.form['quantity'])

        with sqlite3.connect("storage.db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Coffee (size, type, quantity) VALUES (?,?,?)", (size, type, quantity))
            cur.execute("INSERT INTO Sales (transaction_datetime) VALUES (DATETIME())")
            cur.execute("""
            UPDATE Inventory
            SET quantity=quantity-?
            WHERE size=? AND type=?
            """, (quantity, size, type))
            conn.commit()
            return redirect(url_for("orders"))

@app.route("/add-inventory", methods=['POST'])
def add_inventory():
    if request.method == 'POST':
        size = request.form['size']
        type = request.form['type']
        quantity = request.form['quantity']

        with sqlite3.connect("storage.db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Inventory(size, type, quantity) VALUES (?,?,?)", (size, type, quantity))
            conn.commit()
            return redirect(url_for("inventory"))

@app.route("/inventory")
def inventory():
    conn = sqlite3.connect("storage.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Inventory")
    data = cur.fetchall()
    return render_template("inventory.html", items=data)

@app.route("/edit-inventory/<id>", methods=['POST', 'GET'])
def edit_inventory(id):
    conn = sqlite3.connect("storage.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Inventory WHERE id=?", (id,))
    data = cur.fetchall()
    cur.close()
    return render_template("edit.html", item=data[0])

@app.route("/update-inventory/<id>", methods=['POST'])
def update_inventory(id):
    if request.method == 'POST':
        size = request.form['size']
        type = request.form['type']
        quantity = request.form['quantity']

        with sqlite3.connect("storage.db") as conn:
            cur = conn.cursor()
            cur.execute("""
            UPDATE Inventory
            SET size=?,
                type=?,
                quantity=?
            WHERE id=?
            """, (size, type, quantity, id))
            conn.commit()
            return redirect(url_for("inventory"))

@app.route("/delete-inventory/<string:id>", methods=['POST', 'GET'])
def delete_inventory(id):
    conn = sqlite3.connect("storage.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM Inventory WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("inventory"))

if __name__ == "__main__":
    app.run(debug=True)