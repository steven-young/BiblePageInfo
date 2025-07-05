// Initialize the Bible parser
const parser = new BibleReferenceParser();

// DOM elements
const form = document.getElementById('referenceForm');
const input = document.getElementById('referenceInput');
const resultsContainer = document.getElementById('results');

// Form submission handler
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const reference = input.value.trim();
    if (!reference) {
        showResult({
            success: false,
            error: "Please enter a Bible reference."
        });
        return;
    }
    
    // Show loading state
    showLoading();
    
    // Process the reference (simulate async processing)
    setTimeout(() => {
        const result = parser.parseAndConvert(reference);
        showResult(result);
    }, 100);
});

// Show loading state
function showLoading() {
    resultsContainer.innerHTML = `
        <div class="result">
            <div class="result-main">
                <span class="loading"></span>
                Processing reference...
            </div>
        </div>
    `;
}

// Display results
function showResult(result) {
    resultsContainer.innerHTML = '';
    
    if (result.success) {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result success';
        
        let content = `
            <div class="result-main">
                📖 <strong>${result.reference}</strong> can be found on ${result.isRange ? 'pages' : 'page'} <strong>${result.page}</strong>
            </div>
        `;
        
        if (result.warning) {
            content += `
                <div class="result-warning">
                    ⚠️ ${result.warning}
                </div>
            `;
        }
        
        if (result.bookInfo) {
            content += `
                <div class="result-details">
                    <h4>Reference Details</h4>
                    <div class="detail-item"><strong>Book:</strong> ${result.bookInfo.name}</div>
                    ${result.bookInfo.chapter ? `<div class="detail-item"><strong>Chapter:</strong> ${result.bookInfo.chapter}</div>` : ''}
                    ${result.isRange ? 
                        `<div class="detail-item"><strong>Page Range:</strong> ${result.pageStart} - ${result.pageEnd}</div>` :
                        `<div class="detail-item"><strong>Page:</strong> ${result.page}</div>`
                    }
                </div>
            `;
        }
        
        resultDiv.innerHTML = content;
        resultsContainer.appendChild(resultDiv);
        
    } else {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result error';
        resultDiv.innerHTML = `
            <div class="result-main">
                ❌ ${result.error}
            </div>
        `;
        resultsContainer.appendChild(resultDiv);
    }
}

// Auto-focus input on page load
window.addEventListener('load', () => {
    input.focus();
});

// Clear results when input is cleared
input.addEventListener('input', () => {
    if (!input.value.trim()) {
        resultsContainer.innerHTML = '';
    }
});