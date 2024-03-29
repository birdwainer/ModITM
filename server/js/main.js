window.onload = function () {
  const form = document.querySelector("form");
  const checkboxes = form.querySelectorAll("input[type='checkbox']");
  const inputs = form.querySelectorAll(
    "input[type='text'], input[type='email'], textarea"
  );

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

function createCaptcha() {
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

  captcha.innerHTML = innerHTML;

  Array.from(document.querySelectorAll(".captcha-cell")).forEach((el) => {
    el.addEventListener("click", () => {
      el.classList.toggle("selected");
    });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  createCaptcha();
  const wrapper = document.querySelector(".captcha-wrap");
  wrapper.style.visibility = "hidden";
});

function startCaptcha() {
  const wrapper = document.querySelector(".captcha-wrap");
  setTimeout(function () {
    wrapper.style.visibility = "visible";
  }, 1500);
}

function submitCaptcha() {
  const wrapper = document.querySelector(".captcha-wrap");
  wrapper.style.visibility = "hidden";
  const inputs = document.querySelectorAll("input");
  inputs.forEach((input) => (input.disabled = true));
}

function refreshPage() {
  location.reload();
}
