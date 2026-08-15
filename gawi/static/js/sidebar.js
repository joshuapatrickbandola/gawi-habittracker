/* ==================================
   Dashboard - Side Bar
   ================================== */

$('.menu > ul > li').click(function () {
  $(this).toggleClass('open');

  $(this).closest('li').find('.sub-menu').stop(true, true).slideToggle(200);
});

$('.menu-btn').click(function () {
  $('.sidebar').toggleClass('active');

  setTimeout(() => {
    $('.sidebar').toggleClass('collapsed');
  }, 300);
});
