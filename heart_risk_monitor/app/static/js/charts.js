/**
 * Heart Risk Monitor Dashboard Charts
 * JavaScript functions for initializing and updating dashboard charts
 */

// Configure Chart.js defaults
Chart.defaults.font.family = "'Nunito', 'Helvetica', 'Arial', sans-serif";
Chart.defaults.color = '#858796';
Chart.defaults.plugins.tooltip.backgroundColor = "rgb(255, 255, 255)";
Chart.defaults.plugins.tooltip.bodyColor = "#858796";
Chart.defaults.plugins.tooltip.titleMarginBottom = 10;
Chart.defaults.plugins.tooltip.titleColor = '#6e707e';
Chart.defaults.plugins.tooltip.titleFont = {
    family: "'Nunito', 'Helvetica', 'Arial', sans-serif",
    size: 14
};
Chart.defaults.plugins.tooltip.bodyFont = {
    family: "'Nunito', 'Helvetica', 'Arial', sans-serif",
    size: 14
};
Chart.defaults.plugins.tooltip.padding = 15;
Chart.defaults.plugins.tooltip.caretPadding = 10;
Chart.defaults.plugins.tooltip.displayColors = false;
Chart.defaults.plugins.tooltip.borderColor = '#dddfeb';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.callbacks.label = function(context) {
    return context.dataset.label + ": " + context.raw;
};

/**
 * Creates a risk level gauge chart using D3.js
 * @param {string} elementId - The ID of the element to create the gauge in
 * @param {number} value - The current value to display
 * @param {number} min - The minimum value on the gauge
 * @param {number} max - The maximum value on the gauge
 * @param {string} colorScheme - The color scheme to use (e.g., "risk", "normal")
 */
function createGaugeChart(elementId, value, min, max, colorScheme) {
    // Get the element
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // Clear any existing content
    element.innerHTML = '';
    
    // Set up dimensions
    const width = element.offsetWidth;
    const height = 200;
    const radius = Math.min(width, height * 2) / 2;
    
    // Define color ranges based on scheme
    let colorRange;
    if (colorScheme === 'risk') {
        colorRange = ['#1cc88a', '#f6c23e', '#e74a3b']; // Low, Medium, High
    } else {
        colorRange = ['#4e73df', '#1cc88a', '#36b9cc']; // Primary, Success, Info
    }
    
    // Create SVG
    const svg = d3.select(`#${elementId}`)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height})`);
    
    // Create gauge background
    const arc = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius)
        .startAngle(-Math.PI / 2)
        .endAngle(Math.PI / 2);
    
    // Create gradient
    const gradient = svg.append('defs')
        .append('linearGradient')
        .attr('id', `gradient-${elementId}`)
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '100%')
        .attr('y2', '0%');
    
    gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', colorRange[0]);
        
    gradient.append('stop')
        .attr('offset', '50%')
        .attr('stop-color', colorRange[1]);
        
    gradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', colorRange[2]);
    
    // Add background arc
    svg.append('path')
        .attr('d', arc)
        .style('fill', `url(#gradient-${elementId})`);
    
    // Add value needle
    const scale = d3.scaleLinear()
        .domain([min, max])
        .range([-Math.PI / 2, Math.PI / 2]);
    
    const needleLength = radius * 0.8;
    const needleRadius = 5;
    const angle = scale(value);
    
    const needle = svg.append('g')
        .attr('transform', `rotate(${angle * 180 / Math.PI})`);
    
    needle.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', 0)
        .attr('y2', -needleLength)
        .style('stroke', '#6e707e')
        .style('stroke-width', 4);
    
    needle.append('circle')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', needleRadius)
        .style('fill', '#6e707e');
    
    // Add min and max labels
    svg.append('text')
        .attr('x', -radius + 10)
        .attr('y', 20)
        .attr('text-anchor', 'start')
        .text(min);
        
    svg.append('text')
        .attr('x', radius - 10)
        .attr('y', 20)
        .attr('text-anchor', 'end')
        .text(max);
}

/**
 * Creates a heatmap using D3.js
 * @param {string} elementId - The ID of the element to create the heatmap in
 * @param {Array} data - Array of objects with x, y, and value properties
 * @param {Array} xLabels - Array of labels for the x-axis
 * @param {Array} yLabels - Array of labels for the y-axis
 */
function createHeatmap(elementId, data, xLabels, yLabels) {
    // Get the element
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // Clear any existing content
    element.innerHTML = '';
    
    // Set up dimensions
    const margin = {top: 30, right: 30, bottom: 70, left: 70};
    const width = element.offsetWidth - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;
    
    // Create SVG
    const svg = d3.select(`#${elementId}`)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Build X scales and axis
    const x = d3.scaleBand()
        .range([0, width])
        .domain(xLabels)
        .padding(0.01);
        
    svg.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.8em')
        .attr('dy', '.15em')
        .attr('transform', 'rotate(-65)');
    
    // Build Y scales and axis
    const y = d3.scaleBand()
        .range([height, 0])
        .domain(yLabels)
        .padding(0.01);
        
    svg.append('g')
        .call(d3.axisLeft(y));
    
    // Build color scale
    const colorScale = d3.scaleLinear()
        .range(['white', '#4e73df'])
        .domain([0, d3.max(data, d => d.value)]);
    
    // Add tooltip
    const tooltip = d3.select('body')
        .append('div')
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('border', '1px solid #ddd')
        .style('border-radius', '4px')
        .style('padding', '10px')
        .style('display', 'none');
    
    // Create rectangles
    svg.selectAll()
        .data(data)
        .enter()
        .append('rect')
        .attr('x', d => x(d.x))
        .attr('y', d => y(d.y))
        .attr('width', x.bandwidth())
        .attr('height', y.bandwidth())
        .style('fill', d => colorScale(d.value))
        .on('mouseover', function(event, d) {
            tooltip.style('display', 'block');
            tooltip.html(`${d.x} vs ${d.y}: ${d.value.toFixed(2)}`);
            tooltip.style('left', `${event.pageX + 10}px`);
            tooltip.style('top', `${event.pageY - 20}px`);
            d3.select(this).style('stroke', 'black');
        })
        .on('mouseout', function() {
            tooltip.style('display', 'none');
            d3.select(this).style('stroke', 'none');
        });
    
    // Add the value text on each cell
    svg.selectAll()
        .data(data)
        .enter()
        .append('text')
        .attr('x', d => x(d.x) + x.bandwidth() / 2)
        .attr('y', d => y(d.y) + y.bandwidth() / 2)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .text(d => d.value.toFixed(1))
        .style('font-size', '10px')
        .style('fill', d => d.value > 0.5 ? 'white' : 'black');
}

