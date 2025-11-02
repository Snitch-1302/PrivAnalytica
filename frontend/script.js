// Global variables
let selectedFile = null;
let selectedOperation = null;
let chart = null;
let encryptedData = null; // Store encrypted data from JSON files
let demoKeys = null; // Store demo keys for decryption simulation
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
const columnSelectionSection = document.getElementById('columnSelectionSection');
const columnSelect = document.getElementById('columnSelect');
const columnInfo = document.getElementById('columnInfo');

// Dataset column definitions
const datasetColumns = {
    financial: {
        name: 'Financial Data',
        columns: [
            { name: 'transaction_amount', index: 0, description: 'Transaction amount' },
            { name: 'account_balance', index: 1, description: 'Account balance' },
            { name: 'transaction_type', index: 2, description: 'Transaction type (1=Deposit, 2=Withdrawal, 3=Transfer)' },
            { name: 'fraud_flag', index: 3, description: 'Fraud indicator (0=Normal, 1=Fraud)' }
        ]
    },
    medical: {
        name: 'Medical Data',
        columns: [
            { name: 'age', index: 0, description: 'Patient age in years' },
            { name: 'blood_pressure', index: 1, description: 'Blood pressure reading' },
            { name: 'cholesterol', index: 2, description: 'Cholesterol level' },
            { name: 'has_disease', index: 3, description: 'Disease indicator (0=No disease, 1=Has disease)' }
        ]
    },
    housing: {
        name: 'Housing Data',
        columns: [
            { name: 'area', index: 0, description: 'House area in square feet' },
            { name: 'bedrooms', index: 1, description: 'Number of bedrooms' },
            { name: 'age', index: 2, description: 'House age in years' },
            { name: 'price', index: 3, description: 'House price in thousands' }
        ]
    },
    student: {
        name: 'Student Scores Data',
        columns: [
            { name: 'hours_studied', index: 0, description: 'Hours studied per week' },
            { name: 'previous_score', index: 1, description: 'Previous exam score' },
            { name: 'sleep_hours', index: 2, description: 'Average hours of sleep' },
            { name: 'final_score', index: 3, description: 'Final exam score' }
        ]
    }
};
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

async function processSelectedFile(file) {
    selectedFile = file;
    encryptedData = null; // Reset encrypted data    
    // Update UI
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    
    try {
        const text = await file.text();
        
        // Parse as JSON (encrypted data files)
        if (file.name.toLowerCase().endsWith('.json')) {
            try {
                const jsonData = JSON.parse(text);
                
                // Check if it's an encrypted data file
                if (jsonData.encrypted_vectors && jsonData.public_key) {
                    encryptedData = jsonData;
                    showStatus(`🔐 Encrypted data loaded! (${jsonData.encrypted_vectors.length} encrypted vectors)`, 'success');
                    
                    // Load demo keys if available (for decryption simulation)
                    await loadDemoKeys();
                } else {
                    showStatus(`File "${file.name}" is not a valid encrypted data file.`, 'error');
                }
            } catch (jsonError) {
                console.error('Error parsing JSON:', jsonError);
                showStatus(`File "${file.name}" could not be parsed as JSON.`, 'error');
            }
        }
        // For CSV files, inform user to use encrypted JSON files
        else if (file.name.toLowerCase().endsWith('.csv')) {
            showStatus(`📄 CSV file selected. For encrypted operations, please select the encrypted JSON file from encrypted_data folder.`, 'info');
            encryptedData = null;
        }
        else {
            showStatus(`Please select an encrypted JSON file (.json) from the encrypted_data folder.`, 'info');
            encryptedData = null;
        }
    } catch (error) {
        console.error('Error reading file:', error);
        encryptedData = null;
        showStatus(`Error loading file "${file.name}": ${error.message}`, 'error');
    }
    
    // Detect dataset type and populate columns
    populateColumnSelector(file.name);
    
    // If a statistical operation is already selected, show column selector
    if (selectedOperation && ['average', 'sum', 'variance', 'count'].includes(selectedOperation)) {
        columnSelectionSection.style.display = 'block';
    }
    
    updateExecuteButton();
}

async function loadDemoKeys() {
    // Try to load demo keys from the demo_keys.json file
    try {
        const response = await fetch('encrypted_data/demo_keys.json');
        if (response.ok) {
            demoKeys = await response.json();
            console.log('Demo keys loaded for decryption simulation');
        }
    } catch (error) {
        console.log('Demo keys not available (using mock decryption)');
        demoKeys = null;
    }
}

function detectDatasetType(filename) {
    const lowerName = filename.toLowerCase();
    if (lowerName.includes('financial')) return 'financial';
    if (lowerName.includes('medical')) return 'medical';
    if (lowerName.includes('housing')) return 'housing';
    if (lowerName.includes('student')) return 'student';
    return null;
}

