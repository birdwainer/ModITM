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
    classification: "car",
    imgSrc:
      "https://images.unsplash.com/photo-1502877338535-766e1452684a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2372&q=80",
  },
  {
    classification: "car",
    imgSrc:
      "https://images.unsplash.com/photo-1493238792000-8113da705763?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
  },
  {
    classification: "motorcycle",
    imgSrc:
      "https://images.unsplash.com/photo-1558981806-ec527fa84c39?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
  },
  {
    classification: "bus",
    imgSrc:
      "https://images.unsplash.com/photo-1562620669-98104534c6cd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80",
  },
  {
    classification: "car",
    imgSrc:
      "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2340&q=80",
  },
  {
    classification: "bridge",
    imgSrc:
      "https://images.unsplash.com/photo-1638567860967-4d5b82e9e126?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2662&q=80",
  },
  {
    classification: "stoplight",
    imgSrc:
      "https://images.unsplash.com/photo-1472070153210-15e27d938957?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2340&q=80",
  },
  {
    classification: "boat",
    imgSrc:
      "https://images.unsplash.com/photo-1605281317010-fe5ffe798166?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2288&q=80",
  },
  {
    classification: "stopsign",
    imgSrc:
      "https://images.unsplash.com/photo-1618737739013-aed8938604fb?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80",
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

function submitCaptcha() {
  const wrapper = document.querySelector(".captcha-wrap");
  setTimeout(function () {
    wrapper.style.visibility = "visible";
  }, 1500);
}
