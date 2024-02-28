// 获取按钮元素
let helloButton = document.getElementById('helloButton');
let userSwitch = document.getElementById('userSwitch');
let myHeading = document.querySelector("h1");


function setUserName() {
  let myName = prompt("请输入你的名字。");
  if (!myName) {
    setUserName();
  } else {
    localStorage.setItem("name", myName);
    myHeading.textContent = "Welcome to my site，" + myName;
  }
}


if (!localStorage.getItem("name")) {
  setUserName();
} else {
  let storedName = localStorage.getItem("name");
  myHeading.textContent = "Welcome to my site，" + storedName;
}


function previewPDF() {
  const fileInput = document.getElementById('pdf-upload');
  const pdfPreview = document.getElementById('pdf-preview');

  if (fileInput.files.length === 0) {
      alert("Please select a PDF file to upload.");
      return;
  }

  const file = fileInput.files[0];
  if(file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
  }

  // Use FileReader to read file
  const fileReader = new FileReader();

  fileReader.onload = function() {
      pdfPreview.src = fileReader.result;
      pdfPreview.hidden = false;
  };

  fileReader.readAsDataURL(file);
}



// 添加点击事件监听器
helloButton.addEventListener('click', function() {
  // 显示 "Hello, world!" 消息
  alert('Hello, world!');
});

userSwitch.addEventListener('click', function() {
  setUserName();
});
