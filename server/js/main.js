window.onload = function () {
  const form = document.querySelector("form");
  const checkboxes = form.querySelectorAll("input[type='checkbox']");
  const inputs = form.querySelectorAll(
    "input[type='text'], input[type='email'], textarea"
  );

  // Clear out the checkboxes and inputs on page load
  checkboxes.forEach((checkbox) => (checkbox.checked = false));
  inputs.forEach((input) => (input.value = ""));
};

const cellOptions = [
  {
    classification: "ship",
    imgSrc: "/image/1",
  },
  {
    classification: "ship",
    imgSrc: "/image/2",
  },
  {
    classification: "car",
    imgSrc: "/image/3",
  },
  {
    classification: "car",
    imgSrc: "/image/4",
  },
  {
    classification: "car",
    imgSrc: "/image/5",
  },
  {
    classification: "car",
    imgSrc: "/image/6",
  },
  {
    classification: "plane",
    imgSrc: "/image/7",
  },
  {
    classification: "plane",
    imgSrc: "/image/8",
  },
  {
    classification: "plane",
    imgSrc: "/image/9",
  },
];

function shuffle(array) {
  let currentIndex = array.length,
    randomIndex;
  while (currentIndex != 0) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex],
      array[currentIndex],
    ];
  }
  return array;
}

let shuffledOptions = [];
let humanPercent = 10;

// Create a captcha with randomized cells and classifications
function createCaptcha() {
  // Shuffle the cell options array to randomize the order of the cells
  shuffledOptions = shuffle(cellOptions);

  const captcha = document.querySelector("div.captcha");

  let innerHTML = "";
  for (var option of shuffledOptions) {
    innerHTML += `
    <div class="captcha-cell" data-classification="${option.classification}">
      <img src="${option.imgSrc}"  />
    </div>
    `;
  }

  // Add the shuffled cells to the captcha div
  captcha.innerHTML = innerHTML;

  // Loop through each cell and add an event listener for click events
  Array.from(document.querySelectorAll(".captcha-cell")).forEach((el) => {
    el.addEventListener("click", () => {
      el.classList.toggle("selected");
    });
  });
}

// Initialize the captcha on page load
document.addEventListener("DOMContentLoaded", function () {
  createCaptcha();
  const wrapper = document.querySelector(".captcha-wrap");
  wrapper.style.visibility = "hidden";
});

// Start the captcha after a delay of 1.5 seconds
function startCaptcha() {
  const wrapper = document.querySelector(".captcha-wrap");
  setTimeout(function () {
    wrapper.style.visibility = "visible";
  }, 1500);
}

// Submit the captcha form when the user clicks on the submit button
function submitCaptcha() {
  const wrapper = document.querySelector(".captcha-wrap");
  wrapper.style.visibility = "hidden";
  const inputs = document.querySelectorAll("input");
  inputs.forEach((input) => (input.disabled = true));
}

// Refresh the page when the user clicks on the refresh button
function refreshPage() {
  location.reload();
}
