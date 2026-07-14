# Encrypted Analytics-as-a-Service

A privacy-preserving data analysis platform using homomorphic encryption and secure machine learning. This platform allows you to perform statistical computations and ML predictions on encrypted data without ever decrypting it.

## Features

### Privacy-Preserving Analytics
- **Statistical Operations**: Average, Sum, Variance, Count
- **Machine Learning**: Logistic Regression, Linear Regression
- **Homomorphic Encryption**: CKKS scheme for floating-point operations
- **Zero-Knowledge**: Server never sees actual data values

### Easy to Use
- **Web Interface**: Intuitive drag-and-drop file upload
- **REST API**: Complete API documentation
- **Real-time Results**: Instant encrypted computation results
- **Visualization**: Interactive charts and graphs

### Security Features
- **End-to-End Encryption**: Data encrypted before leaving client
- **Secure Computation**: Homomorphic operations on encrypted data
- **Audit Logging**: Complete operation tracking
- **CORS Protection**: Configurable cross-origin policies

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (HTML/JS)     │◄──►│   (FastAPI)     │◄──►│   (SQLite)      │
│   Port 3000     │    │   Port 8000     │    │   (Logs)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start (Windows 11)

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd homomorphic-privacy-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Start the system**
   ```bash
   python start_system.py
   ```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Project Structure

```
homomorphic-privacy-platform/
├── backend/                 # Backend FastAPI application
│   ├── main.py             # FastAPI application entry point
│   ├── encryption_utils.py # Homomorphic encryption utilities
│   ├── requirements.txt    # Python dependencies
│   ├── routes/             # API route modules
│   │   ├── compute.py      # Statistical operations
│   │   ├── model.py        # ML predictions
│   │   └── logs.py         # Logging and reports
│   ├── db/                 # Database models
│   │   └── models.py       # SQLite models
│   └── utils/              # Utility functions
├── frontend/               # Frontend web application
│   ├── index.html          # Main web interface
│   ├── logs.html           # Logs interface
│   ├── script.js           # Frontend JavaScript
│   ├── logs.js             # Logs JavaScript
│   └── style.css           # Styling
├── sample_data/            # Sample datasets for testing
│   ├── financial_data.csv  # Financial dataset
│   ├── housing_data.csv    # Housing dataset
│   ├── medical_data.csv    # Medical dataset
│   ├── student_scores.csv  # Student scores dataset
│   └── generate_sample_data.py # Data generator
├── encrypted_data/         # Mock encrypted data for testing
│   ├── encrypted_test_data.json # General test data
│   ├── encrypted_financial_data.json # Financial encrypted data
│   ├── encrypted_medical_data.json # Medical encrypted data
│   ├── encrypted_housing_data.json # Housing encrypted data
│   ├── encrypted_student_data.json # Student encrypted data
│   └── generate_encrypted_data.py # Encrypted data generator
├── local_client/           # Local client utilities
│   ├── encrypt_and_send.py # Client encryption script
│   └── requirements.txt    # Client dependencies
├── logs/                   # Application logs
├── start_system.py         # MAIN: Unified system startup
├── start_backend.py        # Backend-only startup
├── start_frontend.py       # Frontend-only startup
├── start_system.bat        # Windows batch script
├── start_system.sh         # Linux/Mac shell script
├── test_system.py          # System integration tests
├── docker-compose.yml      # Docker orchestration
├── Dockerfile              # Root Dockerfile
├── netlify.toml            # Netlify deployment config
├── vercel.json             # Vercel deployment config
├── env.example             # Environment variables template
└── README.md               # This file
```

## Startup Options

### Option 1: Unified System (Recommended)
```bash
python start_system.py
```
This starts both backend and frontend automatically.

### Option 2: Individual Services
```bash
# Terminal 1 - Backend
python start_backend.py

# Terminal 2 - Frontend
python start_frontend.py
```

### Option 3: Platform Scripts
```bash
# Windows
start_system.bat

# Linux/Mac
chmod +x start_system.sh
./start_system.sh
```

## Testing

### Test the System
```bash
python test_system.py
```

