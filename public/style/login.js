function changeToRegister() {
  const changeToRegisterBtn = document.querySelector("#changeToRegister");
  const loginForm = document.querySelector("#login");
  const registerForm = document.querySelector("#register");
  changeToRegisterBtn.addEventListener("click", () => {
    loginForm.classList.remove("active");
    registerForm.classList.add("active");
  });
}
function changeToLogin() {
  const changeToLoginBtn = document.querySelector("#changeToLogin");
  const loginForm = document.querySelector("#login");
  const registerForm = document.querySelector("#register");
  changeToLoginBtn.addEventListener("click", () => {
    loginForm.classList.add("active");
    registerForm.classList.remove("active");
  });
}
changeToRegister();
changeToLogin();

const responseText = document.querySelector(".response-text").innerText;
const loginForm = document.querySelector("#login");
const registerForm = document.querySelector("#register");

if (responseText == "User Already Exists") {
  document.querySelector(".response-text").style.backgroundColor = "#FA3E3E";
  loginForm.classList.remove("active");
  registerForm.classList.add("active");
} else if (responseText == "Username Or Password Is Incorrect") {
  document.querySelector(".response-text").style.backgroundColor = "#FA3E3E";
} else if (responseText == "Invalid Link To Change Password") {
  document.querySelector(".response-text").style.backgroundColor = "#FA3E3E";
} else if (responseText == "Check Your Email") {
  document.querySelector(".response-text").style.backgroundColor = "#0A6522";
} else if (responseText == "Invalid Username") {
  document.querySelector(".response-text").style.backgroundColor = "#FA3E3E";
} else if (responseText == "Email Already Exists") {
  document.querySelector(".response-text").style.backgroundColor = "#FA3E3E";
}
