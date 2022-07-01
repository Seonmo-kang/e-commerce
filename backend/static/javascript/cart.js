const URL = "http://127.0.0.1:8000/"
$(document).ready(function(){
    // add item in Cart.
    $(".addCart").click( function(e){

        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let itemObj = { "item_qty":1 };
        const item_id = $(this).data('item'); // e.target으로 해야 값을 출력한다.
                                        // $(this)로 하면 undifinded로 나온다.
        // const test = $(e.target).data("item");

        itemObj["item_id"]= item_id; 
        if($("#inputQuantity").length>0){
            itemObj["item_qty"] = $("#inputQuantity").val(); // get value : Using  jquery val() 
        }
        // console.log("item :"+itemObj.item_id+" / qty : "+itemObj.item_qty);
        $.ajax({
            url:`${URL}`+"order/addCart/",
            type: 'POST',
            headers:{
                'X-CSRFToken': csrftoken
            },
            data : itemObj,
            dataType:'json',
            success: function(res){
                popupAlert(res.data,'#pop-up-');
                $("span.carted_item").text(res.carted_item);
            },
            error: function(err){
                console.log(err);
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
            },
            error: function(err){
                console.log(err);
            }
        });
    });
});
