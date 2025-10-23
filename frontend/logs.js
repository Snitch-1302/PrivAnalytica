document.addEventListener('DOMContentLoaded', function() {
    // API Base URL
    const API_BASE_URL = 'http://localhost:8000';
    
    // DOM Elements
    const statsContainer = document.getElementById('statsCards');
    const logsTableBody = document.getElementById('logsTableBody');
    const paginationContainer = document.getElementById('pagination');
    const reportsContainer = document.getElementById('reportsList');
    const operationTypeFilter = document.getElementById('operationTypeFilter');
    const statusFilter = document.getElementById('statusFilter');
    const refreshLogsBtn = document.getElementById('refreshLogsBtn');
    const generateReportBtn = document.getElementById('generateReportBtn');
    const logDetailsModal = document.getElementById('logDetailsModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const logDetailsContent = document.getElementById('logDetailsContent');
    
    // Pagination state
    let currentPage = 1;
    const logsPerPage = 10;
    let totalLogs = 0;
    let filteredLogs = [];
    
    // Initialize the dashboard
    initDashboard();
    
    // Event listeners
    if (refreshLogsBtn) {
        refreshLogsBtn.addEventListener('click', fetchLogs);
    }
    
    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', generateReport);
    }
    
    if (operationTypeFilter) {
        operationTypeFilter.addEventListener('change', function() {
            currentPage = 1;
            fetchLogs();
        });
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            currentPage = 1;
            fetchLogs();
        });
    }
    
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            logDetailsModal.style.display = 'none';
        });
    }
    
    // Close modal when clicking outside of it
    window.addEventListener('click', function(event) {
        if (event.target === logDetailsModal) {
            logDetailsModal.style.display = 'none';
        }
    });
    
    // Initialize dashboard
    function initDashboard() {
        fetchStats();
        fetchLogs();
        fetchReports();
    }
    
    // Fetch operation statistics
    function fetchStats() {
        fetch(`${API_BASE_URL}/logs/stats`)
            .then(response => response.json())
            .then(data => {
                renderStats(data);
            })
            .catch(error => {
                console.error('Error fetching stats:', error);
                showMessage('Error fetching operation statistics', 'error');
            });
    }
    
    // Render statistics cards
    function renderStats(stats) {
        if (!statsContainer) return;
        
        statsContainer.innerHTML = '';
        
        // Total Operations Card
        const totalCard = createStatCard('Total Operations', stats.total_operations, '📊');
        statsContainer.appendChild(totalCard);
        
        // Success Rate Card
        const successRate = stats.total_operations > 0 
            ? Math.round((stats.successful_operations / stats.total_operations) * 100) 
            : 0;
        const successCard = createStatCard('Success Rate', `${successRate}%`, '✅');
        statsContainer.appendChild(successCard);
        
        // Average Duration Card
        const avgDuration = stats.total_operations > 0 
            ? (stats.average_duration_ms / 1000).toFixed(2) 
            : 0;
        const durationCard = createStatCard('Avg Duration', `${avgDuration}s`, '⏱️');
        statsContainer.appendChild(durationCard);
        
        // Most Common Operation Card
        const commonOpCard = createStatCard('Most Common', stats.most_common_operation || 'N/A', '🔄');
        statsContainer.appendChild(commonOpCard);
    }
    
    // Create a stat card element
    function createStatCard(label, value, icon) {
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.innerHTML = `
            <div class="stat-icon">${icon}</div>
            <div class="stat-value">${value}</div>
            <div class="stat-label">${label}</div>
        `;
        return card;
    }
    
    // Fetch logs with filtering and pagination
    function fetchLogs() {
        const operationType = operationTypeFilter ? operationTypeFilter.value : '';
        const status = statusFilter ? statusFilter.value : '';
        
        let url = `${API_BASE_URL}/logs`;
        const params = [];
        
        if (operationType) params.push(`operation_type=${operationType}`);
        if (status) params.push(`status=${status}`);
        
        if (params.length > 0) {
            url += `?${params.join('&')}`;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                filteredLogs = data;
                totalLogs = data.length;
                renderLogs();
                renderPagination();
            })
            .catch(error => {
                console.error('Error fetching logs:', error);
                showMessage('Error fetching operation logs', 'error');
            });
    }
    
    // Render logs table with pagination
    function renderLogs() {
        if (!logsTableBody) return;
        
        logsTableBody.innerHTML = '';
        
        const startIndex = (currentPage - 1) * logsPerPage;
        const endIndex = Math.min(startIndex + logsPerPage, totalLogs);
        const paginatedLogs = filteredLogs.slice(startIndex, endIndex);
        
        if (paginatedLogs.length === 0) {
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = `<td colspan="6" style="text-align: center;">No logs found</td>`;
            logsTableBody.appendChild(emptyRow);
            return;
        }
        
        paginatedLogs.forEach(log => {
            const row = document.createElement('tr');
            
            // Format timestamp
            const timestamp = new Date(log.timestamp).toLocaleString();
            
            // Format duration
            const duration = log.duration_ms ? `${(log.duration_ms / 1000).toFixed(2)}s` : 'N/A';
            
            // Status class
            const statusClass = log.status === 'success' ? 'status-success' : 'status-error';
            
            row.innerHTML = `
                <td>${log.id}</td>
                <td>${log.operation_type}</td>
                <td>${timestamp}</td>
                <td>${duration}</td>
                <td class="${statusClass}">${log.status}</td>
                <td>
                    <button class="view-details-btn" data-log-id="${log.id}">View Details</button>
                </td>
            `;
            
            logsTableBody.appendChild(row);
        });
        
        // Add event listeners to view details buttons
        document.querySelectorAll('.view-details-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const logId = this.getAttribute('data-log-id');
                showLogDetails(logId);
            });
        });
    }
    
    // Render pagination controls
    function renderPagination() {
        if (!paginationContainer) return;
        
        paginationContainer.innerHTML = '';
        
        const totalPages = Math.ceil(totalLogs / logsPerPage);
        
        // Previous button
        const prevBtn = document.createElement('button');
        prevBtn.className = 'page-btn';
        prevBtn.textContent = 'Previous';
        prevBtn.disabled = currentPage === 1;
        prevBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                renderLogs();
                renderPagination();
            }
        });
        paginationContainer.appendChild(prevBtn);
        
        // Page info
        const pageInfo = document.createElement('span');
        pageInfo.textContent = `Page ${currentPage} of ${totalPages || 1}`;
        paginationContainer.appendChild(pageInfo);
        
        // Next button
        const nextBtn = document.createElement('button');
        nextBtn.className = 'page-btn';
        nextBtn.textContent = 'Next';
        nextBtn.disabled = currentPage === totalPages || totalPages === 0;
        nextBtn.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                renderLogs();
                renderPagination();
            }
        });
        paginationContainer.appendChild(nextBtn);
    }
    
    // Show log details in modal
    function showLogDetails(logId) {
        fetch(`${API_BASE_URL}/logs/${logId}`)
            .then(response => response.json())
            .then(log => {
                if (!logDetailsContent) return;
                
                // Format timestamp
                const timestamp = new Date(log.timestamp).toLocaleString();
                
                // Format duration
                const duration = log.duration_ms ? `${(log.duration_ms / 1000).toFixed(2)} seconds` : 'N/A';
                
                // Format metadata if available
                let metadataHtml = '';
                if (log.metadata && Object.keys(log.metadata).length > 0) {
                    metadataHtml = `
                        <div class="metadata-section">
                            <div class="metadata-title">Additional Metadata</div>
                            <pre class="detail-value">${JSON.stringify(log.metadata, null, 2)}</pre>
                        </div>
                    `;
                }
                
                logDetailsContent.innerHTML = `
                    <div class="detail-group">
                        <span class="detail-label">Operation ID</span>
                        <div class="detail-value">${log.id}</div>
                    </div>
                    <div class="detail-group">
                        <span class="detail-label">Operation Type</span>
                        <div class="detail-value">${log.operation_type}</div>
                    </div>
                    <div class="detail-group">
                        <span class="detail-label">Timestamp</span>
                        <div class="detail-value">${timestamp}</div>
                    </div>
                    <div class="detail-group">
                        <span class="detail-label">Duration</span>
                        <div class="detail-value">${duration}</div>
                    </div>
                    <div class="detail-group">
                        <span class="detail-label">Status</span>
                        <div class="detail-value ${log.status === 'success' ? 'status-success' : 'status-error'}">${log.status}</div>
                    </div>
                    <div class="detail-group">
                        <span class="detail-label">Details</span>
                        <div class="detail-value">${log.details || 'No details available'}</div>
                    </div>
                    ${metadataHtml}
                `;
                
                logDetailsModal.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching log details:', error);
                showMessage('Error fetching log details', 'error');
            });
    }
    
    // Fetch generated reports
    function fetchReports() {
        fetch(`${API_BASE_URL}/logs/report/list`)
            .then(response => response.json())
            .then(reports => {
                renderReports(reports);
            })
            .catch(error => {
                console.error('Error fetching reports:', error);
                showMessage('Error fetching reports', 'error');
            });
    }
    
    // Render reports list
    function renderReports(reports) {
        if (!reportsContainer) return;
        
        reportsContainer.innerHTML = '';
        
        if (reports.length === 0) {
            reportsContainer.innerHTML = '<p>No reports generated yet.</p>';
            return;
        }
        
        reports.forEach(report => {
            const reportCard = document.createElement('div');
            reportCard.className = 'report-card';
            
            // Format creation date
            const creationDate = new Date(report.created_at).toLocaleString();
            
            reportCard.innerHTML = `
                <div class="report-title">${report.filename}</div>
                <div class="report-info">
                    <p><strong>Created:</strong> ${creationDate}</p>
                    <p><strong>Type:</strong> ${report.report_type}</p>
                    <p><strong>Size:</strong> ${formatFileSize(report.size_bytes)}</p>
                </div>
                <a href="${API_BASE_URL}/logs/report/download/${report.filename}" class="download-btn" download>Download Report</a>
            `;
            
            reportsContainer.appendChild(reportCard);
        });
    }
    
    // Generate a new report
    function generateReport() {
        const operationType = operationTypeFilter ? operationTypeFilter.value : '';
        const status = statusFilter ? statusFilter.value : '';
        
        let url = `${API_BASE_URL}/logs/report/generate`;
        const params = [];
        
        if (operationType) params.push(`operation_type=${operationType}`);
        if (status) params.push(`status=${status}`);
        
        if (params.length > 0) {
            url += `?${params.join('&')}`;
        }
        
        showMessage('Generating report...', 'info');
        
        fetch(url, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                showMessage('Report generation started. It will be available shortly.', 'success');
                // Refresh reports list after a short delay
                setTimeout(fetchReports, 2000);
            })
            .catch(error => {
                console.error('Error generating report:', error);
                showMessage('Error generating report', 'error');
            });
    }
    
    // Helper function to format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Show message to user
    function showMessage(message, type = 'info') {
        const messageContainer = document.getElementById('messageContainer');
        if (!messageContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = message;
        
        messageContainer.innerHTML = '';
        messageContainer.appendChild(messageElement);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }
});