### Generate Sample Data
```bash
python sample_data/generate_sample_data.py
```

### Generate Encrypted Test Data
```bash
python encrypted_data/generate_encrypted_data.py
```

## API Documentation

### Health Check
```http
GET /health
```

### Statistical Operations
```http
POST /compute/average
POST /compute/sum
POST /compute/variance
POST /compute/count
```

### Machine Learning
```http
POST /model/predict/logistic_regression
POST /model/predict/linear_regression
```

### Logs & Reports
```http
GET /logs/                    # List all logs
GET /logs/stats              # Operation statistics
GET /logs/report/csv         # Generate CSV report
GET /logs/report/download/{filename}  # Download report
```

## Configuration

### Backend Configuration
- **Host**: `0.0.0.0` (configurable in `main.py`)
- **Port**: `8000` (configurable in `main.py`)
- **Logs**: Stored in `logs/` directory
- **Database**: SQLite in `backend/data/logs.db`

### Frontend Configuration
- **Port**: `3000` (configurable in `start_frontend.py`)
- **API URL**: `http://localhost:8000` (configurable in `script.js`)

## Docker Deployment

### Build and Run
```bash
# Build the Docker image
docker build -t encrypted-analytics .

# Run the container
docker run -p 8000:8000 encrypted-analytics
```

### Using Docker Compose
```bash
docker-compose up -d
```

## Data Organization

### Sample Data (`sample_data/`)
- **Purpose**: Raw CSV datasets for testing
- **Generated by**: `generate_sample_data.py`
- **Contains**: Financial, medical, housing, and student data

### Encrypted Data (`encrypted_data/`)
- **Purpose**: Mock encrypted data for testing API endpoints
- **Generated by**: `generate_encrypted_data.py`
- **Note**: This is **mock encrypted data** for demonstration purposes

## Local Client

The `local_client/` directory contains a Python client library for:

- **Encrypting data** using homomorphic encryption
- **Sending encrypted data** to the backend API
- **Receiving and decrypting** computation results
- **Testing the system** programmatically

### Usage
```bash
# Run demo
python local_client/encrypt_and_send.py --demo

# Custom computation
python local_client/encrypt_and_send.py --operation average --data 1 2 3 4 5
```

## Security Considerations

### Current Implementation
- **Demo Mode**: Uses mock encryption for demonstration
- **Production Ready**: Framework supports real homomorphic encryption
- **Key Management**: Keys should be managed securely in production

### Production Deployment
1. Replace mock encryption with real TenSEAL implementation
2. Implement proper key management
3. Add authentication and authorization
4. Configure HTTPS
5. Set up proper logging and monitoring

## Logging

The system provides comprehensive logging:
- **Application Logs**: `logs/app.log`
- **Startup Logs**: `logs/startup.log`
- **Database Logs**: Stored in SQLite database
- **API Logs**: Available via `/logs/` endpoints

## Deployment Options

### Local Development
- Use the provided startup scripts
- Access via localhost

### Docker Deployment
- Use Dockerfile for containerized deployment
- Suitable for cloud platforms

### Cloud Deployment
- **Frontend**: Vercel/Netlify (using `vercel.json`/`netlify.toml`)
- **Backend**: Render/Railway/Heroku
- **Database**: Cloud SQL/PostgreSQL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the API documentation at `http://localhost:8000/docs`
- Review the logs in the `logs/` directory
- Open an issue in the repository

## Future Enhancements

- [ ] Real homomorphic encryption implementation
- [ ] Additional ML models (Random Forest, Neural Networks)
- [ ] Multi-party computation support
- [ ] Cloud deployment guides
- [ ] Performance optimization
- [ ] Advanced visualization features
- [ ] Authentication and authorization
- [ ] Production environment configuration

---

** Note**: This is a demonstration platform. For production use, implement proper security measures and real homomorphic encryption.

## Quick Commands

```bash
# Start everything
python start_system.py

# Test the system
python test_system.py

# Generate sample data
python sample_data/generate_sample_data.py

# Generate encrypted test data
python encrypted_data/generate_encrypted_data.py

# Run client demo
python local_client/encrypt_and_send.py --demo
```
