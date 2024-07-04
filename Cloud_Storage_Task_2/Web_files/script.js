document.addEventListener('DOMContentLoaded', (event) => {
    loadFiles();
});

function toggleButtons(disabled) {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.disabled = disabled;
        if (disabled) {
            button.classList.add('disabled'); // Add disabled class for styling
        } else {
            button.classList.remove('disabled'); // Remove disabled class for styling
        }
    });
}

var host_IP = 'Enter Your Host IP'

function loadFiles() {
    toggleButtons(true); // Disable buttons while loading files
    fetch(`http://${host_IP}/list_files`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(files => {
            console.log('Files:', files); // Debugging log
            const fileList = document.getElementById('fileList');
            fileList.innerHTML = '';
            files.forEach(file => {
                const li = document.createElement('li');
                li.textContent = file.name;

                const downloadButton = document.createElement('button');
                downloadButton.textContent = 'Download';
                downloadButton.onclick = () => {
                    toggleButtons(true); // Disable buttons while downloading
                    downloadFile(file.name);
                };
                li.appendChild(downloadButton);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.onclick = () => {
                    toggleButtons(true); // Disable buttons while deleting
                    deleteFile(file.name);
                };
                li.appendChild(deleteButton);

                fileList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        })
        .finally(() => {
            toggleButtons(false); // Enable buttons after operation completes
        });
}

function uploadFile() {
    toggleButtons(true); // Disable buttons while uploading
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch(`http://${host_IP}/upload_file`, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                loadFiles();
            } else {
                alert('Failed to upload file');
            }
        }).finally(() => {
            toggleButtons(false); // Enable buttons after upload completes
        });
    } else {
        alert('Please select a file to upload');
        toggleButtons(false); // Enable buttons if no file selected
    }
}

function downloadFile(fileName) {
    window.location.href = `http://${host_IP}/download_file?filename=${fileName}`;
    toggleButtons(false); // Enable buttons after initiating download
}

function deleteFile(fileName) {
    fetch(`http://${host_IP}/delete_file?filename=${fileName}`, {
        method: 'DELETE'
    }).then(response => {
        if (response.ok) {
            loadFiles();
        } else {
            alert('Failed to delete file');
        }
    }).finally(() => {
        toggleButtons(false); // Enable buttons after delete completes
    });
}
