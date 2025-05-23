/**
 * Heart Risk Monitor - Main JavaScript File
 * Contains global utility functions and event handlers for the heart risk monitoring dashboard
 */

// Wait for DOM to be fully loaded before attaching event handlers
document.addEventListener('DOMContentLoaded', function() {
    console.log('Heart Risk Monitor JS loaded successfully');
    
    // Global utility functions
    
    // Format a number with commas for thousands separator
    window.formatNumber = function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };
    
    // Format a percentage value
    window.formatPercent = function(num) {
        return parseFloat(num).toFixed(1) + '%';
    };
    
    // Format a date in a friendly way
    window.formatDate = function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    };
    
    // Global event listeners for common elements across all pages
    
    // Handle dark/light mode toggle if present
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
        });
        
        // Check user's saved preference
        const savedDarkMode = localStorage.getItem('darkMode') === 'true';
        if (savedDarkMode) {
            document.body.classList.add('dark-mode');
        }
    }
    
    // Handle sidebar toggle if present
    const sidebarToggle = document.getElementById('sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }
    
    // Add responsive behavior to tables
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        if (!table.closest('.table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
    
    // Common reset filters functionality
    const resetFiltersBtn = document.getElementById('reset-filters');
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', function() {
            // Reset date range selector
            const dateRangeSelect = document.getElementById('date-range-select');
            if (dateRangeSelect) {
                dateRangeSelect.value = 'week';
                
                // Hide custom date inputs
                const customDateRange = document.getElementById('custom-date-range');
                if (customDateRange) {
                    customDateRange.classList.add('d-none');
                }
            }
            
            // Reset risk level checkboxes
            const riskCheckboxes = document.querySelectorAll('input[name="risk-level"]');
            riskCheckboxes.forEach(checkbox => {
                checkbox.checked = true;
            });
            
            // Clear patient search
            const patientSearch = document.getElementById('patient-search');
            if (patientSearch) {
                patientSearch.value = '';
            }
            
            // Trigger data refresh if needed
            const refreshData = document.getElementById('refresh-data');
            if (refreshData) {
                refreshData.click();
            } else if (window.fetchDashboardData) {
                window.fetchDashboardData();
            }
        });
    }
    
    // Apply filters button
    const applyFiltersBtn = document.getElementById('apply-filters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            if (window.fetchDashboardData) {
                window.fetchDashboardData();
            }
        });
    }
});
