const API_BASE_URL = 'http://localhost:5000/api';

// ============================================================================
// DOM ELEMENTS
// ============================================================================

const promptInput = document.getElementById('promptInput');
const sourceInput = document.getElementById('sourceInput');
const submitBtn = document.getElementById('submitBtn');
const presetSelect = document.getElementById('presetSelect');
const resultSection = document.getElementById('resultSection');
const outputBox = document.getElementById('outputBox');
const detailsBox = document.getElementById('detailsBox');
const detailsContent = document.getElementById('detailsContent');

// ============================================================================
// PLACEHOLDERS
// ============================================================================

const promptPlaceholder = "Type your prompt...";
const sourcePlaceholder = "Source code...";

// ============================================================================
// INPUT HANDLERS
// ============================================================================

// Prompt input focus/blur
promptInput.addEventListener('focus', () => {
    if (promptInput.innerText === promptPlaceholder) {
        promptInput.innerText = "";
    }
});

promptInput.addEventListener('blur', () => {
    if (promptInput.innerText.trim() === "") {
        promptInput.innerText = promptPlaceholder;
    }
});

// Source input focus/blur
sourceInput.addEventListener('focus', () => {
    if (sourceInput.innerText === sourcePlaceholder) {
        sourceInput.innerText = "";
    }
});

sourceInput.addEventListener('blur', () => {
    if (sourceInput.innerText.trim() === "") {
        sourceInput.innerText = sourcePlaceholder;
    }
});

// ============================================================================
// PRESET HANDLER
// ============================================================================

presetSelect.addEventListener('change', (e) => {
    if (e.target.value !== "") {
        promptInput.innerText = e.target.value;
        promptInput.focus();
    }
});

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function showLoading() {
    outputBox.innerText = "🤖 AI is analyzing your code...\nPlease wait...";
    detailsContent.innerHTML = `
        <div class="flex items-center gap-2 text-white/60">
            <div class="animate-spin rounded-full h-4 w-4 border-2 border-white/20 border-t-white"></div>
            <span>Processing request...</span>
        </div>
    `;
    resultSection.classList.remove('hidden');
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    outputBox.innerHTML = `
        <div class="text-red-400">
            <div class="text-xl mb-2">❌ Error</div>
            <div>${message}</div>
        </div>
    `;
    detailsContent.innerHTML = `
        <div class="text-red-400/80">
            <strong>Status:</strong> Failed<br>
            <strong>Message:</strong> ${message}
        </div>
    `;
}

function formatDiffs(diffs) {
    if (!diffs || diffs.length === 0) return '<p class="text-white/40">No changes made</p>';
    
    let html = '<div class="space-y-3">';
    
    diffs.forEach((diff, index) => {
        const colors = {
            'replace': 'bg-blue-500/10 border-blue-500/30',
            'insert': 'bg-green-500/10 border-green-500/30',
            'delete': 'bg-red-500/10 border-red-500/30'
        };
        
        const icons = {
            'replace': '🔄',
            'insert': '➕',
            'delete': '➖'
        };
        
        const color = colors[diff.operation] || 'bg-white/5 border-white/20';
        const icon = icons[diff.operation] || '📝';
        
        html += `
            <div class="border ${color} rounded-lg p-3">
                <div class="flex items-start gap-2 mb-2">
                    <span class="text-lg">${icon}</span>
                    <div class="flex-1">
                        <div class="text-white font-semibold text-sm">
                            ${diff.operation.toUpperCase()} 
                            <span class="text-white/50">Lines ${diff.start_line}-${diff.end_line}</span>
                        </div>
                        <div class="text-white/60 text-xs mt-1">${diff.reasoning}</div>
                    </div>
                </div>
                ${diff.new_code ? `
                    <pre class="bg-black/40 p-2 rounded text-xs text-white/80 overflow-x-auto mt-2 font-mono">${escapeHtml(diff.new_code)}</pre>
                ` : ''}
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function displayResults(data) {
    // Display modified code
    outputBox.innerText = data.modified_code;
    
    // Display details
    if (data.success) {
        detailsContent.innerHTML = `
            <div class="space-y-3">
                <div class="flex items-center gap-2 text-green-400">
                    <span class="text-xl">✅</span>
                    <span class="font-semibold">Success!</span>
                </div>
                
                <div class="grid grid-cols-2 gap-3 text-sm">
                    <div class="bg-white/5 p-3 rounded">
                        <div class="text-white/50 text-xs mb-1">Total Changes</div>
                        <div class="text-white text-lg font-semibold">${data.details.total_changes}</div>
                    </div>
                    <div class="bg-white/5 p-3 rounded">
                        <div class="text-white/50 text-xs mb-1">Total Lines</div>
                        <div class="text-white text-lg font-semibold">${data.details.total_lines}</div>
                    </div>
                    <div class="bg-white/5 p-3 rounded col-span-2">
                        <div class="text-white/50 text-xs mb-1">Changed</div>
                        <div class="text-white text-lg font-semibold">${data.details.change_percentage}%</div>
                    </div>
                </div>
                
                <div class="border-t border-white/10 pt-3 mt-3">
                    <h4 class="text-white font-semibold mb-2 text-sm">Changes Made:</h4>
                    ${formatDiffs(data.diffs)}
                </div>
            </div>
        `;
    } else {
        showError(data.error);
    }
}

// ============================================================================
// API CALLS
// ============================================================================

async function processCode() {
    const sourceCode = sourceInput.innerText.trim();
    const prompt = promptInput.innerText.trim();
    
    // Validation
    if (!sourceCode || sourceCode === sourcePlaceholder) {
        alert('⚠️ Please enter your source code first!');
        sourceInput.focus();
        return;
    }
    
    if (!prompt || prompt === promptPlaceholder) {
        alert('⚠️ Please enter a prompt or select a preset!');
        promptInput.focus();
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source_code: sourceCode,
                prompt: prompt
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Server error occurred');
        }
        
        displayResults(data);
        
    } catch (error) {
        console.error('API Error:', error);
        showError(error.message || 'Failed to connect to server. Make sure the backend is running.');
    }
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

// Submit button click
submitBtn.addEventListener('click', processCode);

// Enter key (without Shift) to submit
promptInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        processCode();
    }
});

// Also allow Enter in source code to trigger (optional)
sourceInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        e.preventDefault();
        processCode();
    }
});

// ============================================================================
// LOAD PRESETS FROM API
// ============================================================================

async function loadPresets() {
    try {
        const response = await fetch(`${API_BASE_URL}/presets`);
        const data = await response.json();
        
        if (data.presets) {
            // Clear existing options except the first one
            presetSelect.innerHTML = '<option value="">Presets...</option>';
            
            // Add new presets
            data.presets.forEach(preset => {
                const option = document.createElement('option');
                option.value = preset.prompt;
                option.textContent = preset.label;
                presetSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Failed to load presets:', error);
    }
}

// Load presets when page loads
document.addEventListener('DOMContentLoaded', loadPresets);

// ============================================================================
// HEALTH CHECK
// ============================================================================

async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('✅ Backend connected:', data);
    } catch (error) {
        console.warn('⚠️ Backend not reachable. Make sure server.py is running.');
    }
}

// Check health on load
checkBackendHealth();
