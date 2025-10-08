// neue Kitchentype hinzufügen
function showInput() {
    var kitchenType = document.getElementById("kitchen-type").value;
    var customInput = document.getElementById("custom-kitchen-type");

    if (kitchenType === "sonst") {
      customInput.style.display = "block";
    } else {
      customInput.style.display = "none"; // Ansonsten bleibt es verborgen
    }
  }
// Halal und Alkohol können nicht gleichzeitig ausgewählt werden
document.querySelectorAll('input[name="product-category"]').forEach((checkbox) => {
  checkbox.addEventListener('change', function () {
      const alcoholCheckbox = document.querySelector('input[value="alcohol"]');
      const halalCheckbox = document.querySelector('input[value="halal"]');

      if (alcoholCheckbox.checked && halalCheckbox.checked) {
          // Falls beide gleichzeitig ausgewählt werden, zeige eine Warnung und deaktiviere die aktuelle Auswahl
          if (this.value === 'alcohol') {
              halalCheckbox.checked = false;
              alert('Sie können "Halal" und "Enthält Alkohol" nicht gleichzeitig auswählen.');
          } else if (this.value === 'halal') {
              alcoholCheckbox.checked = false;
              alert('Sie können "Halal" und "Enthält Alkohol" nicht gleichzeitig auswählen.');
          }
      }
  });
});

