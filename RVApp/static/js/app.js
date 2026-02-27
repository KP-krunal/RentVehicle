const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");

inputs.forEach((inp) => {
  inp.addEventListener("focus", () => {
    inp.classList.add("active");
  });
  inp.addEventListener("blur", () => {
    if (inp.value != "") return;
    inp.classList.remove("active");
  });
});

toggle_btn.forEach((btn) => {
  btn.addEventListener("click", () => {
    main.classList.toggle("sign-up-mode");
  });
});

function moveSlider() {
  let index = this.dataset.value;

  let currentImage = document.querySelector(`.img-${index}`);
  images.forEach((img) => img.classList.remove("show"));
  currentImage.classList.add("show");

  const textSlider = document.querySelector(".text-group");
  textSlider.style.transform = `translateY(${-(index - 1) * 2.2}rem)`;

  bullets.forEach((bull) => bull.classList.remove("active"));
  this.classList.add("active");
}

bullets.forEach((bullet) => {
  bullet.addEventListener("click", moveSlider);
});


document.addEventListener('DOMContentLoaded', () => {
  // Get references to elements
  const selectRole = document.getElementById('selectRole');
  const customerFields = document.getElementById('customer-fields');
  const employeeFields = document.getElementById('employee-fields');

  // Event listener for dropdown change
  selectRole.addEventListener('change', () => {
    const selectedValue = selectRole.value;

    if (selectedValue === 'user') {
      // Show customer fields, hide employee fields
      customerFields.classList.remove('hidden');
      employeeFields.classList.add('hidden');
    } else if (selectedValue === 'emp') {
      // Show employee fields, hide customer fields
      employeeFields.classList.remove('hidden');
      customerFields.classList.add('hidden');
    }
  });
});
