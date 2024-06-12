from car_repair_shop_project import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=80, host='0.0.0.0')
