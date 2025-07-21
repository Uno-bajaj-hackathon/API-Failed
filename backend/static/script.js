const form = document.getElementById('queryForm');
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('files');
const fileList = document.getElementById('file-list');
const browseSpan = document.getElementById('browse');
const resultsDiv = document.getElementById('results');
const downloadJson = document.getElementById('downloadJson');
const downloadPdf = document.getElementById('downloadPdf');
const llmSelect = document.getElementById('llm-select');
let latestResults = null;
let dt = new DataTransfer();

// File drag & drop handling
['dragenter', 'dragover'].forEach(event => {
  dropArea.addEventListener(event, e => {
    e.preventDefault();
    dropArea.classList.add('highlight');
  });
});
['dragleave', 'drop'].forEach(event => {
  dropArea.addEventListener(event, e => {
    e.preventDefault();
    dropArea.classList.remove('highlight');
  });
});
dropArea.addEventListener('drop', e => {
  let files = e.dataTransfer.files;
  for (let i = 0; i < files.length; i++) {
    dt.items.add(files[i]);
  }
  fileInput.files = dt.files;
  updateFileList();
});

browseSpan.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
  for (let i = 0; i < fileInput.files.length; i++) {
    dt.items.add(fileInput.files[i]);
  }
  fileInput.files = dt.files;
  updateFileList();
});

function updateFileList() {
  fileList.innerHTML = '';
  for (let i = 0; i < fileInput.files.length; i++) {
    fileList.innerHTML += `<div>${fileInput.files[i].name}</div>`;
  }
}

form.onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('query', document.getElementById('query').value);
    formData.append('llm', llmSelect.value);
    for (let i = 0; i < fileInput.files.length; i++) {
      formData.append("files", fileInput.files[i]);
    }
    resultsDiv.innerHTML = 'Processing...';
    fetch('http://localhost:5000/query', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        latestResults = data.results;
        resultsDiv.innerHTML = '<pre>' + JSON.stringify(data.results, null, 2) + '</pre>';
        downloadJson.style.display = 'inline';
        downloadPdf.style.display = 'inline';
    }).catch(err => {
        resultsDiv.innerHTML = 'Error: ' + err.message;
    });
};

downloadJson.onclick = () => {
    if (!latestResults) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(latestResults, null, 2));
    const dl = document.createElement('a');
    dl.setAttribute("href", dataStr);
    dl.setAttribute("download", "report.json");
    document.body.appendChild(dl);
    dl.click();
    dl.remove();
};

downloadPdf.onclick = async () => {
    if (!latestResults) return;
    const res = await fetch('http://localhost:5000/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({results: latestResults, as_pdf: true})
    });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const dl = document.createElement('a');
    dl.href = url;
    dl.download = "report.pdf";
    document.body.appendChild(dl);
    dl.click();
    dl.remove();
};
