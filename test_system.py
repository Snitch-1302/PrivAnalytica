#!/usr/bin/env python3
"""
Test script for the Encrypted Analytics-as-a-Service system
"""

import requests
import json
import time
import sys
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend health check passed: {data}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not reachable: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    endpoints = [
        ("/", "Root endpoint"),
        ("/compute/operations", "Compute operations list"),
        ("/model/info", "Model information"),
        ("/logs/stats", "Logs statistics")
    ]
    
    results = []
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                results.append(True)
            else:
                print(f"❌ {description}: Failed ({response.status_code})")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Error - {e}")
            results.append(False)
    
    return all(results)

def test_computation_endpoints():
    """Test computation endpoints with mock data"""
    mock_data = {
        "encrypted_vectors": ["mock_encrypted_1", "mock_encrypted_2", "mock_encrypted_3"],
        "public_key": "mock_public_key",
        "metadata": {"test": True}
    }
    
    operations = ["average", "sum", "variance", "count"]
    results = []
    
    for operation in operations:
        try:
            response = requests.post(
                f"{BACKEND_URL}/compute/{operation}",
                json=mock_data,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {operation} computation: OK")
                results.append(True)
            else:
                print(f"❌ {operation} computation: Failed ({response.status_code})")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {operation} computation: Error - {e}")
            results.append(False)
    
    return all(results)

def test_ml_endpoints():
    """Test ML prediction endpoints"""
    mock_features = {
        "encrypted_features": ["mock_feature_1", "mock_feature_2", "mock_feature_3"],
        "public_key": "mock_public_key",
        "model_type": "logistic_regression",
        "metadata": {"test": True}
    }
    
    models = ["logistic_regression", "linear_regression"]
    results = []
    
    for model in models:
        try:
            mock_features["model_type"] = model
            response = requests.post(
                f"{BACKEND_URL}/model/predict/{model}",
                json=mock_features,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {model} prediction: OK")
                results.append(True)
            else:
                print(f"❌ {model} prediction: Failed ({response.status_code})")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {model} prediction: Error - {e}")
            results.append(False)
    
    return all(results)

def main():
    """Run all tests"""
    print("🧪 Testing Encrypted Analytics-as-a-Service System")
    print("=" * 50)
    
    # Test backend health
    print("\n1. Testing Backend Health...")
    if not test_backend_health():
        print("❌ Backend is not running. Please start it with: python start_backend.py")
        sys.exit(1)
    
    # Test API endpoints
    print("\n2. Testing API Endpoints...")
    if not test_api_endpoints():
        print("❌ Some API endpoints failed")
        sys.exit(1)
    
    # Test computation endpoints
    print("\n3. Testing Computation Endpoints...")
    if not test_computation_endpoints():
        print("❌ Some computation endpoints failed")
        sys.exit(1)
    
    # Test ML endpoints
    print("\n4. Testing ML Prediction Endpoints...")
    if not test_ml_endpoints():
        print("❌ Some ML endpoints failed")
        sys.exit(1)
    
    print("\n🎉 All tests passed! The system is working correctly.")
    print("\n📋 Next steps:")
    print("1. Start the frontend: python start_frontend.py")
    print("2. Open http://localhost:3000 in your browser")
    print("3. Upload a file and test the analysis features")

if __name__ == "__main__":
    main()
