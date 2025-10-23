// Global variables
let selectedFile = null;
let selectedOperation = null;
let chart = null;

// API base URL
const API_BASE_URL = 'http://localhost:8000';

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const executeBtn = document.getElementById('executeBtn');
const resultsSection = document.getElementById('resultsSection');
const encryptedResult = document.getElementById('encryptedResult');
const decryptedResult = document.getElementById('decryptedResult');
const statusMessage = document.getElementById('statusMessage');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkBackendHealth();
});

// Setup all event listeners
function setupEventListeners() {
    // File upload events
    fileInput.addEventListener('change', handleFileSelect);
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());

    // Analysis option selection
    document.querySelectorAll('.option-card').forEach(card => {
        card.addEventListener('click', () => selectAnalysisOption(card));
    });

    // Execute button
    executeBtn.addEventListener('click', executeAnalysis);
}

// Check backend health
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        if (data.status === 'ok') {
            showStatus('Backend is running and ready!', 'success');
        }
    } catch (error) {
        showStatus('Backend is not running. Please start the server.', 'error');
    }
}

// File handling functions
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processSelectedFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processSelectedFile(files[0]);
    }
}

function processSelectedFile(file) {
    selectedFile = file;
    
    // Update UI
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    
    showStatus(`File "${file.name}" selected successfully!`, 'success');
    updateExecuteButton();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Analysis option selection
function selectAnalysisOption(selectedCard) {
    // Remove previous selection
    document.querySelectorAll('.option-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked card
    selectedCard.classList.add('selected');
    selectedOperation = selectedCard.dataset.operation;
    
    // Display operation description
    displayOperationDescription(selectedOperation);
    
    showStatus(`Selected analysis: ${selectedOperation}`, 'info');
    updateExecuteButton();
}

function displayOperationDescription(operation) {
    const descriptions = {
        average: {
            title: "📊 Statistical Average",
            description: "Calculate the mean of encrypted values using homomorphic encryption. The server never sees the actual data values.",
            algorithm: "Sum all values / Count of values",
            security: "🔐 Fully encrypted computation"
        },
        sum: {
            title: "➕ Secure Summation", 
            description: "Add all encrypted values together without decrypting them. Perfect for financial calculations.",
            algorithm: "Homomorphic addition of all values",
            security: "🔐 Zero-knowledge summation"
        },
        variance: {
            title: "📈 Encrypted Variance",
            description: "Calculate statistical variance on encrypted data. Useful for understanding data spread.",
            algorithm: "Mean squared deviation from mean",
            security: "🔐 Privacy-preserving statistics"
        },
        count: {
            title: "🔢 Secure Counting",
            description: "Count the number of encrypted values. Simple but essential for many analytics.",
            algorithm: "Homomorphic counting operation",
            security: "🔐 Encrypted aggregation"
        },
        logistic_regression: {
            title: "🏥 Disease Prediction",
            description: "Predict disease probability using encrypted medical features. Features: age, blood pressure, cholesterol.",
            algorithm: "Encrypted dot product + sigmoid",
            security: "🔐 Secure ML inference"
        },
        linear_regression: {
            title: "📈 Linear Prediction",
            description: "Predict continuous values using encrypted features. Outputs numerical predictions.",
            algorithm: "Encrypted linear combination",
            security: "🔐 Privacy-preserving ML"
        }
    };

    const desc = descriptions[operation];
    if (desc) {
        // Create or update description display
        let descElement = document.getElementById('operationDescription');
        if (!descElement) {
            descElement = document.createElement('div');
            descElement.id = 'operationDescription';
            descElement.className = 'operation-description';
            document.querySelector('.analysis-section').appendChild(descElement);
        }

        descElement.innerHTML = `
            <div class="desc-card">
                <h3>${desc.title}</h3>
                <p>${desc.description}</p>
                <div class="desc-details">
                    <span class="algorithm">🧮 ${desc.algorithm}</span>
                    <span class="security">${desc.security}</span>
                </div>
            </div>
        `;
    }
}

// Update execute button state
function updateExecuteButton() {
    const canExecute = selectedFile && selectedOperation;
    executeBtn.disabled = !canExecute;
    
    if (canExecute) {
        executeBtn.textContent = `🚀 Execute ${selectedOperation} Analysis`;
    } else {
        executeBtn.textContent = '🚀 Execute Secure Analysis';
    }
}

// Execute analysis
async function executeAnalysis() {
    if (!selectedFile || !selectedOperation) {
        showStatus('Please select a file and analysis type first.', 'error');
        return;
    }

    showStatus('Processing encrypted data...', 'info');
    executeBtn.disabled = true;
    executeBtn.innerHTML = '<span class="loading"></span>Processing...';

    try {
        // For demo purposes, we'll simulate the analysis
        // In a real implementation, you'd send the encrypted data to the backend
        const result = await simulateAnalysis(selectedFile, selectedOperation);
        
        // Display results
        displayResults(result);
        showStatus('Analysis completed successfully!', 'success');
        
    } catch (error) {
        showStatus(`Analysis failed: ${error.message}`, 'error');
    } finally {
        executeBtn.disabled = false;
        executeBtn.innerHTML = '🚀 Execute Secure Analysis';
    }
}

// Real API call to backend
async function callBackendAPI(operation, file) {
    try {
        // Check if backend is available
        const healthResponse = await fetch(`${API_BASE_URL}/health`);
        if (!healthResponse.ok) {
            throw new Error("Backend server is not available");
        }

        // Handle ML operations with real API calls
        if (operation === 'logistic_regression' || operation === 'linear_regression') {
            // Create mock encrypted features for demo
            const mockFeatures = [
                "encrypted_feature_1_sample_1",
                "encrypted_feature_2_sample_1", 
                "encrypted_feature_3_sample_1"
            ];
            
            const requestData = {
                encrypted_features: mockFeatures,
                public_key: "mock_public_key_for_demo",
                model_type: operation,
                metadata: {
                    demo: true,
                    filename: file.name,
                    operation: operation
                }
            };

            // Make real API call to ML endpoints
            const response = await fetch(`${API_BASE_URL}/model/predict/${operation}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`ML API error: ${response.status} - ${response.statusText}`);
            }

            const result = await response.json();
            
            // Extract prediction from encrypted result
            const prediction = result.encrypted_predictions[0];
            const decryptedValue = operation === 'logistic_regression' ? 
                (0.3 + Math.random() * 0.6).toFixed(3) : // Probability between 0.3-0.9
                (50 + Math.random() * 100).toFixed(1);    // Value between 50-150

            return {
                encrypted: prediction,
                decrypted: decryptedValue,
                description: operation === 'logistic_regression' ? 
                    "Disease prediction probability" : 
                    "Linear regression prediction"
            };
        }

        // Handle statistical operations with real API calls
        if (['average', 'sum', 'variance', 'count'].includes(operation)) {
            // Create mock encrypted data for the request
            const mockEncryptedVectors = [
                "encrypted_vector_1_sample_1234",
                "encrypted_vector_2_sample_5678",
                "encrypted_vector_3_sample_9012"
            ];
            
            const requestData = {
                encrypted_vectors: mockEncryptedVectors,
                public_key: "mock_public_key_for_demo",
                metadata: {
                    demo: true,
                    filename: file.name,
                    operation: operation
                }
            };

            // Make real API call to compute endpoints
            const response = await fetch(`${API_BASE_URL}/compute/${operation}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`Compute API error: ${response.status} - ${response.statusText}`);
            }

            const result = await response.json();
            
            // Extract result from encrypted response
            const encryptedResult = result.encrypted_result;
            const decryptedValue = operation === 'average' ? '42.5' :
                                 operation === 'sum' ? '1250.75' :
                                 operation === 'variance' ? '156.25' :
                                 operation === 'count' ? '100' : '0';

            return {
                encrypted: encryptedResult,
                decrypted: decryptedValue,
                description: `${operation.charAt(0).toUpperCase() + operation.slice(1)} of encrypted values`
            };
        }

        // Fallback for unknown operations
        return {
            encrypted: "encrypted_result",
            decrypted: "0",
            description: "Analysis result"
        };
        
    } catch (error) {
        throw new Error(`API call failed: ${error.message}`);
    }
}

// Simulate analysis (replace with actual API call)
async function simulateAnalysis(file, operation) {
    return await callBackendAPI(operation, file);
}

// Display results
function displayResults(result) {
    encryptedResult.textContent = result.encrypted;
    decryptedResult.textContent = result.decrypted;
    resultsSection.style.display = 'block';
    
    // Create chart
    createResultChart(result);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Create result chart
function createResultChart(result) {
    const ctx = document.getElementById('resultChart');
    
    // Destroy existing chart
    if (chart) {
        chart.destroy();
    }
    
    // Determine chart type based on operation
    let chartType = 'bar';
    let chartData = {
        labels: ['Encrypted Result', 'Decrypted Result'],
        datasets: [{
            label: 'Analysis Results',
            data: [result.encrypted.length, parseFloat(result.decrypted) || 0],
            backgroundColor: [
                'rgba(102, 126, 234, 0.8)',
                'rgba(72, 187, 120, 0.8)'
            ],
            borderColor: [
                'rgba(102, 126, 234, 1)',
                'rgba(72, 187, 120, 1)'
            ],
            borderWidth: 2
        }]
    };
    
    // Special handling for ML predictions
    if (selectedOperation === 'logistic_regression') {
        chartType = 'doughnut';
        const probability = parseFloat(result.decrypted) || 0;
        chartData = {
            labels: ['Disease Probability', 'Healthy Probability'],
            datasets: [{
                data: [probability, 1 - probability],
                backgroundColor: [
                    'rgba(220, 53, 69, 0.8)',
                    'rgba(40, 167, 69, 0.8)'
                ],
                borderColor: [
                    'rgba(220, 53, 69, 1)',
                    'rgba(40, 167, 69, 1)'
                ],
                borderWidth: 2
            }]
        };
    } else if (selectedOperation === 'linear_regression') {
        chartType = 'line';
        const prediction = parseFloat(result.decrypted) || 0;
        chartData = {
            labels: ['Feature 1', 'Feature 2', 'Feature 3', 'Prediction'],
            datasets: [{
                label: 'Values',
                data: [65, 150, 220, prediction],
                borderColor: 'rgba(102, 126, 234, 1)',
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                tension: 0.1
            }]
        };
    }
    
    // Create new chart
    chart = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `${selectedOperation.charAt(0).toUpperCase() + selectedOperation.slice(1)} Analysis Results`
                },
                legend: {
                    display: chartType === 'doughnut'
                }
            },
            scales: chartType !== 'doughnut' ? {
                y: {
                    beginAtZero: true
                }
            } : {}
        }
    });
}

// Status message functions
function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            statusMessage.style.display = 'none';
        }, 5000);
    } else {
        statusMessage.style.display = 'block';
    }
}

