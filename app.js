// Tab Switching Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons and panes
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.add('hidden'));
            
            // Add active class to clicked button
            btn.classList.add('active');
            
            // Show corresponding pane
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.remove('hidden');
        });
    });

    // Initialize penguin charts
    initPenguinCharts();
});

// Penguin Data Simulation
function simulatePenguinData() {
    const species = ['Adelie', 'Chinstrap', 'Gentoo'];
    const data = [];
    
    for (let i = 0; i < 50; i++) {
        const speciesType = species[Math.floor(Math.random() * species.length)];
        data.push({
            species: speciesType,
            billLength: +(30 + Math.random() * 10).toFixed(1),
            billDepth: +(15 + Math.random() * 5).toFixed(1),
            flipperLength: +(180 + Math.random() * 30).toFixed(0),
            bodyMass: +(3500 + Math.random() * 2000).toFixed(0)
        });
    }
    
    return data;
}

// Initialize Charts
function initCharts() {
    const penguinData = simulatePenguinData();
    const realEstateData = simulateRealEstateData();
    const statsData = simulateStatsData();
    
    // Initialize Penguin Charts
    initPenguinCharts(penguinData);
    
    // Initialize Real Estate Charts
    initRealEstateCharts(realEstateData);
    
    // Initialize Statistics
    initStatistics(statsData);
}

// Penguin Data Simulation
function simulatePenguinData() {
    const species = ['Adelie', 'Chinstrap', 'Gentoo'];
    const data = [];
    
    for (let i = 0; i < 50; i++) {
        const speciesType = species[Math.floor(Math.random() * species.length)];
        data.push({
            species: speciesType,
            billLength: +(30 + Math.random() * 10).toFixed(1),
            billDepth: +(15 + Math.random() * 5).toFixed(1),
            flipperLength: +(180 + Math.random() * 30).toFixed(0),
            bodyMass: +(3500 + Math.random() * 2000).toFixed(0)
        });
    }
    
    return data;
}

// Real Estate Data Simulation
function simulateRealEstateData() {
    const data = [];
    
    for (let i = 0; i < 100; i++) {
        const area = +(80 + Math.random() * 300).toFixed(1);
        const price = area * 50000 + Math.random() * 1000000;
        const year = 2015 + Math.floor(Math.random() * 10);
        
        data.push({
            area,
            price: +price.toFixed(0),
            year
        });
    }
    
    return data;
}

// Statistics Data Simulation
function simulateStatsData() {
    return [
        { variable: 'العمر', mean: 34.2, std: 8.7, min: 18, max: 65 },
        { variable: 'الدخل (بالآلاف)', mean: 45.6, std: 12.3, min: 15, max: 120 },
        { variable: 'حجم الأسرة', mean: 3.8, std: 1.2, min: 1, max: 8 },
        { variable: 'سنوات التعليم', mean: 12.5, std: 3.1, min: 5, max: 22 },
        { variable: 'مؤشر السعادة', mean: 6.8, std: 1.5, min: 2, max: 10 }
    ];
}

