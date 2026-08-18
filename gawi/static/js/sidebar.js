/* ==================================
   Dashboard - Side Bar
   ================================== */

$('.menu > .menu-box > ul > li').click(function () {
  $(this).toggleClass('open');

  $(this).closest('li').find('.sub-menu').stop(true, true).slideToggle(200);
});

$('.menu-btn').click(function () {
  $('.sidebar').toggleClass('active');

  setTimeout(() => {
    $('.sidebar').toggleClass('collapsed');
  }, 300);
});

$(function () {
  $('.mode-btn').click(function () {
    $('html').toggleClass('transitioning');

    setTimeout(() => {
      $('html').toggleClass('dark');
      localStorage.setItem('theme', $('html').hasClass('dark') ? 'dark' : 'light');
      updateChartTheme();
      $('html').removeClass('transitioning');
    }, 150);
  });
});
