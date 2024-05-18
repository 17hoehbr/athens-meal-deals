function checkAll(name) {
  let checkboxes = document.querySelectorAll(`input[type="checkbox"][name="${name}"]`);
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = true;
  }
}

function uncheckAll(name) {
  let checkboxes = document.querySelectorAll(`input[type="checkbox"][name="${name}"]`);
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = false;
  }
}

function resetFilter(name) {
  let checkboxes = document.querySelectorAll(`input[type="checkbox"]`);
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = true;
  }
}

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register("/sw.js").then(function(registration) {
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
      console.log('ServiceWorker registration failed: ', err);
    });
  });
}

const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];

const d = new Date();
let day = weekday[d.getDay()];

window.onload = function() {
  document.getElementById(day).scrollIntoView();
};