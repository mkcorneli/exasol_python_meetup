#!/usr/bin/env python3
"""
Simple Flight Delay Prediction with Exasol
==========================================
Minimal version - just the essentials.
"""

import pyexasol
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import pickle

class SimpleFlightPredictor:
    def __init__(self, dsn, user, password):
        self.conn = pyexasol.connect(dsn=dsn, user=user, password=password, schema='FLIGHTS')
        self.model = None
        self.encoders = {}
        print("✅ Connected to Exasol")
    
    def get_data(self, limit=10000):
        """Get flight data from Exasol."""
        query = f"""
        SELECT 
            "OP_CARRIER",
            "ORIGIN", 
            "DEST",
            "DAY_OF_WEEK",
            "MONTH",
            "CRS_DEP_TIME",
            "DEP_DEL15"
        FROM "FLIGHTS"."FLIGHTS"
        WHERE "CANCELLED" = 0 
            AND "DEP_DEL15" IS NOT NULL
        LIMIT {limit}
        """
        
        df = self.conn.export_to_pandas(query)
        print(f"📥 Loaded {len(df)} flights")
        return df
    
    def prepare_data(self, df):
        """Create features and target."""
        # Create hour feature
        df['HOUR'] = (df['CRS_DEP_TIME'].astype(str).str.zfill(4).str[:2]).astype(int)
        
        # Encode categoricals
        for col in ['OP_CARRIER', 'ORIGIN', 'DEST']:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
            df[f'{col}_ENCODED'] = self.encoders[col].fit_transform(df[col])
        
        # Select features (no distance)
        features = ['DAY_OF_WEEK', 'MONTH', 'HOUR',
                   'OP_CARRIER_ENCODED', 'ORIGIN_ENCODED', 'DEST_ENCODED']
        
        X = df[features]
        y = df['DEP_DEL15']
        
        print(f"🔧 Features: {X.shape}, Target: {y.shape}")
        return X, y
    
    def train(self, X, y):
        """Train the model."""
        # Simple 80/20 split
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Test
        y_pred = self.model.predict(X_test)
        accuracy = (y_pred == y_test).mean()
        
        print(f"🎯 Accuracy: {accuracy:.1%}")
        print("\n📊 Classification Report:")
        print(classification_report(y_test, y_pred))
    
    def save_model(self, filename='simple_flight_model.pkl'):
        """Save model and encoders."""
        with open(filename, 'wb') as f:
            pickle.dump({'model': self.model, 'encoders': self.encoders}, f)
        print(f"💾 Model saved to {filename}")
    
    def predict(self, carrier, origin, dest, day_of_week, month, hour):
        """Make a prediction."""
        # Encode inputs
        data = {
            'DAY_OF_WEEK': day_of_week,
            'MONTH': month,
            'HOUR': hour,
            'OP_CARRIER_ENCODED': self.encoders['OP_CARRIER'].transform([carrier])[0],
            'ORIGIN_ENCODED': self.encoders['ORIGIN'].transform([origin])[0],
            'DEST_ENCODED': self.encoders['DEST'].transform([dest])[0]
        }
        
        features = [[data[f] for f in ['DAY_OF_WEEK', 'MONTH', 'HOUR',
                                      'OP_CARRIER_ENCODED', 'ORIGIN_ENCODED', 'DEST_ENCODED']]]
        
        prob = self.model.predict_proba(features)[0][1]
        return f"Delay probability: {prob:.1%}"

def main():
    # Database config - UPDATE THESE WITH YOUR CREDENTIALS
    # For Exasol SaaS, use: 'your-cluster.clusters.exasol.com:8563'
    # For on-premise, use: 'your-cluster.exacloud.com:8563'
    config = {
        'dsn': 'your-cluster.clusters.exasol.com:8563',  # SaaS format
        'user': 'your-username',
        'password': 'your-password'
    }
    
    # Run pipeline
    predictor = SimpleFlightPredictor(**config)
    
    # Get data and train
    df = predictor.get_data(limit=20000)
    X, y = predictor.prepare_data(df)
    predictor.train(X, y)
    predictor.save_model()
    
    # Example prediction
    print("\n🔮 Example prediction:")
    result = predictor.predict(
        carrier='AA', 
        origin='LAX', 
        dest='JFK', 
        day_of_week=2, 
        month=7, 
        hour=15
    )
    print(result)
    
    print("\n🎉 Done!")

if __name__ == "__main__":
    main()