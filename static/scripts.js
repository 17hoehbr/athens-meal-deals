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

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})