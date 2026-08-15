/* ==================================
   Form - Custom Category
   ================================== */

document.addEventListener('DOMContentLoaded', () => {
  const customSelect = document.querySelector('.custom-select');
  const selectButton = document.querySelector('.custom-select-button');
  const selectedCategory = document.querySelector('.selected-category');
  const options = document.querySelectorAll('.custom-option');

  const categorySelect = document.querySelector('#id_category');
  const customCategoryInput = document.querySelector('.custom-category-input');
  const customCategory = document.querySelector('#custom-category');

  selectButton.addEventListener('click', () => {
    customSelect.classList.toggle('open');
  });

  options.forEach((option) => {
    option.addEventListener('click', () => {
      const value = option.dataset.value;
      const text = option.textContent.trim();

      if (value === 'custom') {
        selectedCategory.textContent = 'Custom category';

        customCategoryInput.style.display = 'block';
        customCategory.focus();

        categorySelect.value = '';
      } else {
        selectedCategory.textContent = text;

        customCategoryInput.style.display = 'none';
        customCategory.value = '';

        categorySelect.value = value;
      }

      customSelect.classList.remove('open');
    });
  });

  document.addEventListener('click', (event) => {
    if (!customSelect.contains(event.target)) {
      customSelect.classList.remove('open');
    }
  });
  
  const currentCategoryValue = categorySelect.value;

  if (currentCategoryValue) {
    const match = document.querySelector(
      `.custom-option[data-value="${currentCategoryValue}"]`
    );
    if (match) {
      selectedCategory.textContent = match.textContent.trim();
    }
  } else if (customCategory.value.trim()) {
    selectedCategory.textContent = 'Custom category';
    customCategoryInput.style.display = 'block';
  }
});

/* ==================================
   Form - Custom Color
   ================================== */

document.addEventListener('DOMContentLoaded', () => {
  const colorField = document.querySelector('#id_color');
  const colorOptions = document.querySelectorAll('.color-option');
  const customColorPicker = document.querySelector('#custom-color-picker');
  const customColorCircle = document.querySelector('.custom-color-circle');

  if (!colorField) {
    return;
  }

  colorOptions.forEach((option) => {
    option.addEventListener('click', () => {
      const color = option.dataset.color;

      colorField.value = color;

      colorOptions.forEach((item) => {
        item.classList.remove('selected');
      });

      option.classList.add('selected');

      customColorCircle.style.background = '';
      customColorCircle.style.boxShadow = '';
    });
  });

  customColorPicker.addEventListener('input', () => {
    const color = customColorPicker.value;

    colorField.value = color;

    customColorCircle.style.background = color;
    customColorCircle.style.borderColor = '#efefef';
    customColorCircle.style.boxShadow = `0 0 0 2px ${color}`;

    colorOptions.forEach((item) => {
      item.classList.remove('selected');
    });    
  });

  const currentColorValue = colorField.value;

  if (currentColorValue) {
    const match = document.querySelector(
      `.color-option[data-color="${currentColorValue}"]`
    );

    if (match) {
      match.classList.add('selected');
    } else {
      customColorPicker.value = currentColorValue;
      customColorCircle.style.background = currentColorValue;
      customColorCircle.style.borderColor = '#efefef';
      customColorCircle.style.boxShadow = `0 0 0 2px ${currentColorValue}`;
    }
  }

});

/* ==================================
   Form - Time Interval
   ================================== */

document.addEventListener('DOMContentLoaded', () => {
  const picker = document.querySelector('#interval-picker');

  if (!picker) {
    return;
  }

  const options = picker.querySelectorAll('.interval-option');
  const optionsContainer = picker.querySelector('.interval-options');
  const djangoField = document.querySelector('#id_notification_interval');

  const optionHeight = 40;

  function selectOption(option) {
    const value = option.dataset.value;

    djangoField.value = value;

    options.forEach((item) => {
      item.classList.remove('selected');
    });

    option.classList.add('selected');
  }

  options.forEach((option) => {
    option.addEventListener('click', () => {
      option.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });

      selectOption(option);
    });
  });

  optionsContainer.addEventListener('scroll', () => {
    const scrollTop = optionsContainer.scrollTop;

    const index = Math.round(scrollTop / optionHeight);

    const option = options[index];

    if (option) {
      selectOption(option);
    }
  });

  const currentValue = djangoField.value || '0';

  const defaultOption = picker.querySelector(`[data-value="${currentValue}"]`);

  if (defaultOption) {
    defaultOption.classList.add('selected');

    defaultOption.scrollIntoView({
      block: 'center',
    });
  }
});

