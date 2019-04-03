$(document).ready(function() {
  $(".sidebar-dropdown > a").click(function() {
    $(".sidebar-submenu").slideUp(200);
    if (
      $(this)
        .parent()
        .hasClass("active")
    ) {
      $(".sidebar-dropdown").removeClass("active");
      $(this)
        .parent()
        .removeClass("active");
    } else {
      $(".sidebar-dropdown").removeClass("active");
      $(this)
        .next(".sidebar-submenu")
        .slideDown(200);
      $(this)
        .parent()
        .addClass("active");
    }
  });

  $(".acc-options").on("click", function(e) {
    $(this).toggleClass("open");
    e.stopPropagation()
  });
  $(document).on("click", function(e) {
    if ($(e.target).is(".acc-options") === false) {
      $(".acc-options").removeClass("open");
    }
  });
});