function populateColumnSelector(filename) {
    const datasetType = detectDatasetType(filename);
    
    // Clear existing options except "All Columns"
    columnSelect.innerHTML = '<option value="">All Columns (default)</option>';
    
    if (datasetType && datasetColumns[datasetType]) {
        const dataset = datasetColumns[datasetType];
        
        // Add column options
        dataset.columns.forEach(col => {
            const option = document.createElement('option');
            option.value = col.index;
            option.textContent = `${col.name} - ${col.description}`;
            columnSelect.appendChild(option);
        });
        
        columnInfo.textContent = `Detected: ${dataset.name} with ${dataset.columns.length} columns`;
    } else {
        columnInfo.textContent = 'Column information not available. Use "All Columns" or load a recognized dataset.';
    }
    
    // Show column selector if a statistical operation is selected
    if (selectedOperation && ['average', 'sum', 'variance', 'count'].includes(selectedOperation)) {
        columnSelectionSection.style.display = 'block';
    } else {
        // Hide if no statistical operation is selected
        columnSelectionSection.style.display = 'none';
    }
}
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getColumnName(filename, columnIndex) {
    const datasetType = detectDatasetType(filename);
    if (datasetType && datasetColumns[datasetType]) {
        const col = datasetColumns[datasetType].columns.find(c => c.index === columnIndex);
        return col ? col.name : null;
    }
    return null;
}

function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    if (lines.length === 0) return { headers: [], rows: [] };
    
    const headers = lines[0].split(',').map(h => h.trim());
    const rows = [];
    
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim());
        if (values.length === headers.length) {
            const row = {};
            headers.forEach((header, index) => {
                const numValue = parseFloat(values[index]);
                row[header] = isNaN(numValue) ? values[index] : numValue;
            });
            rows.push(row);
        }
    }
    
    return { headers, rows };
}

// Simulate decryption of encrypted computation result
// This computes what the decrypted value would be based on the original data metadata
// In real homomorphic encryption, this would decrypt using the secret key
function simulateDecryption(encryptedResult, operation, encryptedData, columnIndex) {
    // First, try to use precomputed statistics from metadata (most accurate)
    if (encryptedData && encryptedData.metadata && encryptedData.metadata.computed_statistics) {
        const computedStats = encryptedData.metadata.computed_statistics;
        const numericColumns = encryptedData.columns?.numeric || [];
        
        // Determine which column to use
        let targetColumn = null;
        if (columnIndex !== null && columnIndex >= 0 && columnIndex < numericColumns.length) {
            // Specific column selected
            targetColumn = numericColumns[columnIndex];
        } else {
            // When "All Columns" is selected, default to first column for individual column stats
            // This matches the user expectation where "all columns" shows first column's stats
            if (numericColumns.length > 0) {
                targetColumn = numericColumns[0];  // Use first column when "All Columns" is selected
            } else {
                targetColumn = "all_columns";  // Fallback to aggregated stats
            }
        }
        
        // Get statistics for the target column
        let columnStats = null;
        if (computedStats[targetColumn]) {
            columnStats = computedStats[targetColumn];
        } else if (computedStats["all_columns"]) {
            // Fallback to all_columns if specific column not found
            columnStats = computedStats["all_columns"];
        }
        
        // Return the precomputed statistic
        if (columnStats) {
            switch (operation) {
                case 'average':
                    return columnStats.average.toFixed(2);
                case 'sum':
                    return columnStats.sum.toFixed(2);
                case 'variance':
                    return columnStats.variance.toFixed(2);
                case 'count':
                    return columnStats.count.toString();
            }
        }
    }
    
    // Fallback: use count from num_rows if available
    if (operation === 'count' && encryptedData && encryptedData.num_rows) {
        return encryptedData.num_rows.toString();
    }
    
    // Last fallback: Extract operation type from encrypted result string for demo
    // In real system, this would be actual decryption
    if (encryptedResult.includes('average')) {
        return 'N/A (Decrypt with secret key to see result)';
    } else if (encryptedResult.includes('sum')) {
        return 'N/A (Decrypt with secret key to see result)';
    } else if (encryptedResult.includes('variance')) {
        return 'N/A (Decrypt with secret key to see result)';
    } else if (encryptedResult.includes('count')) {
        return encryptedData?.num_rows?.toString() || 'N/A';
    }
    
    return 'N/A (Decrypt with secret key to see result)';
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
    
    // Show/hide column selector based on operation type
    const isStatisticalOperation = ['average', 'sum', 'variance', 'count'].includes(selectedOperation);
    if (isStatisticalOperation && selectedFile) {
        columnSelectionSection.style.display = 'block';
        // Ensure column selector is populated if file was selected first
        populateColumnSelector(selectedFile.name);
    } else {
        columnSelectionSection.style.display = 'none';
    }
        showStatus(`Selected analysis: ${selectedOperation}`, 'info');
    updateExecuteButton();
}

