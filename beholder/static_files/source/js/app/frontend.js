// Âncoras Suaves
$(".navbar a").on("click", function(event){
    var ancora = $(this).attr("href");
    console.log(ancora);
    //return false;
    if (ancora[0] == '#'){
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $(ancora).offset().top+5
        }, 1000);
    }
    $(".navbar-collapse").removeClass("in");
});
