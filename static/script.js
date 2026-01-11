document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeBtn = document.getElementById('removeBtn');
    const predictBtn = document.getElementById('predictBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultTitle = document.getElementById('resultTitle');
    const statusIcon = document.getElementById('statusIcon');
    const resetBtn = document.getElementById('resetBtn');

    let currentFile = null;

    // --- Drag & Drop Handlers ---
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => uploadArea.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('dragover'), false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);
    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFiles);
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering uploadArea click
        resetUpload();
    });

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files: files } });
    }

    function handleFiles(e) {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            if (!file.type.startsWith('image/')) {
                alert('Please upload an image file.');
                return;
            }
            currentFile = file;
            showPreview(file);
        }
    }

    function showPreview(file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
            imagePreview.src = reader.result;
            previewContainer.style.display = 'block';
            document.querySelector('.upload-content').style.display = 'none';
            predictBtn.disabled = false;
            resultsSection.style.display = 'none'; // Hide previous results
        }
    }

    function resetUpload() {
        currentFile = null;
        fileInput.value = '';
        previewContainer.style.display = 'none';
        document.querySelector('.upload-content').style.display = 'flex';
        predictBtn.disabled = true;
        resultsSection.style.display = 'none';
    }

    // --- Prediction Logic ---
    predictBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        predictBtn.disabled = true;
        predictBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Prediction failed');

            const data = await response.json();
            displayResult(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis.');
        } finally {
            predictBtn.disabled = false;
            predictBtn.innerHTML = '<span>Analyze Scan</span><i class="fa-solid fa-arrow-right"></i>';
        }
    });

    function displayResult(data) {
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        const isMature = data.result.includes('Mature');
        
        resultTitle.textContent = data.result;
        statusIcon.innerHTML = isMature ? '<i class="fa-solid fa-triangle-exclamation"></i>' : '<i class="fa-solid fa-check-circle"></i>';
        statusIcon.className = 'status-icon ' + (isMature ? 'result-warning' : 'result-success');
        
        // Mock probability/confidence visualization since the backend only gives a binary string currently
        // If the backend is updated to return confidence, we would use that here.
        const probFill = document.getElementById('probFill');
        probFill.style.width = '0%';
        setTimeout(() => {
            probFill.style.width = '92%'; // Mock value
            probFill.style.background = isMature ? 'var(--warning-color)' : 'var(--success-color)';
        }, 100);
    }

    resetBtn.addEventListener('click', () => {
        resetUpload();
        resultsSection.style.display = 'none';
    });

    // Global function for sample images
    window.loadSample = async (imgUrl) => {
        try {
            const response = await fetch(imgUrl);
            const blob = await response.blob();
            const file = new File([blob], "sample.jpg", { type: "image/jpeg" });
            currentFile = file;
            showPreview(file);
        } catch (e) {
            console.error("Could not load sample", e);
        }
    }
});