function displayOperationDescription(operation) {
    const descriptions = {
        average: {
            title: "📊 Statistical Average",
            description: "Calculate the mean of a specific column across all rows using homomorphic encryption. Operations are performed column-wise.",
            algorithm: "Sum all column values / Count of rows",
            security: "🔐 Fully encrypted computation (column-wise)"
        },
        sum: {
            title: "➕ Secure Summation", 
            description: "Add all values in a specific column together without decrypting them. Operations are performed column-wise.",
            algorithm: "Homomorphic addition of column values",
            security: "🔐 Zero-knowledge summation (column-wise)"
        },
        variance: {
            title: "📈 Encrypted Variance",
            description: "Calculate statistical variance for a specific column on encrypted data. Operations are performed column-wise.",
            algorithm: "Mean squared deviation from mean (column-wise)",
            security: "🔐 Privacy-preserving statistics (column-wise)"        },
        count: {
            title: "🔢 Secure Counting",
            description: "Count the number of encrypted values. Simple but essential for many analytics.",
            algorithm: "Homomorphic counting operation",
            security: "🔐 Encrypted aggregation"
        },
        logistic_regression: {
            title: "🏥 Disease Prediction",
            description: "Predict disease probability using encrypted medical features. Features: age, blood pressure, cholesterol. ⚠️ REQUIRES MEDICAL DATA ONLY",            algorithm: "Encrypted dot product + sigmoid",
            security: "🔐 Secure ML inference"
        },
        linear_regression: {
            title: "📈 Linear Prediction",
            description: "Predict continuous values using encrypted medical features (age, blood_pressure, cholesterol). ⚠️ REQUIRES MEDICAL DATA ONLY",            algorithm: "Encrypted linear combination",
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
            // Check if this is medical data
            const isMedicalData = file.name.toLowerCase().includes('medical');
            
            if (!isMedicalData) {
                throw new Error(
                    `${operation === 'logistic_regression' ? 'Logistic Regression' : 'Linear Regression'} ` +
                    `only works with medical data. ` +
                    `This model requires features: age, blood_pressure, cholesterol. ` +
                    `Selected file: ${file.name}`
                );
            }
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
                    operation: operation,
                    dataset_type: "medical"                }
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
            
            // Compute deterministic prediction from actual medical data if available
            let decryptedValue = null;
            let actualFeatures = null;
            
            if (encryptedData && encryptedData.metadata && encryptedData.metadata.sample_original_data) {
                // Use first sample's actual data for prediction
                const sampleData = encryptedData.metadata.sample_original_data[0];
                if (sampleData) {
                    const age = parseFloat(sampleData.age) || 55;
                    const bp = parseFloat(sampleData.blood_pressure) || 140;
                    const chol = parseFloat(sampleData.cholesterol) || 200;
                    
                    actualFeatures = [age, bp, chol];
                    
                    if (operation === 'logistic_regression') {
                        // Logistic regression: weights * features + intercept, then sigmoid
                        // Model weights: [0.2, -0.1, 0.3] for [age, bp, chol], intercept: -2.5
                        const linear = (0.2 * age) + (-0.1 * bp) + (0.3 * chol) + (-2.5);
                        // Sigmoid approximation: 1 / (1 + exp(-linear))
                        const probability = 1 / (1 + Math.exp(-linear));
                        // Clamp between 0 and 1
                        decryptedValue = Math.max(0, Math.min(1, probability)).toFixed(3);
                    } else if (operation === 'linear_regression') {
                        // Linear regression: weights * features + bias
                        // Model weights: [0.5, 0.3, 0.2] for [age, bp, chol], bias: 10.0
                        const pred = (0.5 * age) + (0.3 * bp) + (0.2 * chol) + 10.0;
                        decryptedValue = pred.toFixed(1);
                    }
                }
            }
            
            // Fallback to deterministic mock value if no data available
            if (!decryptedValue) {
                // Use a hash of the filename to get consistent but varied values
                let hash = 0;
                for (let i = 0; i < file.name.length; i++) {
                    hash = ((hash << 5) - hash) + file.name.charCodeAt(i);
                    hash = hash & hash; // Convert to 32bit integer
                }
                const seed = Math.abs(hash) % 1000;
                
                if (operation === 'logistic_regression') {
                    decryptedValue = (0.3 + (seed / 1000) * 0.6).toFixed(3);
                } else {
                    decryptedValue = (50 + (seed / 10) % 100).toFixed(1);
                }
            }
            return {
                encrypted: prediction,
                decrypted: decryptedValue,
                description: operation === 'logistic_regression' ? 
                    "Disease prediction probability" : 
                    "Linear regression prediction",
                actualFeatures: actualFeatures // Store for chart
            };
        }

        // Handle statistical operations with real API calls
        if (['average', 'sum', 'variance', 'count'].includes(operation)) {
            // Use actual encrypted data if available, otherwise use mock
            let encryptedVectors = [];
            let publicKey = "mock_public_key_for_demo";
            
            if (encryptedData && encryptedData.encrypted_vectors) {
                encryptedVectors = encryptedData.encrypted_vectors;
                publicKey = encryptedData.public_key;
                console.log(`Using ${encryptedVectors.length} encrypted vectors from loaded file`);
            } else {
                // Fallback to mock data for demo
                encryptedVectors = [
                    "encrypted_vector_1_sample_1234",
                    "encrypted_vector_2_sample_5678",
                    "encrypted_vector_3_sample_9012"
                ];
                console.log('Using mock encrypted vectors (no encrypted data file loaded)');
            }
            
            // Get selected column index
            const selectedColumnIndex = columnSelect.value === '' ? null : parseInt(columnSelect.value);
            const selectedColumnName = selectedColumnIndex !== null && selectedFile ? 
                getColumnName(selectedFile.name, selectedColumnIndex) : null;
            
            const requestData = {
                encrypted_vectors: encryptedVectors,
                public_key: publicKey,
                column_index: selectedColumnIndex,  // null = analyze all columns; set to 0,1,2,3 for specific column
                column_name: selectedColumnName,
                metadata: {
                    demo: true,
                    filename: file.name,
                    operation: operation,
                    note: selectedColumnIndex !== null ? 
                        `Computing ${operation} for column index ${selectedColumnIndex} (${selectedColumnName || 'unknown'})` :
                        "Statistical operations are computed column-wise across all rows"
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
            
            // Simulate decryption of the encrypted result
            // In real homomorphic encryption, this would decrypt using the secret key
            // For demo purposes, we compute what the decrypted value would be based on metadata
            let decryptedValue = simulateDecryption(encryptedResult, operation, encryptedData, selectedColumnIndex);

            // Build description with column information
            let description = `${operation.charAt(0).toUpperCase() + operation.slice(1)} of encrypted values`;
            if (selectedColumnIndex !== null && selectedColumnName) {
                description = `${operation.charAt(0).toUpperCase() + operation.slice(1)} of column "${selectedColumnName}"`;
            } else if (selectedColumnIndex !== null) {
                description = `${operation.charAt(0).toUpperCase() + operation.slice(1)} of column index ${selectedColumnIndex}`;
            }
            return {
                encrypted: encryptedResult,
                decrypted: decryptedValue,
                description: description
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
    // Display encrypted result (show truncated if too long)
    const encryptedText = result.encrypted || '';
    if (encryptedText.length > 100) {
        encryptedResult.textContent = encryptedText.substring(0, 100) + '...';
        encryptedResult.title = encryptedText; // Show full text on hover
    } else {
        encryptedResult.textContent = encryptedText;
    }
    
    // Display decrypted result with description if available
    let decryptedText = result.decrypted || 'N/A';
    if (result.description) {
        decryptedResult.textContent = `${decryptedText} (${result.description})`;
    } else {
        decryptedResult.textContent = decryptedText;
    }
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
        chartType = 'bar'; // Use bar chart for clearer comparison
        const prediction = parseFloat(result.decrypted) || 0;
        
        // Use actual features if available, otherwise use placeholder
        const features = result.actualFeatures || [65, 150, 220];
        const featureLabels = ['Age', 'Blood Pressure', 'Cholesterol', 'Prediction'];
        
        // Separate features and prediction for clearer visualization
        chartData = {
            labels: featureLabels,
            datasets: [
                {
                    label: 'Input Features',
                    data: [...features, null], // Features only, prediction in separate dataset
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Model Prediction',
                    data: [null, null, null, prediction], // Only show prediction
                    backgroundColor: 'rgba(72, 187, 120, 0.8)',
                    borderColor: 'rgba(72, 187, 120, 1)',
                    borderWidth: 2
                }
            ]
        };
        
        // Create chart with custom options for linear regression
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
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += context.parsed.y.toFixed(1);
                                    if (context.dataset.label === 'Model Prediction') {
                                        label += ' (computed from features)';
                                    } else {
                                        label += ' (input feature)';
                                    }
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Value'
                        }
                    }
                }
            }
        });
        return; // Exit early since we created the chart
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

