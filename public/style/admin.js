const menuBar = document.querySelector("#content nav .bx.bx-menu");
const sidebar = document.getElementById("sidebar");

menuBar.addEventListener("click", function () {
  sidebar.classList.toggle("hide");
});

window.addEventListener("resize", function () {
  if (this.innerWidth < 768) {
    sidebar.classList.add("hide");
  } else {
    sidebar.classList.remove("hide");
  }
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
