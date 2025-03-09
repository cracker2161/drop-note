
/**
 * Public Notepad App Utility Functions
 */

// Show status message
function showStatus(message, isError = false) {
    const statusMessage = document.getElementById('statusMessage');
    if (!statusMessage) return;
    
    statusMessage.innerHTML = message;
    statusMessage.className = 'status ' + (isError ? 'status-error' : 'status-success') + ' show';
    
    setTimeout(() => {
        statusMessage.classList.remove('show');
    }, 3000);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Get file icon based on extension
function getFileIcon(extension) {
    const icons = {
        '.txt': 'fa-file-alt',
        '.md': 'fa-file-alt',
        '.html': 'fa-file-code',
        '.css': 'fa-file-code',
        '.js': 'fa-file-code',
        '.json': 'fa-file-code',
        '.py': 'fa-file-code'
    };
    
    return icons[extension] || 'fa-file';
}

// Debounce function to limit how often a function can be called
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Get file extension
function getFileExtension(filename) {
    return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 1).toLowerCase();
}

// Format date string
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}
