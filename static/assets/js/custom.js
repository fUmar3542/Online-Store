/*==================================================================================
    Custom JS (Any custom js code you want to apply should be defined here).
====================================================================================*/

// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    $(".category-div .btn.btn-fill-type").click(function(){
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

    $(".btn.btn-fill-type.update-a-product").click(function(){
        var id = this.id
        $.ajax({
            url: "/api/" + id
        }).done(function(arr){
              document.getElementById("id").value = arr[0];
              document.getElementById("name").value = arr[1];
              document.getElementById("price").value = arr[2];
              document.getElementById("brand").value = arr[3];
              document.getElementById("stock").value = arr[4];
              document.getElementById("discount").value = arr[5];
              document.getElementById("detail").value = arr[6];
        });
        $(".modal-window-container.fancy.update-product.window-show").css("display","block");
        $(".modal-window-container.fancy.update-product").addClass("window-show");
        $("body").addClass("modal-window-open");
    });

    $(".update-cart-btn.btn.btn-fill-type").click(function(){
        var objects = $(".product-quantity-list");
        var server_data = []
        var index = 0;
        for (var x of objects){
            server_data[index] = (x.value);
            index++;
        }
        $.ajax({
              type: "POST",
              url: "/update",
              data: JSON.stringify(server_data),
              contentType: "application/json",
              dataType: 'json',
              success: function(result) {
                console.log(result);
                location.reload();
              }
        });
    });

    const actualBtn = document.getElementById('actual-btn');
    const fileChosen = document.getElementById('file-chosen');
    actualBtn.addEventListener('change', function(){
    fileChosen.textContent = this.files[0].name;
    });
});


//        var a = 0
//        for (var obj of objects) {
//            if(obj.value > 1){
//                $.ajax({
//                    url: "/update-cart/" + a + "/" + obj.value,
//                }).done(function(arr){
//                    console.log("Done")
//                });
//            }
//            a++;
//        }
//        $.ajax({
//            url: "/cart-list"
//        }).done(function(arr){
//            console.log("Done")
//        });
