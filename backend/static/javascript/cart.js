const URL = "http://127.0.0.1:8000/"
$(document).ready(function(){
    var itemObj = { };
    // add item in Cart.
    $("#addCart").click( (e)=>{
        const item_id = e.target.value; // e.target으로 해야 값을 출력한다.
                                        // $(this)로 하면 undifinded로 나온다.
        // const test = $(e.target).data("item");
        const item_qty = document.getElementById("inputQuantity").value;
        itemObj["item_id"]= item_id;
        itemObj["item_qty"]= item_qty;        
        // console.log("item :"+itemObj.item_id+" / qty : "+itemObj.item_qty);
        $.ajax({
            url:`${URL}`+"order/addCart/",
            data : itemObj,
            dataType:'json',
            success: function(res){
                popupAlert(res.data,'#pop-up-');
                $("span.carted_item").text(res.carted_item);
            }
        })
    });
    // remove cart from clicking x button.
    $(".remove_item").click( (e)=>{
        let remove_item = {};
        remove_item["item_id"] = document.getElementById(e.target.id).getAttribute("data-item");
        console.log(remove_item);
        $.ajax({
            url:`${URL}order/remove_item`,
            data: remove_item,
            dataType: 'json',
            success: function(res){
                location.reload();
            }
        });
    });
});
