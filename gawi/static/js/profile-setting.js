/* ==================================
   Profile Setting - Progress Bar
   ================================== */

const progress = document.querySelector('.progress');

const targetWidth = progress.dataset.progress.trim();

const previousWidth = localStorage.getItem('progress') || '0';

progress.style.width = `${previousWidth}%`;

setTimeout(() => {
  progress.style.width = `${targetWidth}%`;
  localStorage.setItem('progress', targetWidth);

  setTimeout(() => {
    activeStep.classList.add('show');
  }, 500);
}, 50);

/* ==================================
   Profile Setting - Upload Image
   ================================== */

const dropZone = document.querySelector('.drop-zone');
const fileInput = document.querySelector('.file-input');
const preview = document.querySelector('.file-preview');

dropZone.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  showFile(fileInput.files[0]);
});

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragging');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('dragging');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();

  const file = e.dataTransfer.files[0];

  fileInput.files = e.dataTransfer.files;

  showFile(file);
});

function showFile(file) {
  if (!file) return;

  const reader = new FileReader();

  reader.onload = () => {
    preview.innerHTML = `
            <img src="${reader.result}">
        `;
  };

  reader.readAsDataURL(file);
}