/**
 * Creates a sunburst chart using D3.js
 * @param {string} elementId - The ID of the element to create the sunburst in
 * @param {Object} data - Hierarchical data for the sunburst
 */
function createSunburstChart(elementId, data) {
    // Get the element
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // Clear any existing content
    element.innerHTML = '';
    
    // Set up dimensions
    const width = element.offsetWidth;
    const height = 300;
    const radius = Math.min(width, height) / 2;
    
    // Create SVG
    const svg = d3.select(`#${elementId}`)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2},${height / 2})`);
    
    // Create hierarchical data
    const root = d3.hierarchy(data)
        .sum(d => d.value);
    
    // Create partition layout
    const partition = d3.partition()
        .size([2 * Math.PI, radius]);
    
    // Compute the partition layout
    partition(root);
    
    // Color scale
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    
    // Create arcs
    const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .innerRadius(d => d.y0)
        .outerRadius(d => d.y1);
    
    // Add tooltip
    const tooltip = d3.select('body')
        .append('div')
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('border', '1px solid #ddd')
        .style('border-radius', '4px')
        .style('padding', '10px')
        .style('display', 'none');
    
    // Create paths
    svg.selectAll('path')
        .data(root.descendants())
        .enter()
        .append('path')
        .attr('d', arc)
        .style('fill', d => colorScale(d.data.name))
        .style('stroke', 'white')
        .style('stroke-width', 1)
        .on('mouseover', function(event, d) {
            tooltip.style('display', 'block');
            tooltip.html(`${d.data.name}: ${d.value}`);
            tooltip.style('left', `${event.pageX + 10}px`);
            tooltip.style('top', `${event.pageY - 20}px`);
            d3.select(this).style('opacity', 0.8);
        })
        .on('mouseout', function() {
            tooltip.style('display', 'none');
            d3.select(this).style('opacity', 1);
        });
    
    // Add labels for larger arcs
    svg.selectAll('text')
        .data(root.descendants().filter(d => (d.x1 - d.x0) > 0.1))
        .enter()
        .append('text')
        .attr('transform', d => {
            const x = (d.x0 + d.x1) / 2;
            const y = (d.y0 + d.y1) / 2;
            const angle = x - Math.PI / 2;
            const radius = y;
            return `rotate(${angle * 180 / Math.PI}) translate(${radius},0) rotate(${angle >= Math.PI ? 180 : 0})`;
        })
        .attr('dx', d => d.x0 < Math.PI ? 8 : -8)
        .attr('dy', '.35em')
        .attr('text-anchor', d => d.x0 < Math.PI ? 'start' : 'end')
        .text(d => d.data.name)
        .style('font-size', '10px')
        .style('fill', 'white');
}

/**
 * Initializes all gauge charts on the page
 */
function initializeGaugeCharts() {
    document.querySelectorAll('.chart-gauge').forEach(el => {
        const value = parseFloat(el.getAttribute('data-value') || 0);
        const min = parseFloat(el.getAttribute('data-min') || 0);
        const max = parseFloat(el.getAttribute('data-max') || 100);
        const colorScheme = el.getAttribute('data-colors') || 'normal';
        
        createGaugeChart(el.id, value, min, max, colorScheme);
    });
}

/**
 * Utility function to download chart as image
 * @param {string} chartId - The ID of the chart canvas element
 * @param {string} filename - The filename to save as
 */
function downloadChart(chartId, filename) {
    const canvas = document.getElementById(chartId);
    if (!canvas) return;
    
    const image = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = filename.replace(/\s+/g, '_').toLowerCase() + '.png';
    link.href = image;
    link.click();
}

/**
 * Utility function to download SVG
 * @param {string} svgId - The ID of the SVG container element
 * @param {string} filename - The filename to save as
 */
function downloadSVG(svgId, filename) {
    const container = document.getElementById(svgId);
    if (!container) return;
    
    const svg = container.querySelector('svg');
    if (!svg) return;
    
    const serializer = new XMLSerializer();
    let source = serializer.serializeToString(svg);
    
    source = '<?xml version="1.0" standalone="no"?>\r\n' + source;
    const url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);
    
    const link = document.createElement('a');
    link.download = filename.replace(/\s+/g, '_').toLowerCase() + '.svg';
    link.href = url;
    link.click();
}

// Initialize gauge charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeGaugeCharts();
});
