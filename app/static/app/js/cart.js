
var detail = document.getElementById('detail');
var  detail_text= detail.textContent;



function updateUserOrder(productvariant_id, action){
    console.log('user logged in, success da thay doi')
    var url = '/update_item/'
    fetch(url,{
        method : 'POST',
        headers : {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken

        },
        body: JSON.stringify({'productvariant_id':productvariant_id, 'action':action})
    })
    .then((response) =>{
        return response.json() 
    })
    .then((data)=>{
        console.log('data',data)
        location.reload()
    })
   
}

var urlParams = new URLSearchParams(window.location.search);
var productId = urlParams.get('id');
var baseUrl = '/static/'; 


$.get('../productvariant_api/', function(data) {
   
    var updateBtns=document.getElementsByClassName('update-cart')
    for (i=0;i< updateBtns.length;i++){
        updateBtns[i].addEventListener('click', function(){
            for (var i = 0; i < data.length; i++) {
                var size = $("input[name='size']:checked").val();
                var color = $("input[name='color']:checked").val();
               if (data[i].color == color && data[i].size == size && data[i].product== productId ) {
                var productvariant_id =data[i].id;
               }}
            
            var action = this.dataset.action
            console.log('productvariant_id',productvariant_id, 'action', action)
            console.log('user: ',user)
            if (user ==="AnonymousUser"){
                console.log('user not login')
            }
            else{
                updateUserOrder(productvariant_id,action)
            }
        })
    }



    $(document).ready(function() {
        function updateImage() {
            // Hàm này được gọi khi thay đổi radio size hoặc color
            
           
            for (var i = 0; i < data.length; i++) {
                var size = $("input[name='size']:checked").val();
                var color = $("input[name='color']:checked").val();
               
               if (data[i].color == color && data[i].size == size && data[i].product== productId ) {
                    $("#main-image").attr("src", data[i].ImageURL);
                    $("#shoeType").text(data[i].shoe_type);
                    $("#productName").text(data[i].name);
                    $("#productPrice").text(data[i].price+ "$");
                    $("#detail").text(detail_text);
                    break; 
                }
                else {
                    $("#main-image").attr("src",baseUrl + 'app/images/soldout.jpg');
                    $("#productPrice").text("0.00 $");
                    $("#detail").text("Vui lòng chọn sản phẩm khác!!");
                }
            }
        }

        // Gọi hàm khi radio size hoặc color thay đổi
        $("input[name='size']").change(updateImage);
        $("input[name='color']").change(updateImage);
    });
});