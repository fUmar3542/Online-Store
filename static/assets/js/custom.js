/*==================================================================================
    Custom JS (Any custom js code you want to apply should be defined here).
====================================================================================*/

// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    $(".category-div .btn.btn-fill-type").click(function(){
      //alert("The paragraph was clicked.");
      $(".modal-window-container.fancy.sub-cat.window-show").css("display","block");
      $(".modal-window-container.fancy.sub-cat").addClass("window-show");
      $("body").addClass("modal-window-open");
    });

    $(".btn.btn-fill-type.add-a-product").click(function(){
      //alert("The paragraph was clicked.");
      $(".modal-window-container.fancy.view-product.window-show").css("display","block");
      $(".modal-window-container.fancy.view-product").addClass("window-show");
      $("body").addClass("modal-window-open");
    });

});

const actualBtn = document.getElementById('actual-btn');
const fileChosen = document.getElementById('file-chosen');
actualBtn.addEventListener('change', function(){
  fileChosen.textContent = this.files[0].name
})
