// Global variables for charts
let priceChartInstance = null;
let rsiChartInstance = null;

// Clock Display
function updateClock() {
    const timeDisplay = document.getElementById("current-time");
    if (timeDisplay) {
        const now = new Date();
        timeDisplay.textContent = now.toLocaleTimeString();
    }
}
setInterval(updateClock, 1000);
updateClock();

// Initialize Charts
function initCharts(data = []) {
    const ctxPrice = document.getElementById('priceChart').getContext('2d');
    const ctxRsi = document.getElementById('rsiChart').getContext('2d');

    const labels = data.map(d => d.date);
    const closePrices = data.map(d => d.close);
    const smaFast = data.map(d => d.sma_14);
    const smaSlow = data.map(d => d.sma_50);
    const rsi = data.map(d => d.rsi);

    // Destroy existing instances if they exist
    if (priceChartInstance) priceChartInstance.destroy();
    if (rsiChartInstance) rsiChartInstance.destroy();

    // 1. Price Overlay Chart
    priceChartInstance = new Chart(ctxPrice, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Spot Price (XAUUSD)',
                    data: closePrices,
                    borderColor: '#f39c12',
                    backgroundColor: 'rgba(243, 156, 18, 0.05)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.1,
                    pointRadius: 2
                },
                {
                    label: 'Fast SMA',
                    data: smaFast,
                    borderColor: '#2ecc71',
                    borderWidth: 1.5,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Slow SMA',
                    data: smaSlow,
                    borderColor: '#e74c3c',
                    borderWidth: 1.5,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#a0a5b5', font: { family: 'Outfit' } }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#a0a5b5', maxTicksLimit: 10 },
                    grid: { color: 'rgba(255,255,255,0.03)' }
                },
                y: {
                    ticks: { color: '#a0a5b5' },
                    grid: { color: 'rgba(255,255,255,0.03)' }
                }
            }
        }
    });

    // 2. RSI Oscillator Sub-chart
    rsiChartInstance = new Chart(ctxRsi, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'RSI (14)',
                    data: rsi,
                    borderColor: '#9b59b6',
                    borderWidth: 1.5,
                    fill: false,
                    pointRadius: 0,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    ticks: { display: false },
                    grid: { display: false }
                },
                y: {
                    min: 0,
                    max: 100,
                    ticks: { 
                        color: '#a0a5b5',
                        stepSize: 30,
                        callback: function(value) { return value; }
                    },
                    grid: { color: 'rgba(255,255,255,0.03)' }
                }
            }
        }
    });
}

// Simple Markdown to HTML Parser for the generated daily briefing report
function parseMarkdown(md) {
    if (!md) return "";
    let html = md;
    
    // Replace Headers
    html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');
    html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
    html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
    
    // Replace Horizontal rules
    html = html.replace(/^---$/gm, '<hr>');
    
    // Replace Blockquotes
    html = html.replace(/^> (.*?)$/gm, '<blockquote><p>$1</p></blockquote>');
    
    // Replace Bullet Lists
    html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/^- (.*?)$/gm, '<li>$1</li>');
    
    // Wrap lists in ul
    html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    
    // Replace Bold Text
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Replace Linebreaks (not matching elements)
    html = html.split('\n').map(line => {
        if (line.trim().startsWith('<h') || line.trim().startsWith('<u') || line.trim().startsWith('<l') || line.trim().startsWith('<b') || line.trim().startsWith('<h') || line.trim().startsWith('<h')) {
            return line;
        }
        return line.trim() ? `<p>${line}</p>` : '';
    }).join('\n');
    
    return html;
}

// Fetch Initial Live News and Prices
async function fetchInitialData() {
    try {
        // Fetch Realtime Price
        const priceRes = await fetch('/api/prices/realtime');
        const priceData = await priceRes.json();
        if (priceData.success) {
            updateLiveMetrics(priceData);
        }
        
        // Fetch News Stream
        const newsRes = await fetch('/api/news');
        const newsData = await newsRes.json();
        if (newsData.success) {
            renderNews(newsData.news);
        }
    } catch (err) {
        console.error("Failed to load initial metrics:", err);
    }
}

// Update UI price elements
function updateLiveMetrics(price) {
    document.getElementById("live-price").textContent = `$${price.price.toFixed(2)}`;
    document.getElementById("bid-price").textContent = price.bid.toFixed(2);
    document.getElementById("ask-price").textContent = price.ask.toFixed(2);
    
    const trendElem = document.getElementById("price-change-trend");
    trendElem.textContent = `${price.change_daily > 0 ? '+' : ''}${price.change_daily.toFixed(2)} (${price.change_pct > 0 ? '+' : ''}${price.change_pct.toFixed(2)}%)`;
    trendElem.className = 'metric-trend ' + (price.change_daily >= 0 ? 'up' : 'down');
    
    // Update chart overlay values if available
    const chartPrice = document.getElementById("chart-live-price");
    const chartChange = document.getElementById("chart-live-change");
    if (chartPrice && chartChange) {
        chartPrice.textContent = `$${price.price.toFixed(2)}`;
        chartChange.textContent = `${price.change_pct > 0 ? '+' : ''}${price.change_pct.toFixed(2)}%`;
        chartChange.className = price.change_daily >= 0 ? 'change-pct up' : 'change-pct down';
    }
}

