#!/usr/bin/env python3
"""
Sample data generator for the Homomorphic Privacy Platform

This script generates various sample datasets for testing the platform's features:
- Medical data for disease prediction (logistic regression)
- Housing data for price prediction (linear regression)
- Student scores for statistical operations
- Financial data for both statistical and ML operations
"""

import numpy as np
import pandas as pd
import os
import argparse
from typing import Dict, Any, List, Tuple

# Ensure reproducibility
np.random.seed(42)

def generate_medical_data(num_samples: int = 50) -> pd.DataFrame:
    """
    Generate sample medical data for disease prediction
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        DataFrame with medical data
    """
    # Generate features
    ages = np.random.normal(55, 15, num_samples).astype(int)
    ages = np.clip(ages, 25, 85)  # Reasonable age range
    
    blood_pressures = np.random.normal(140, 20, num_samples).astype(int)
    blood_pressures = np.clip(blood_pressures, 90, 200)  # Reasonable BP range
    
    cholesterols = np.random.normal(200, 40, num_samples).astype(int)
    cholesterols = np.clip(cholesterols, 120, 300)  # Reasonable cholesterol range
    
    # Generate labels based on a simple rule
    risk_scores = (
        0.02 * (ages - 50) +  # Age factor
        0.01 * (blood_pressures - 140) +  # BP factor
        0.005 * (cholesterols - 200)  # Cholesterol factor
    )
    
    # Convert to probabilities and generate binary labels
    probabilities = 1 / (1 + np.exp(-risk_scores))
    has_disease = (np.random.random(num_samples) < probabilities).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'age': ages,
        'blood_pressure': blood_pressures,
        'cholesterol': cholesterols,
        'has_disease': has_disease
    })
    
    return df

def generate_housing_data(num_samples: int = 50) -> pd.DataFrame:
    """
    Generate sample housing data for price prediction
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        DataFrame with housing data
    """
    # Generate features
    areas = np.random.randint(800, 3001, num_samples)  # 800-3000 sq ft
    bedrooms = np.random.randint(1, 6, num_samples)  # 1-5 bedrooms
    ages = np.random.randint(0, 51, num_samples)  # 0-50 years old
    
    # Generate prices based on a linear model with some noise
    prices = (
        100 +  # Base price
        0.1 * areas +  # Area factor
        20 * bedrooms +  # Bedroom factor
        -1 * ages +  # Age factor (negative correlation)
        np.random.normal(0, 20, num_samples)  # Random noise
    ).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'area': areas,
        'bedrooms': bedrooms,
        'age': ages,
        'price': prices
    })
    
    return df

def generate_student_data(num_samples: int = 50) -> pd.DataFrame:
    """
    Generate sample student data for statistical operations
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        DataFrame with student data
    """
    # Generate features
    hours_studied = np.random.randint(1, 11, num_samples)  # 1-10 hours
    previous_scores = np.random.randint(50, 101, num_samples)  # 50-100 points
    sleep_hours = np.random.randint(4, 11, num_samples)  # 4-10 hours
    
    # Generate final scores based on a model with some noise
    final_scores = (
        50 +  # Base score
        2 * hours_studied +  # Study factor
        0.3 * previous_scores +  # Previous performance factor
        1 * sleep_hours +  # Sleep factor
        np.random.normal(0, 3, num_samples)  # Random noise
    ).astype(int)
    
    # Clip to valid range
    final_scores = np.clip(final_scores, 50, 100)
    
    # Create DataFrame
    df = pd.DataFrame({
        'hours_studied': hours_studied,
        'previous_score': previous_scores,
        'sleep_hours': sleep_hours,
        'final_score': final_scores
    })
    
    return df

def generate_financial_data(num_samples: int = 50) -> pd.DataFrame:
    """
    Generate sample financial data for both statistical and ML operations
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        DataFrame with financial data
    """
    # Generate features
    transaction_amounts = np.random.randint(10, 1001, num_samples)  # $10-$1000
    transaction_types = np.random.randint(1, 4, num_samples)  # 1=deposit, 2=withdrawal, 3=transfer
    
    # Generate account balances with some logic
    account_balances = np.zeros(num_samples)
    current_balance = 5000  # Starting balance
    
    for i in range(num_samples):
        if transaction_types[i] == 1:  # Deposit
            current_balance += transaction_amounts[i]
        elif transaction_types[i] == 2:  # Withdrawal
            current_balance -= transaction_amounts[i]
        # For transfers (type 3), balance doesn't change
        
        account_balances[i] = current_balance
    
    # Generate fraud flags based on some rules
    # Higher transaction amounts and withdrawals are more likely to be fraudulent
    fraud_probabilities = (
        0.001 * transaction_amounts +  # Amount factor
        0.02 * (transaction_types == 2) +  # Withdrawal factor
        -0.01 * (transaction_types == 1)  # Deposit factor (negative)
    )
    
    # Clip probabilities to valid range
    fraud_probabilities = np.clip(fraud_probabilities, 0.01, 0.2)
    
    # Generate binary fraud flags
    fraud_flags = (np.random.random(num_samples) < fraud_probabilities).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'transaction_amount': transaction_amounts,
        'account_balance': account_balances.astype(int),
        'transaction_type': transaction_types,
        'fraud_flag': fraud_flags
    })
    
    return df

