function toggleDropdown() {
  const dropdown = document.getElementById("dropdown");
  dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

function selectItem(id, name) {
  const button = document.querySelector(".dropdown-btn");
  button.textContent = name
  document.getElementById("selected_list").value = id; // Записываем выбранный список в скрытое поле
  toggleDropdown(); // Закрыть меню
}