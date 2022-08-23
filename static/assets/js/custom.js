/*==================================================================================
    Custom JS (Any custom js code you want to apply should be defined here).
====================================================================================*/

// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    $(".btn.btn-fill-type").click(function(){
      //alert("The paragraph was clicked.");
      $(".modal-window-container.fancy.sub-cat.window-show").css("display","block");
      $(".modal-window-container").addClass("window-show");
      $("body").addClass("modal-window-open");
    });
});

