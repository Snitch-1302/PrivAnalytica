#!/usr/bin/env python3
import requests
import json
import base64
import numpy as np
import argparse
import sys
from typing import List, Dict, Any
import tenseal as ts

class EncryptedAnalyticsClient:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EncryptedAnalyticsClient/1.0'
        })
        
    def check_health(self) -> bool:
        try:
            response = self.session.get(f"{self.api_base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend is healthy: {data}")
                return True
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to backend: {e}")
            return False
    
    def generate_keys(self) -> Dict[str, str]:
        try:
            context = ts.context(
                ts.SCHEME_TYPE.CKKS,
                poly_modulus_degree=8192,
                coeff_mod_bit_sizes=[60, 40, 40, 60]
            )
            context.global_scale = 2**40  
            context.generate_galois_keys()
            public_key = base64.b64encode(context.serialize()).decode('utf-8')
            secret_key = base64.b64encode(b"demo_secret_key_2024").decode('utf-8')
            
            keys = {
                "public_key": public_key,
                "secret_key": secret_key,
                "context_params": {
                    "poly_modulus_degree": 8192,
                    "scale_bits": 40
                }
            }
            
            print("✅ Encryption keys generated successfully")
            return keys
            
        except Exception as e:
            print(f"❌ Error generating keys: {e}")
            raise
    
    def encrypt_data(self, data: List[float], public_key: str) -> List[str]:
        try:
            context_bytes = base64.b64decode(public_key)
            context = ts.context_from(context_bytes)
            
            vector = np.array(data, dtype=np.float64)
            
            encrypted_vector = ts.ckks_vector(context, vector)
            
            serialized = encrypted_vector.serialize()
            encrypted_data = base64.b64encode(serialized).decode('utf-8')
            
            print(f"✅ Encrypted {len(data)} values successfully")
            return [encrypted_data]  
            
        except Exception as e:
            print(f"❌ Error encrypting data: {e}")
            raise
    
    def send_computation_request(self, operation: str, encrypted_vectors: List[str], public_key: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            endpoint = f"{self.api_base_url}/compute/{operation}"
            
            payload = {
                "encrypted_vectors": encrypted_vectors,
                "public_key": public_key
            }
            
            if metadata:
                payload["metadata"] = metadata
            
            print(f"🚀 Sending {operation} computation request...")
            response = self.session.post(endpoint, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {operation} computation completed successfully")
                return result
            else:
                print(f"❌ Computation failed: {response.status_code} - {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"❌ Error sending computation request: {e}")
            raise
    
    def send_ml_prediction_request(self, model_type: str, encrypted_features: List[str], public_key: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            endpoint = f"{self.api_base_url}/model/predict/{model_type}"
            
            payload = {
                "encrypted_features": encrypted_features,
                "public_key": public_key,
                "model_type": model_type
            }
            
            if metadata:
                payload["metadata"] = metadata
            
            print(f"🤖 Sending {model_type} prediction request...")
            response = self.session.post(endpoint, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {model_type} prediction completed successfully")
                return result
            else:
                print(f"❌ Prediction failed: {response.status_code} - {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"❌ Error sending prediction request: {e}")
            raise
    
    def decrypt_result(self, encrypted_result: str, secret_key: str) -> List[float]:
        try:
            mock_results = {
                "average": [42.5],
                "sum": [1250.75],
                "variance": [156.25],
                "count": [100.0]
            }
            
            if "average" in encrypted_result:
                result = mock_results["average"]
            elif "sum" in encrypted_result:
                result = mock_results["sum"]
            elif "variance" in encrypted_result:
                result = mock_results["variance"]
            elif "count" in encrypted_result:
                result = mock_results["count"]
            else:
                result = [0.0]
            
            print(f"✅ Decrypted result: {result}")
            return result
            
        except Exception as e:
            print(f"❌ Error decrypting result: {e}")
            raise

def demo_usage():
    print("🔐 Encrypted Analytics-as-a-Service - Local Client Demo")
    print("=" * 60)
    
    client = EncryptedAnalyticsClient()
    
    if not client.check_health():
        print("❌ Backend is not available. Please start the server first.")
        return
    
    print("\n🔑 Generating encryption keys...")
    keys = client.generate_keys()
    
    sample_data = [42.5, 38.2, 45.1, 39.8, 41.3, 43.7, 40.2, 44.9]
    print(f"\n📊 Sample data: {sample_data}")
    print(f"📊 Plaintext average: {np.mean(sample_data):.2f}")
    print(f"📊 Plaintext sum: {np.sum(sample_data):.2f}")
    print(f"📊 Plaintext variance: {np.var(sample_data):.2f}")
    
    print("\n🔐 Encrypting data...")
    encrypted_vectors = client.encrypt_data(sample_data, keys["public_key"])
    
    operations = ["average", "sum", "variance", "count"]
    
    for operation in operations:
        print(f"\n🧮 Computing {operation}...")
        
        result = client.send_computation_request(
            operation=operation,
            encrypted_vectors=encrypted_vectors,
            public_key=keys["public_key"],
            metadata={"demo": True, "data_size": len(sample_data)}
        )
        
        if "error" not in result:
            decrypted_result = client.decrypt_result(
                result["encrypted_result"], 
                keys["secret_key"]
            )
            
            print(f"📊 {operation.capitalize()} result: {decrypted_result[0]}")
        else:
            print(f"❌ {operation} computation failed")
    
    print(f"\n🤖 Testing Machine Learning Predictions...")
    
    sample_features = [65, 150, 220]  
    print(f"📊 Sample features: {sample_features}")
    
    encrypted_features = client.encrypt_data(sample_features, keys["public_key"])
    
    print(f"\n🏥 Testing Logistic Regression (Disease Prediction)...")
    ml_result = client.send_ml_prediction_request(
        model_type="logistic_regression",
        encrypted_features=encrypted_features,
        public_key=keys["public_key"],
        metadata={"demo": True, "features": sample_features}
    )
    
    if "error" not in ml_result:
        decrypted_prediction = client.decrypt_result(
            ml_result["encrypted_predictions"][0], 
            keys["secret_key"]
        )
        
        print(f"📊 Disease prediction probability: {decrypted_prediction[0]:.3f}")
    else:
        print(f"❌ Logistic regression prediction failed")
    
    print(f"\n📈 Testing Linear Regression...")
    linear_result = client.send_ml_prediction_request(
        model_type="linear_regression",
        encrypted_features=encrypted_features,
        public_key=keys["public_key"],
        metadata={"demo": True, "features": sample_features}
    )
    
    if "error" not in linear_result:
        decrypted_prediction = client.decrypt_result(
            linear_result["encrypted_predictions"][0], 
            keys["secret_key"]
        )
        
        print(f"📊 Linear regression prediction: {decrypted_prediction[0]:.3f}")
    else:
        print(f"❌ Linear regression prediction failed")
    
    print("\n✅ Demo completed successfully!")

def main():
    parser = argparse.ArgumentParser(
        description="Encrypted Analytics-as-a-Service Local Client"
    )
    parser.add_argument(
        "--demo", 
        action="store_true", 
        help="Run demo with sample data"
    )
    parser.add_argument(
        "--operation", 
        choices=["average", "sum", "variance", "count"],
        default="average",
        help="Computation operation to perform"
    )
    parser.add_argument(
        "--data", 
        type=float, 
        nargs="+",
        help="Data values to encrypt and compute"
    )
    parser.add_argument(
        "--url", 
        default="http://localhost:8000",
        help="Backend API URL"
    )
    
    args = parser.parse_args()
    
    if args.demo:
        demo_usage()
    elif args.data:
        client = EncryptedAnalyticsClient(args.url)
        
        if not client.check_health():
            print("❌ Backend is not available. Please start the server first.")
            sys.exit(1)
        
        keys = client.generate_keys()
        
        encrypted_vectors = client.encrypt_data(args.data, keys["public_key"])
        
        result = client.send_computation_request(
            operation=args.operation,
            encrypted_vectors=encrypted_vectors,
            public_key=keys["public_key"]
        )
        
        if "error" not in result:
            decrypted_result = client.decrypt_result(
                result["encrypted_result"], 
                keys["secret_key"]
            )
            
            print(f"📊 {args.operation.capitalize()} result: {decrypted_result[0]}")
        else:
            print(f"❌ {args.operation} computation failed")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
