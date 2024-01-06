
var urlParams = new URLSearchParams(window.location.search);
var productId = urlParams.get('id');
var baseUrl = '/static/'; 


$.get('../productvariant_api/', function(data) {
    $(document).ready(function() {
        function updateImage() {
            // Hàm này được gọi khi thay đổi radio size hoặc color
            
            var size = $("input[name='size']:checked").val();
            var color = $("input[name='color']:checked").val();
            for (var i = 0; i < data.length; i++) {
               
               if (data[i].color == color && data[i].size == size && data[i].product== productId ) {
                    $("#main-image").attr("src", data[i].ImageURL);
                    $("#shoeType").text(data[i].shoe_type);
                    $("#productName").text(data[i].name);
                    $("#productPrice").text(data[i].price+ "$");
                    break; 
                }
                else {
                    $("#main-image").attr("src",baseUrl + 'app/images/soldout.jpg');
                    $("#productPrice").text("0.00 $");
                }
            }
        }

        // Gọi hàm khi radio size hoặc color thay đổi
        $("input[name='size']").change(updateImage);
        $("input[name='color']").change(updateImage);
    });
});
