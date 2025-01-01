from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the modelx``
model_path = r"C:\Users\cuted\OneDrive\Desktop\gem\experiments\model.joblib"
try:
    model = joblib.load(model_path)
    print(f"Model loaded successfully: {type(model)}")
except FileNotFoundError:
    raise FileNotFoundError(f"Ensure {model_path} exists in the working directory.")
except Exception as e:
    raise Exception(f"Error loading model: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve form data
        sale_id = request.form['sale_id']
        city = request.form['city']
        customer_type = request.form['customer_type']
        gender = request.form['gender']
        product_name = request.form['product_name']
        product_category = request.form['product_category']
        unit_price = float(request.form['unit_price'])
        tax = float(request.form['tax'])

        # Prepare input data for prediction
        input_data = pd.DataFrame([[sale_id, city, customer_type, gender, product_name, product_category, unit_price, tax]],
                                  columns=['sale_id', 'city', 'customer_type', 'gender', 'product_name', 'product_category', 'unit_price', 'tax'])
        
        # Make prediction
        prediction = model.predict(input_data)

        return render_template('result.html', prediction_text=f"Predicted Price: ${prediction[0]:.2f}")

    except ValueError as ve:
        return render_template('result.html', prediction_text=f"Error: {ve}")
    except Exception as e:
        return render_template('result.html', prediction_text=f"Error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)