/* ==================================
   Form - Icon
   ================================== */

document.addEventListener("DOMContentLoaded", () => {
  const iconToggle = document.getElementById("icon-toggle-checkbox");
  const iconPicker = document.getElementById("icon-picker");
  const iconField = document.getElementById("id_icon");
  const customEmojiInput = document.getElementById("custom-emoji-input");
  const emojiPopup = document.getElementById("emoji-popup");
  const emojiPopupGrid = document.getElementById("emoji-popup-grid");
  const emojiSearch = document.getElementById("emoji-search");

  const EMOJI_LIST = [
    "🏃", "🏃‍♀️", "🏃‍♂️", "🚶", "🚶‍♀️", "🚶‍♂️", "🏋️", "🏋️‍♀️", "🏋️‍♂️", "🤸", "🧘", "🚴", "🚴‍♀️", "🚴‍♂️", "🏊", "🏊‍♀️", "🏊‍♂️", "⚽", "🏀", "🏐", "🎾",
    "💧", "🥤", "🍎", "🍏", "🥑", "🥦", "🥕", "🍌", "🍊", "🥗", "🥛", "💊", "🦷", "🛌", "😴", "🧴", "🧼", "🛁",
    "📚", "📖", "✏️", "📝", "🖊️", "📓", "📔", "💻", "🖥️", "⌨️", "🧠", "💡", "🎓", "🔬", "📐", "📅", "⏰", "⏱️", "🎯",
    "🎨", "🖌️", "🖍️", "🧶", "🧵", "🪡", "🧩", "🎸", "🎹", "🎵", "🎶", "🎤", "📷", "📸", "🎬", "🎭", "✍️", "🖋️",
    "🧘‍♀️", "🧘‍♂️", "🌿", "🌱", "🌸", "🌺", "🌻", "☀️", "🌙", "⭐", "🕯️", "❤️", "🫶", "😊", "😌", "🧖", "🧖‍♀️", "🧖‍♂️",
    "🧹", "🧽", "🧺", "🛒", "🍳", "🍽️", "☕", "🫖", "🪴", "🛏️", "🚿", "👕", "🗑️", "🔑",
    "💰", "💵", "💳", "🪙", "🏦", "📈", "📊", "💸", "🐷", "🏆", "🥇", "🥈", "🥉",
    "🌳", "🌞", "🔥", "✨", "🚀", "🦋", "🌈", "💪",
  ];

  function renderEmojiGrid(filter = "") {
    emojiPopupGrid.innerHTML = "";
    EMOJI_LIST.filter((e) => !filter || e.includes(filter)).forEach((emoji) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "emoji-popup-option";
      btn.textContent = emoji;
      btn.dataset.emoji = emoji;
      emojiPopupGrid.appendChild(btn);
    });
  }

  renderEmojiGrid();

  iconToggle?.addEventListener("change", () => {
    iconPicker.hidden = !iconToggle.checked;
    if (!iconToggle.checked) {
      iconField.value = "";
      customEmojiInput.value = "";
      emojiPopup.hidden = true;
      document
        .querySelectorAll(".emoji-option.selected")
        .forEach((el) => el.classList.remove("selected"));
    }
  });

  document.querySelectorAll(".emoji-option").forEach((btn) => {
    btn.addEventListener("click", () => {
      document
        .querySelectorAll(".emoji-option.selected")
        .forEach((el) => el.classList.remove("selected"));
      btn.classList.add("selected");
      iconField.value = btn.dataset.emoji;
      customEmojiInput.value = btn.dataset.emoji;
    });
  });

  customEmojiInput?.addEventListener("click", () => {
    emojiPopup.hidden = false;
    emojiSearch.value = "";
    renderEmojiGrid();
    emojiSearch.focus();
  });

  emojiSearch?.addEventListener("input", () => {
    renderEmojiGrid(emojiSearch.value);
  });

  emojiPopupGrid?.addEventListener("click", (e) => {
    const btn = e.target.closest(".emoji-popup-option");
    if (!btn) return;

    document
      .querySelectorAll(".emoji-option.selected")
      .forEach((el) => el.classList.remove("selected"));

    iconField.value = btn.dataset.emoji;
    customEmojiInput.value = btn.dataset.emoji;
    emojiPopup.hidden = true;
  });

  document.addEventListener("click", (e) => {
    if (
      emojiPopup &&
      !emojiPopup.hidden &&
      !emojiPopup.contains(e.target) &&
      e.target !== customEmojiInput
    ) {
      emojiPopup.hidden = true;
    }
  });
});