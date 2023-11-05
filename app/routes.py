from app import app, db
from app.models import Admin, Drivers, Routes, Input
from flask import request, jsonify, render_template
from flask_login import current_user, login_user, logout_user
from sqlalchemy import text
from joblib import load

mlmodel = load(app.config["ML_MODEL_URI"])


@app.route("/")
def test():
    return {"message": "hello, world"}


@app.route("/test_database_connection")
def test_database_connection():
    try:
        result = db.session.execute(text("SELECT version()"))
        version = result.scalar()
        return (
            jsonify({"message": "Database connection successful", "version": version}),
            200,
        )
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500


@app.route("/test_model_status")
def test_model_status():
    try:
        if mlmodel:
            return jsonify({"status": "Model is loaded and ready for predictions"}), 200
    except Exception as e:
        return jsonify({"status": f"Error loading the model: {str(e)}"}), 500


@app.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({"loggedIn": True, "username": current_user.username}), 200

    username = request.json.get("username")
    password = request.json.get("password")
    remember_me = request.json.get("remember_me")
    user = Admin.query.filter_by(username=username).first()

    if user is None or not user.check_password(password=password):
        return (
            jsonify(
                {"message": "Login failed", "reason": "Invalid username or password"}
            ),
            401,
        )

    login_user(user, remember=remember_me)
    return jsonify({"message": "Login successful"}), 200


@app.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "Logout Successful"}), 200


@app.route("/driver/<int:driver_id>/")
def driver(driver_id):
    try:
        d = Drivers.query.get_or_404(driver_id)
        return jsonify(d.serialize())
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/route/<int:route_id>/")
def route(route_id):
    try:
        r = Routes.query.get_or_404(route_id)
        return jsonify(r.serialize())
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.json
        predictions = predict_accident_probabilities(input_data, mlmodel)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)})


def predict_accident_probabilities(input_data, model):
    predicted_class = model.predict(input_data)
    class_probabilities = model.predict_proba(input_data)
    probability_fatal = class_probabilities[0][0]  # Probability for fatal accident
    probability_serious = class_probabilities[0][1]  # Probability for serious accident
    probability_slight = class_probabilities[0][2]  # Probability for slight accident

    w_fatal = 0.5  # Weight for fatal accidents
    w_serious = 0.4  # Weight for serious accidents
    w_slight = 0.3  # Weight for slight accidents

    combined_probability = (
        w_fatal * probability_fatal
        + w_serious * probability_serious
        + w_slight * probability_slight
    )

    return {
        "Predicted_Class": int(predicted_class[0]),
        "Probability_Fatal": probability_fatal,
        "Probability_Serious": probability_serious,
        "Probability_Slight": probability_slight,
        "Combined_Probability": combined_probability,
    }


"""@app.route('/Input', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_input = Input(
            Latitude=request.form['Latitude'],
            Longitude=request.form['Longitude'],
            Age_Band_of_Driver=request.form['Age_Band_of_Driver'],
            Date=request.form['Date'],
            Time=request.form['Time'],
            Speed_Limit=request.form['Speed_Limit'],
            Light_Conditions=request.form['Light_Conditions'],
            Road_Surface_Conditions=request.form['Road_Surface_Conditions'],
            Junction_Control=request.form['Junction_Control'],
            Sex_of_Driver=request.form['Sex_of_Driver'],
            Road_Type=request.form['Road_Type'],
            Weather_Conditions=request.form['Weather_Conditions'],
            Urban_or_Rural_Area=request.form['Urban_or_Rural_Area'],
            Probability_Fatal=request.form['Probability_Fatal'],
            Probability_Serious=request.form['Probability_Serious'],
            Probability_Slight=request.form['Probability_Slight'],
            Combined_Probability=request.form['Combined_Probability']
        )
        db.session.add(new_input)
        db.session.commit()
        return redirect(url_for('index')) #next page
    inputs = Input.query.all()
    return render_template('index.html', inputs=inputs)"""
