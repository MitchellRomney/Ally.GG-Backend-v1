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

  $("#summoner-menu > .general").click(function() {
    $("#summoner-content-wrapper").attr("class","general");
    $("#summoner-menu > .selector").attr("class","selector");
    $("#summoner-menu").attr("class","");
  })
  $("#summoner-menu > .matches").click(function() {
    $("#summoner-content-wrapper").attr("class","matches");
    $("#summoner-menu > .selector").attr("class","selector s_matches");
    $("#summoner-menu").attr("class","s_matches");
  })
  $("#summoner-menu > .champions").click(function() {
    $("#summoner-content-wrapper").attr("class","champions");
    $("#summoner-menu > .selector").attr("class","selector s_champions");
    $("#summoner-menu").attr("class","s_champions");
  })
  $("#summoner-menu > .achievements").click(function() {
    $("#summoner-content-wrapper").attr("class","achievements");
    $("#summoner-menu > .selector").attr("class","selector s_achievements");
    $("#summoner-menu").attr("class","s_achievements");
  })
});
