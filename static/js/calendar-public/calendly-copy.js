document.addEventListener('DOMContentLoaded', function() {
  var buttons = document.querySelectorAll('.demo-button');

  buttons.forEach(function(button) {
    button.addEventListener('click', function() {
      alert('This would lead to the Calendly embed for ' + this.textContent);
    });
  });
});