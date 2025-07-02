from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Allow cross-origin requests
import util

app = Flask(__name__)
CORS(app)

# ✅ Load model and columns immediately
util.load_saved_artifacts()

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        # ✅ Use .get to safely access form fields
        total_sqft = request.form.get('total_sqft')
        location = request.form.get('location')
        bhk = request.form.get('bhk')
        bath = request.form.get('bath')

        print(f"[DEBUG] Form data: sqft={total_sqft}, location={location}, bhk={bhk}, bath={bath}")

        if not all([total_sqft, location, bhk, bath]):
            raise ValueError("Missing one or more form values.")

        # ✅ Convert values after checking they're present
        total_sqft = float(total_sqft)
        bhk = int(bhk)
        bath = int(bath)

        price = util.get_estimated_price(location, total_sqft, bhk, bath)

        print(f"[DEBUG] Estimated price: {price}")
        return jsonify({'estimated_price': price})

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    app.run()