def save_dataframe(df: pd.DataFrame, filename: str):
    """
    Save DataFrame to CSV file
    
    Args:
        df: DataFrame to save
        filename: Output filename
    """
    df.to_csv(filename, index=False)
    print(f"✅ Dataset saved to {filename}")

def analyze_dataframe(df: pd.DataFrame, dataset_name: str):
    """
    Print analysis of the generated dataset
    
    Args:
        df: DataFrame to analyze
        dataset_name: Name of the dataset
    """
    print(f"\n📊 {dataset_name} Dataset Analysis")
    print("=" * 40)
    print(f"Number of samples: {len(df)}")
    print(f"Number of features: {len(df.columns)}")
    print(f"Columns: {', '.join(df.columns)}")
    print("\n📈 Summary Statistics:")
    print(df.describe().round(2))
    print("\n")

def generate_encrypted_test_data(num_samples: int = 10) -> Dict[str, Any]:
    """
    Generate mock encrypted data for testing API endpoints
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        Dictionary containing mock encrypted data
    """
    # Generate mock encrypted vectors
    encrypted_vectors = []
    for i in range(num_samples):
        mock_encrypted = f"encrypted_vector_{i+1}_sample_{np.random.randint(1000, 9999)}"
        encrypted_vectors.append(mock_encrypted)
    
    # Generate mock public key
    public_key = "mock_public_key_for_testing_" + str(np.random.randint(10000, 99999))
    
    return {
        "encrypted_vectors": encrypted_vectors,
        "public_key": public_key,
        "metadata": {
            "test": True,
            "num_samples": num_samples,
            "generated_at": pd.Timestamp.now().isoformat()
        }
    }

def save_encrypted_test_data(data: Dict[str, Any], filename: str):
    """
    Save encrypted test data to JSON file
    
    Args:
        data: Dictionary containing encrypted test data
        filename: Output filename
    """
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Encrypted test data saved to {filename}")

def main():
    """
    Generate and save sample datasets
    """
    parser = argparse.ArgumentParser(description="Generate sample datasets for Homomorphic Privacy Platform")
    parser.add_argument(
        "--num_samples", 
        type=int, 
        default=50, 
        help="Number of samples to generate for each dataset"
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        default=".", 
        help="Directory to save the generated datasets"
    )
    parser.add_argument(
        "--analyze", 
        action="store_true", 
        help="Print analysis of the generated datasets"
    )
    parser.add_argument(
        "--encrypted", 
        action="store_true", 
        help="Also generate encrypted test data for API testing"
    )
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("🔬 Generating Sample Datasets for Homomorphic Privacy Platform")
    print("=" * 70)
    
    # Generate and save medical data
    print("\n🏥 Generating Medical Data...")
    medical_df = generate_medical_data(args.num_samples)
    medical_filename = os.path.join(args.output_dir, "medical_data.csv")
    save_dataframe(medical_df, medical_filename)
    if args.analyze:
        analyze_dataframe(medical_df, "Medical")
    
    # Generate and save housing data
    print("\n🏠 Generating Housing Data...")
    housing_df = generate_housing_data(args.num_samples)
    housing_filename = os.path.join(args.output_dir, "housing_data.csv")
    save_dataframe(housing_df, housing_filename)
    if args.analyze:
        analyze_dataframe(housing_df, "Housing")
    
    # Generate and save student data
    print("\n🎓 Generating Student Data...")
    student_df = generate_student_data(args.num_samples)
    student_filename = os.path.join(args.output_dir, "student_scores.csv")
    save_dataframe(student_df, student_filename)
    if args.analyze:
        analyze_dataframe(student_df, "Student")
    
    # Generate and save financial data
    print("\n💰 Generating Financial Data...")
    financial_df = generate_financial_data(args.num_samples)
    financial_filename = os.path.join(args.output_dir, "financial_data.csv")
    save_dataframe(financial_df, financial_filename)
    if args.analyze:
        analyze_dataframe(financial_df, "Financial")
    
    # Generate encrypted test data if requested
    if args.encrypted:
        print("\n🔐 Generating Encrypted Test Data...")
        encrypted_data = generate_encrypted_test_data(10)
        encrypted_filename = os.path.join(args.output_dir, "encrypted_test_data.json")
        save_encrypted_test_data(encrypted_data, encrypted_filename)
    
    print("\n✅ Sample dataset generation completed!")
    print("📁 Files created:")
    print(f"  - {medical_filename}")
    print(f"  - {housing_filename}")
    print(f"  - {student_filename}")
    print(f"  - {financial_filename}")
    if args.encrypted:
        print(f"  - {encrypted_filename}")
    print("\n🚀 Use these files to test the Homomorphic Privacy Platform!")
    print("\n📋 Next steps:")
    print("1. Start backend: python start_backend.py")
    print("2. Start frontend: python start_frontend.py")
    print("3. Test system: python test_system.py")
    print("4. Open http://localhost:3000 to use the web interface")

if __name__ == "__main__":
    main()