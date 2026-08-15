$(function () {
  const $fileInput = $('#id_profile_picture');
  const $preview = $('#avatar-preview');
  const $dropZone = $('#drop-zone');

  function previewFile(file) {
    if (!file || !file.type.startsWith('image/')) return;

    const reader = new FileReader();
    reader.onload = function (e) {
      $preview.attr('src', e.target.result);
    };
    reader.readAsDataURL(file);
  }

  $fileInput.on('change', function () {
    previewFile(this.files[0]);
  });

  $dropZone.on('dragover', function (e) {
    e.preventDefault();
    $(this).addClass('dragover');
  });

  $dropZone.on('dragleave', function () {
    $(this).removeClass('dragover');
  });

  $dropZone.on('drop', function (e) {
    e.preventDefault();
    $(this).removeClass('dragover');

    const files = e.originalEvent.dataTransfer.files;
    if (files && files.length) {
      $fileInput[0].files = files;
      previewFile(files[0]);
    }
  });
});
