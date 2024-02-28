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
    myHeading.textContent = "Mozilla 酷毙了，" + myName;
  }
}



if (!localStorage.getItem("name")) {
  setUserName();
} else {
  let storedName = localStorage.getItem("name");
  myHeading.textContent = "Mozilla 酷毙了，" + storedName;
}


// 添加点击事件监听器
helloButton.addEventListener('click', function() {
  // 显示 "Hello, world!" 消息
  alert('Hello, world!');
});

userSwitch.addEventListener('click', function() {
  setUserName();
});