// Render macroeconomic news list
function renderNews(news = []) {
    const container = document.getElementById("news-list");
    if (!container) return;
    
    if (news.length === 0) {
        container.innerHTML = `<p class="news-placeholder">No macroeconomic headlines available.</p>`;
        return;
    }
    
    container.innerHTML = news.map(item => `
        <div class="news-item">
            <div class="news-header-row">
                <span class="news-source-meta">${item.source} &bull; ${item.timestamp}</span>
                <span class="news-impact-badge ${item.impact.toLowerCase()}">${item.impact}</span>
            </div>
            <h4>${item.title}</h4>
            <p>${item.content}</p>
        </div>
    `).join('');
}

// Console Logging Stream Animation
function streamLogs(logs = []) {
    const consoleElem = document.getElementById("logs-console");
    if (!consoleElem) return;
    
    consoleElem.innerHTML = '';
    let i = 0;
    
    function addNextLog() {
        if (i < logs.length) {
            const entry = document.createElement("p");
            let line = logs[i];
            
            // Format styling based on node context
            if (line.includes("Error") || line.includes("Failed")) {
                entry.className = "log-entry error";
            } else if (line.includes("Starting") || line.includes("Completed")) {
                entry.className = "log-entry system";
            } else {
                entry.className = "log-entry";
            }
            
            entry.textContent = line;
            consoleElem.appendChild(entry);
            consoleElem.scrollTop = consoleElem.scrollHeight;
            i++;
            setTimeout(addNextLog, 150); // Realistic rolling output speed
        }
    }
    
    addNextLog();
}

// Core submit action: Run the workflow
const form = document.getElementById("workflow-form");
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById("btn-run");
    const loader = btn.querySelector(".btn-loader");
    const btnText = btn.querySelector(".btn-text");
    
    // Disable inputs
    btn.disabled = true;
    loader.classList.remove("hidden");
    btnText.textContent = "Processing Multi-Agent Logic...";
    
    // Collect settings
    const payload = {
        custom_rsi_period: parseInt(document.getElementById("rsi-period").value),
        custom_sma_fast: parseInt(document.getElementById("sma-fast").value),
        custom_sma_slow: parseInt(document.getElementById("sma-slow").value)
    };
    
    try {
        const response = await fetch('/api/run-workflow', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 1. Output scrollable agent console logs
            streamLogs(result.logs);
            
            // 2. Update Live Tick Indicators
            updateLiveMetrics(result.realtime_price);
            
            // 3. Update Metrics Grid
            const sentiment = result.macro_sentiment;
            const signals = result.technical_signals;
            
            document.getElementById("sentiment-label").textContent = sentiment.sentiment_label;
            document.getElementById("sentiment-score").textContent = sentiment.average_sentiment_score.toFixed(2);
            
            // Calculate a width percentage based on average sentiment score (-1.0 to +1.0 -> 0% to 100%)
            const percent = ((sentiment.average_sentiment_score + 1.0) / 2.0) * 100;
            document.getElementById("sentiment-bar-fill").style.width = `${percent}%`;
            
            document.getElementById("technical-trend").textContent = signals.indicator_trend;
            document.getElementById("technical-rsi").textContent = signals.rsi.toFixed(2);
            document.getElementById("rsi-status").textContent = signals.rsi_sentiment;
            document.getElementById("crossover-signal").textContent = signals.crossover_signal;
            
            // 4. Update Execution Perf times
            const perf = result.performance;
            document.getElementById("perf-orchestrator").textContent = `${perf.data_orchestrator.toFixed(4)}s`;
            document.getElementById("perf-quant").textContent = `${perf.quant_analyst.toFixed(4)}s`;
            document.getElementById("perf-sentiment").textContent = `${perf.macro_sentiment.toFixed(4)}s`;
            document.getElementById("perf-reporting").textContent = `${perf.reporting_agent.toFixed(4)}s`;
            
            const totalPerf = perf.data_orchestrator + perf.quant_analyst + perf.macro_sentiment + perf.reporting_agent;
            document.getElementById("perf-total").textContent = `${totalPerf.toFixed(4)}s`;
            
            // 5. Update Charts
            initCharts(result.chart_data);
            
            // 6. Output markdown report content
            const briefingContainer = document.getElementById("briefing-report-content");
            briefingContainer.innerHTML = parseMarkdown(result.briefing_report);
            
        } else {
            alert("Error running Multi-Agent Workflow: " + result.error);
        }
    } catch (err) {
        alert("Workflow Execution failed. Verify the backend console server is running.");
        console.error(err);
    } finally {
        btn.disabled = false;
        loader.classList.add("hidden");
        btnText.textContent = "Execute Multi-Agent Workflow";
    }
});

// Setup on initial page load
document.addEventListener("DOMContentLoaded", () => {
    fetchInitialData();
    // Default charts empty init
    initCharts([]);
});
