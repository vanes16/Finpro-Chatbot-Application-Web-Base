const textarea = document.querySelector(".chatbox-message-input");
const chatboxForm = document.querySelector(".chatbox-message-form");

const chatboxToggle = document.querySelector(".chatbox-toggle");
const chatboxMessage = document.querySelector(".chatbox-message-wrapper");
const dropdownToggle = document.querySelector(
  ".chatbox-message-dropdown-toggle"
);
const dropdownMenu = document.querySelector(".chatbox-message-dropdown-menu");

const msgerChat = get("#chatbox-message-content");
const getUser = document.querySelector(".nameText").innerText;
const botprofile =
  "data:image/png;base64,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";
const botname = "Jo Bot";
const userprofile =
  "data:image/png;base64,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";
const username = getUser.replace("Hello, ", "");
const submitMessage = document.querySelector(".chatbox-message-button");

var date = new Date();
var getTime = date.toLocaleTimeString();

chatboxToggle.addEventListener("click", function () {
  dropdownMenu.classList.remove("show");
  chatboxMessage.classList.toggle("show");
});

dropdownToggle.addEventListener("click", function () {
  dropdownMenu.classList.toggle("show");
});

document.addEventListener("click", function (e) {
  if (
    !e.target.matches(".chatbox-message-dropdown, .chatbox-message-dropdown *")
  ) {
    dropdownMenu.classList.remove("show");
  }
});

function msgTemplate(name, img, side, text) {
  const msgHTML = `
<div class="chatbox-message-response ${side}-message">
  <div class="chatbox-message-response-image " style="background-image: url(${img})"></div>
  <div class="chatbox-message-bubble ">
    <div class="chatbox-message-info">
      <div class="chatbox-message-info-name">${name}</div>
      <div class="chatbox-message-info-time">${getTime}</div>
    </div>
    <div class="chatbox-message-text">${text}</div>
  </div>
</div>
`;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 400;
}

function get(selector, root = document) {
  return root.querySelector(selector);
}

function botResponse(userResponse) {
  $.get("/bot-resp", { userInput: userResponse }).done(function (data) {
    msgTemplate(botname, botprofile, "left", data);
  });
}

submitMessage.addEventListener("click", function (event) {
  event.preventDefault();

  const msgText = textarea.value;
  if (!msgText) return;
  msgTemplate(username, userprofile, "right", msgText);
  textarea.value = "";
  botResponse(msgText);
});

chatboxForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const msgText = textarea.value;
  if (!msgText) return;
  msgTemplate(username, userprofile, "right", msgText);
  textarea.value = "";
  botResponse(msgText);
});

const switchMode = document.getElementById("switch-mode");
switchMode.addEventListener("change", function () {
  if (this.checked) {
    document.body.classList.add("dark");
    const mode = "Dark";
    const sendData = JSON.stringify(mode);
    $.ajax({
      url: "/get-darkmode",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(sendData),
    });
  } else {
    document.body.classList.remove("dark");
    const mode = "Light";
    const sendData = JSON.stringify(mode);
    $.ajax({
      url: "/get-darkmode",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(sendData),
    });
  }
});

function get(selector, root = document) {
  return root.querySelector(selector);
}
$.get("/send-darkmode").done(function (data) {
  if (data == "Dark") {
    document.body.classList.add("dark");
    switchMode.checked = true;
  } else if (data == "Light") {
    document.body.classList.remove("dark");
    switchMode.checked = false;
  }
});

const myslide = document.querySelectorAll(".myslide");
let counter = 1;
slider(counter);

let timer = setInterval(autoSlide, 8000);
function autoSlide() {
  counter += 1;
  slider(counter);
}
function plusSlides(n) {
  counter += n;
  slider(counter);
  resetTimer();
}
function resetTimer() {
  clearInterval(timer);
  timer = setInterval(autoSlide, 8000);
}

function slider(n) {
  let i;
  for (i = 0; i < myslide.length; i++) {
    myslide[i].style.display = "none";
  }
  if (n > myslide.length) {
    counter = 1;
  }
  if (n < 1) {
    counter = myslide.length;
  }
  myslide[counter - 1].style.display = "block";
}
// End Home Section
