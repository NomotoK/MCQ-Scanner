function uploadAndPreviewPDF() {
    const fileInput = document.getElementById('pdf-upload');
    const pdfPreview = document.getElementById('pdf-preview');

    if (fileInput.files.length === 0) {
        alert("Please select one or more PDF files to upload.");
        return;
    }

    // 预览第一个 PDF 文件
    const firstFile = fileInput.files[0];
    if (firstFile.type !== "application/pdf") {
        alert("Only PDF files are allowed.");
        return;
    }

    // 使用 FileReader 预览第一个 PDF 文件
    const fileReader = new FileReader();
    fileReader.onload = function() {
        pdfPreview.src = fileReader.result;
        pdfPreview.style.display = 'block'; // 显示预览
    };
    fileReader.readAsDataURL(firstFile);

    // 创建 FormData 对象并为每个选中的文件添加条目
    const formData = new FormData();
    Array.from(fileInput.files).forEach((file, index) => {
        if(file.type === "application/pdf") {
            formData.append('files[]', file, file.name);
        }
    });

    // 异步发送文件到服务器
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            alert('Files uploaded successfully');
        } else {
            throw new Error('File upload failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




function uploadCSV() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("No file selected.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_csv', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            alert('CSV uploaded successfully');
        } else {
            throw new Error('CSV upload failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading file');
    });
}



function uploadStudentInfo() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("No file selected.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_student_info', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            alert('CSV uploaded successfully');
        } else {
            throw new Error('CSV upload failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading file');
    });
}





document.addEventListener('DOMContentLoaded', function() {
    const dragArea = document.getElementById('drag-area');

    // 当文件被拖拽到区域上方时
    dragArea.addEventListener('dragover', function(event) {
        event.preventDefault();  // 阻止默认行为
        this.classList.add('drag-over');  // 添加背景变深的效果
    });

    // 当文件离开拖拽区域时
    dragArea.addEventListener('dragleave', function(event) {
        this.classList.remove('drag-over');  // 移除背景变深的效果
    });

    // 当文件被放置到拖拽区域时
    dragArea.addEventListener('drop', function(event) {
        event.preventDefault();  // 阻止默认行为
        this.classList.remove('drag-over');  // 放置文件后，移除背景变深的效果

        const file = event.dataTransfer.files[0];  // 获取拖拽的文件

        // 检查文件类型
        if (file.type !== "application/pdf") {
            alert("Please drop a PDF file.");
            return;
        }

        // 使用 FormData 封装文件，以便发送
        const formData = new FormData();
        formData.append('file', file);

        // 使用 fetch API 异步发送文件到服务器
        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                alert('File uploaded successfully');
                // 这里可以添加更多成功上传后的处理逻辑
            } else {
                throw new Error('File upload failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});




function scanAnswer() {
    document.getElementById('progressContainer').style.display = 'block';
    let progress = 0;
    const progressBar = document.getElementById('progressBar');

    const interval = setInterval(function() {
        progress += 1; // 快速更新时适当调整每次增加的百分比
        progressBar.style.width = progress + '%';
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 100); // 每0.1秒更新一次

    fetch('/analyse_mcq', { method: 'POST' })
    .then(response => {
        if (!response.ok) {
            throw new Error('Files missing or analysis failed');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        document.querySelector('.container-view-results').style.display = 'block'; // 显示“view results”按钮
        window.location.href = '/download_scores';
        clearInterval(interval);
        progressBar.style.width = '100%';
        setTimeout(function() {
            document.getElementById('progressContainer').style.display = 'none';
            progressBar.style.width = '0%';
        }, 2000);
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
        clearInterval(interval);
        document.getElementById('progressContainer').style.display = 'none';
    });
}


function viewResults() {
    // 跳转到显示结果的新页面
    window.location.href = '/results';
}



function sendEmail() {
    fetch('/send_email', { method: 'POST' })
    .then(response => {
        if (!response.ok) {
            // 如果响应状态码不是 2xx，抛出错误
            throw new Error('Failed to send email');
        }
        return response.json();
    })
    .then(data => {
        alert('Email Sent Successfully!');  // 显示成功消息
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error sending email');  // 弹窗显示错误消息
    });
}