// Initialize Penguin Charts
function initPenguinCharts(penguinData) {
    // Populate data table
    const table = document.getElementById('penguinDataTable');
    let tableHTML = `
        <thead>
            <tr>
                <th>النوع</th>
                <th>طول المنقار (مم)</th>
                <th>عمق المنقار (مم)</th>
                <th>طول الزعنفة (مم)</th>
                <th>الكتلة (جم)</th>
            </tr>
        </thead>
        <tbody>
    `;
    
    penguinData.forEach(penguin => {
        tableHTML += `
            <tr>
                <td>${penguin.species}</td>
                <td>${penguin.billLength}</td>
                <td>${penguin.billDepth}</td>
                <td>${penguin.flipperLength}</td>
                <td>${penguin.bodyMass}</td>
            </tr>
        `;
    });
    
    tableHTML += '</tbody>';
    table.innerHTML = tableHTML;
    
    // Correlation Heatmap
    const heatmapCtx = document.getElementById('correlationHeatmap').getContext('2d');
    new Chart(heatmapCtx, {
        type: 'bar',
        data: {
            labels: ['الطول/العمق', 'الطول/الزعنفة', 'الطول/الكتلة', 'العمق/الزعنفة', 'العمق/الكتلة', 'الزعنفة/الكتلة'],
            datasets: [{
                label: 'معامل الارتباط',
                data: [0.65, 0.78, 0.72, -0.58, -0.45, 0.84],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'قيمة الارتباط'
                    }
                }
            }
        }
    });
    
    // PCA Chart
    const pcaCtx = document.getElementById('pcaChart').getContext('2d');
    new Chart(pcaCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Adelie',
                data: Array.from({length: 20}, () => ({
                    x: (Math.random() - 0.5) * 10,
                    y: (Math.random() - 0.5) * 10
                })),
                backgroundColor: 'rgba(255, 99, 132, 0.7)'
            }, {
                label: 'Chinstrap',
                data: Array.from({length: 15}, () => ({
                    x: (Math.random() - 0.2) * 8,
                    y: (Math.random() - 0.3) * 8
                })),
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }, {
                label: 'Gentoo',
                data: Array.from({length: 15}, () => ({
                    x: (Math.random() + 0.5) * 6,
                    y: (Math.random() + 0.5) * 6
                })),
                backgroundColor: 'rgba(75, 192, 192, 0.7)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'المكون الأساسي 1'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'المكون الأساسي 2'
                    }
                }
            }
        }
    });
    
    // Box Plot (simplified)
    const boxCtx = document.getElementById('lengthBoxPlot').getContext('2d');
    new Chart(boxCtx, {
        type: 'boxplot',
        data: {
            labels: ['Adelie', 'Chinstrap', 'Gentoo'],
            datasets: [{
                label: 'توزيع أطوال المناقير',
                data: [
                    [32.1, 33.5, 36.8, 38.5, 40.1],
                    [40.2, 42.6, 46.7, 48.9, 50.3],
                    [44.5, 46.1, 49.5, 52.3, 55.7]
                ],
                backgroundColor: 'rgba(231, 6, 85, 0.84)',
                borderColor: 'rgba(12, 205, 219, 1)',
                borderWidth: 1
            }]
        }
    });
    
    // Histogram
    const histCtx = document.getElementById('lengthHistogram').getContext('2d');
    new Chart(histCtx, {
        type: 'bar',
        data: {
            labels: ['30-35', '35-40', '40-45', '45-50', '50-55'],
            datasets: [{
                label: 'توزيع أطوال المناقير',
                data: [12, 19, 8, 7, 4],
                backgroundColor: 'rgba(153, 102, 255, 0.7)'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'التكرار'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'نطاق الطول (مم)'
                    }
                }
            }
        }
    });
}

// Initialize Real Estate Charts
function initRealEstateCharts(realEstateData) {
    // Area vs Price Scatter
    const scatterCtx = document.getElementById('areaPriceScatter').getContext('2d');
    new Chart(scatterCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'العقارات',
                data: realEstateData.map(property => ({
                    x: property.area,
                    y: property.price
                })),
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'المساحة (م²)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'السعر (ج.م)'
                    }
                }
            }
        }
    });
    
    // Price Timeline
    const timelineCtx = document.getElementById('priceTimeline').getContext('2d');
    
    // Group data by year
    const yearlyData = {};
    realEstateData.forEach(property => {
        if (!yearlyData[property.year]) {
            yearlyData[property.year] = [];
        }
        yearlyData[property.year].push(property.price);
    });
    
    // Calculate average prices
    const years = Object.keys(yearlyData).sort();
    const avgPrices = years.map(year => {
        const prices = yearlyData[year];
        return prices.reduce((sum, price) => sum + price, 0) / prices.length;
    });
    
    new Chart(timelineCtx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'متوسط السعر السنوي',
                data: avgPrices,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'متوسط السعر (ج.م)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'السنة'
                    }
                }
            }
        }
    });
}

// Initialize Statistics
function initStatistics(statsData) {
    // Populate statistics table
    const table = document.getElementById('statsDataTable');
    let tableHTML = `
        <thead>
            <tr>
                <th>المتغير</th>
                <th>المتوسط</th>
                <th>الانحراف المعياري</th>
                <th>الحد الأدنى</th>
                <th>الحد الأقصى</th>
            </tr>
        </thead>
        <tbody>
    `;
    
    statsData.forEach(stat => {
        tableHTML += `
            <tr>
                <td>${stat.variable}</td>
                <td>${stat.mean}</td>
                <td>${stat.std}</td>
                <td>${stat.min}</td>
                <td>${stat.max}</td>
            </tr>
        `;
    });
    
    tableHTML += '</tbody>';
    table.innerHTML = tableHTML;
    
    // Factor Analysis
    const factorCtx = document.getElementById('factorAnalysis').getContext('2d');
    new Chart(factorCtx, {
        type: 'bar',
        data: {
            labels: ['الموقع', 'المساحة', 'المرافق', 'العمر', 'الجودة'],
            datasets: [{
                label: 'تأثير العوامل على السعر',
                data: [0.85, 0.92, 0.78, 0.65, 0.82],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)'
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'مستوى التأثير'
                    }
                }
            }
        }
    });
}

// Tab Switching Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons and panes
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.add('hidden'));
            
            // Add active class to clicked button
            btn.classList.add('active');
            
            // Show corresponding pane
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.remove('hidden');
        });
    });

    // Initialize charts
    initCharts();
});