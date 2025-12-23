# ==========================================================
# 🚗 REAL-TIME VEHICLE TRACKING SYSTEM (COLLEGE POC VERSION)
# ==========================================================

from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import random
import warnings

# ----------------------------------------------------------
# ⚙️ 1. INITIAL SETUP
# ----------------------------------------------------------
app = Flask(__name__)
CORS(app)
warnings.filterwarnings("ignore", category=UserWarning)

# ----------------------------------------------------------
# 📂 2. LOAD DATASET (GeoLife or Your Own CSV)
# ----------------------------------------------------------
df = pd.read_csv("1_Raw_Dataset.csv")[['latitude', 'longitude', 'date', 'time']]
df = df.reset_index(drop=True)

# ----------------------------------------------------------
# 🧠 3. LOAD TRAINED ML MODELS
# ----------------------------------------------------------
model_lr = joblib.load("trained_models/linear_regression_model.pkl")     # 6 features
model_dt = joblib.load("trained_models/decision_tree_model.pkl")         # 8 features
model_rf = joblib.load("trained_models/random_forest_model.pkl")         # 9 features

# ----------------------------------------------------------
# 🚘 4. API ENDPOINT - FAST PREDICTION MODE (for College Demo)
# ----------------------------------------------------------
@app.route('/api/vehicle', methods=['GET'])
def get_vehicle_data():
    # Take only 20 random records for faster, smoother response
    sample_df = df.sample(10).reset_index(drop=True)
    data_points = []

    for i in range(len(sample_df)):
        row = sample_df.iloc[i]
        lat, lon = row['latitude'], row['longitude']

        # Simulated driving inputs (these act as features)
        speed_kmh = np.random.uniform(30, 80)
        distance_travelled = np.random.uniform(1, 15)
        remaining_km = np.random.uniform(1, 30)
        traffic = np.random.uniform(0.8, 1.3)
        driver_aggr = np.random.uniform(0.9, 1.1)
        road_factor = random.choice([0.95, 1.0, 1.05])
        altitude = np.random.uniform(200, 500)  # extra feature for RF

        # Input for each model (based on its training features)
        X_lr = [[speed_kmh, distance_travelled, remaining_km, traffic, driver_aggr, road_factor]]               # 6 features
        X_dt = [[speed_kmh, distance_travelled, remaining_km, traffic, driver_aggr, road_factor, lat, lon]]     # 8 features
        X_rf = [[speed_kmh, distance_travelled, remaining_km, traffic, driver_aggr, road_factor, lat, lon, altitude]]  # 9 features

        # Predict ETA using 3 models
        eta_lr = model_lr.predict(X_lr)[0]
        eta_dt = model_dt.predict(X_dt)[0]
        eta_rf = model_rf.predict(X_rf)[0]

        # Average ETA for better accuracy
        avg_eta = round((eta_lr + eta_dt + eta_rf) / 3, 2)

        # Prepare response data
        data_points.append({
            'latitude': lat,
            'longitude': lon,
            'speed': round(speed_kmh, 2),
            'eta': avg_eta,
            'timestamp': f"{row['date']} {row['time']}"
        })

    print(f"✅ Sent {len(data_points)} points to frontend.")
    return jsonify(data_points)


# ----------------------------------------------------------
# 🛰️ 5. OPTIONAL - STREAMING MODE (for Live Demo)
# ----------------------------------------------------------
from flask import Response, json
import time

@app.route('/api/vehicle-stream', methods=['GET'])
def stream_vehicle_data():
    """Stream one vehicle coordinate per second (real-time demo)."""
    def generate():
        for i in range(len(df)):
            row = df.iloc[i]
            lat, lon = row['latitude'], row['longitude']
            speed = np.random.uniform(30, 80)
            eta = np.random.uniform(5, 20)
            payload = {'latitude': lat, 'longitude': lon, 'speed': speed, 'eta': eta}
            yield f"data:{json.dumps(payload)}\n\n"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')


# ----------------------------------------------------------
# 🚀 6. RUN FLASK SERVER
# ----------------------------------------------------------
if __name__ == '__main__':
    print("🔥 Real-Time Vehicle Tracking System Backend is Running...")
    print("➡️  Access API at: http://127.0.0.1:5000/api/vehicle")
    print("➡️  Or live stream at: http://127.0.0.1:5000/api/vehicle-stream")
    app.run(debug=True)
