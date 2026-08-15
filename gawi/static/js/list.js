/* ==================================
   Habit List - Checkboxes
   ================================== */

document.querySelectorAll('.habit-checkbox').forEach((checkbox) => {
  checkbox.addEventListener('change', async () => {
    const url = checkbox.dataset.url;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
    });

    const data = await response.json();

    const habitCard = checkbox.closest('.habit-card');
    const days = habitCard.querySelectorAll('.tracker-day:not(.empty)');
    const todayCell = days[days.length - 1];

    if (todayCell) {
      todayCell.classList.toggle('completed', data.completed);
    }
  });
});

/* ==================================
   Habit List - Scroll Max Left
   ================================== */

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tracker-grid').forEach((grid) => {
    grid.scrollLeft = grid.scrollWidth;
  });
});
