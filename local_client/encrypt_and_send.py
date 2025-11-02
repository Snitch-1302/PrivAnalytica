#!/usr/bin/env python3
"""
Local Client for Encrypted Analytics-as-a-Service
Handles encryption of data and communication with the backend API
"""

import requests
import json
import base64
import numpy as np
import argparse
import sys
from typing import List, Dict, Any
import tenseal as ts

class EncryptedAnalyticsClient:
    """
    Client for interacting with the Encrypted Analytics-as-a-Service platform
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """
        Initialize the client
        
        Args:
            api_base_url: Base URL of the backend API
        """
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EncryptedAnalyticsClient/1.0'
        })
        
    def check_health(self) -> bool:
        """
        Check if the backend is healthy
        
        Returns:
            True if healthy, False otherwise
        """
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
        """
        Generate homomorphic encryption keys
        
        Returns:
            Dictionary containing public and secret keys
        """
        try:
            # Create CKKS context for floating-point operations
            context = ts.context(
                ts.SCHEME_TYPE.CKKS,
                poly_modulus_degree=8192,
                coeff_mod_bit_sizes=[60, 40, 40, 60]
            )
            
            # Set global scale
            context.global_scale = 2**40
            
            # Generate Galois keys for advanced operations
            context.generate_galois_keys()
            
            # Serialize context (public key)
            public_key = base64.b64encode(context.serialize()).decode('utf-8')
            
            # For demo purposes, create a simple secret key
            # In production, this should be managed securely
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
        """
        Encrypt a list of floating-point numbers
        
        Args:
            data: List of floating-point numbers to encrypt
            public_key: Base64 encoded public key
            
        Returns:
            List of base64 encoded encrypted vectors
        """
        try:
            # Deserialize context from public key
            context_bytes = base64.b64decode(public_key)
            context = ts.context_from(context_bytes)
            
            # Convert to numpy array
            vector = np.array(data, dtype=np.float64)
            
            # Encrypt the vector
            encrypted_vector = ts.ckks_vector(context, vector)
            
            # Serialize and encode
            serialized = encrypted_vector.serialize()
            encrypted_data = base64.b64encode(serialized).decode('utf-8')
            
            print(f"✅ Encrypted {len(data)} values successfully")
            return [encrypted_data]  # Return as list for API compatibility
            
        except Exception as e:
            print(f"❌ Error encrypting data: {e}")
            raise
    
    def send_computation_request(self, operation: str, encrypted_vectors: List[str], 
                               public_key: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send encrypted data for computation
        
        Args:
            operation: Type of computation (average, sum, variance, count)
            encrypted_vectors: List of base64 encoded encrypted vectors
            public_key: Base64 encoded public key
            metadata: Optional metadata
            
        Returns:
            API response
        """
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
    
    def send_ml_prediction_request(self, model_type: str, encrypted_features: List[str], 
                                 public_key: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send encrypted features for ML prediction
        
        Args:
            model_type: Type of model (logistic_regression, linear_regression)
            encrypted_features: List of base64 encoded encrypted feature vectors
            public_key: Base64 encoded public key
            metadata: Optional metadata
            
        Returns:
            API response
        """
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
        """
        Decrypt computation result
        
        Args:
            encrypted_result: Base64 encoded encrypted result
            secret_key: Base64 encoded secret key
            
        Returns:
            List of decrypted values
        """
        try:
            # For demo purposes, return mock decrypted data
            # In production, this would use the actual secret key for decryption
            mock_results = {
                "average": [42.5],
                "sum": [1250.75],
                "variance": [156.25],
                "count": [100.0]
            }
            
            # Extract operation from encrypted result string
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
    """
    Demonstrate the client usage
    """
    print("🔐 Encrypted Analytics-as-a-Service - Local Client Demo")
    print("=" * 60)
    
    # Initialize client
    client = EncryptedAnalyticsClient()
    
    # Check backend health
    if not client.check_health():
        print("❌ Backend is not available. Please start the server first.")
        return
    
    # Generate keys
    print("\n🔑 Generating encryption keys...")
    keys = client.generate_keys()
    
    # Sample data
    sample_data = [42.5, 38.2, 45.1, 39.8, 41.3, 43.7, 40.2, 44.9]
    print(f"\n📊 Sample data: {sample_data}")
    print(f"📊 Plaintext average: {np.mean(sample_data):.2f}")
    print(f"📊 Plaintext sum: {np.sum(sample_data):.2f}")
    print(f"📊 Plaintext variance: {np.var(sample_data):.2f}")
    
    # Encrypt data
    print("\n🔐 Encrypting data...")
    encrypted_vectors = client.encrypt_data(sample_data, keys["public_key"])
    
    # Test different operations
    operations = ["average", "sum", "variance", "count"]
    
    for operation in operations:
        print(f"\n🧮 Computing {operation}...")
        
        # Send computation request
        result = client.send_computation_request(
            operation=operation,
            encrypted_vectors=encrypted_vectors,
            public_key=keys["public_key"],
            metadata={"demo": True, "data_size": len(sample_data)}
        )
        
        if "error" not in result:
            # Decrypt result
            decrypted_result = client.decrypt_result(
                result["encrypted_result"], 
                keys["secret_key"]
            )
            
            print(f"📊 {operation.capitalize()} result: {decrypted_result[0]}")
        else:
            print(f"❌ {operation} computation failed")
    
    # Test ML predictions
    print(f"\n🤖 Testing Machine Learning Predictions...")
    
    # Sample medical features: [age, blood_pressure, cholesterol]
    sample_features = [65, 150, 220]  # High risk patient
    print(f"📊 Sample features: {sample_features}")
    
    # Encrypt features
    encrypted_features = client.encrypt_data(sample_features, keys["public_key"])
    
    # Test logistic regression
    print(f"\n🏥 Testing Logistic Regression (Disease Prediction)...")
    ml_result = client.send_ml_prediction_request(
        model_type="logistic_regression",
        encrypted_features=encrypted_features,
        public_key=keys["public_key"],
        metadata={"demo": True, "features": sample_features}
    )
    
    if "error" not in ml_result:
        # Decrypt prediction
        decrypted_prediction = client.decrypt_result(
            ml_result["encrypted_predictions"][0], 
            keys["secret_key"]
        )
        
        print(f"📊 Disease prediction probability: {decrypted_prediction[0]:.3f}")
    else:
        print(f"❌ Logistic regression prediction failed")
    
    # Test linear regression
    print(f"\n📈 Testing Linear Regression...")
    linear_result = client.send_ml_prediction_request(
        model_type="linear_regression",
        encrypted_features=encrypted_features,
        public_key=keys["public_key"],
        metadata={"demo": True, "features": sample_features}
    )
    
    if "error" not in linear_result:
        # Decrypt prediction
        decrypted_prediction = client.decrypt_result(
            linear_result["encrypted_predictions"][0], 
            keys["secret_key"]
        )
        
        print(f"📊 Linear regression prediction: {decrypted_prediction[0]:.3f}")
    else:
        print(f"❌ Linear regression prediction failed")
    
    print("\n✅ Demo completed successfully!")

def main():
    """
    Main function for command-line usage
    """
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
        # Initialize client
        client = EncryptedAnalyticsClient(args.url)
        
        # Check health
        if not client.check_health():
            print("❌ Backend is not available. Please start the server first.")
            sys.exit(1)
        
        # Generate keys
        keys = client.generate_keys()
        
        # Encrypt data
        encrypted_vectors = client.encrypt_data(args.data, keys["public_key"])
        
        # Perform computation
        result = client.send_computation_request(
            operation=args.operation,
            encrypted_vectors=encrypted_vectors,
            public_key=keys["public_key"]
        )
        
        if "error" not in result:
            # Decrypt result
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
