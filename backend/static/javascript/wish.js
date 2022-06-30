
// Function to GET csrftoken from Cookie
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// var csrftoken = getCookie('csrftoken');



// fuction that change top,left css to top 20%, left: 50% on the current page position.
function popupCalc(section){
    // $(window).height() : current viewport height
    // $(window).width() : current viewport width
    // $(section).outerHeight() : section element height
    // $(section).outerWidth() : section element width
    // $(window).scrollTop() : window current scrollTop position
    // $(window).scrollLeft() : window current scrollLeft position
    /* referece : https://qjadud22.tistory.com/7
    // $("#popupDiv").css({
    //     "top": (($(window).height()-$("#popupDiv").outerHeight())/2+$(window).scrollTop())+"px",
    //     "left": (($(window).width()-$("#popupDiv").outerWidth())/2+$(window).scrollLeft())+"px"
    //     //팝업창을 가운데로 띄우기 위해 현재 화면의 가운데 값과 스크롤 값을 계산하여 팝업창 CSS 설정
    //  }); 
    */
    $(section).css({
        "top": (($(window).height()-$(section).outerHeight())/10+$(window).scrollTop())+"px",
        "left": (($(window).width())/2+$(window).scrollLeft())+"px"
    });
}

// Pop up alert function
const popupSection = ".pop-up-section";
const popupBox = ".pop-up-box";
var popupCount = 0;
function popupAlert(word){
    popupCalc(popupSection);
    popupCount++;
    let newPopup = document.createElement("div");
    newPopup.id = `pop-up-${popupCount}`;
    newPopup.classList.add("pop-up-box");
    newPopup.textContent = word;
    $(popupSection).append(newPopup);
    wait('#pop-up-',1500,popupCount);
}

// Async setTimeout function 
const wait = (section,timeToDelay,number) => 
    new Promise(()=>
        setTimeout( ()=>{
            $(section+number).remove();
        },timeToDelay));

$(document).ready(function(){
    // var wishObj = {};
    $(".addWish").click( function(e){
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let wishObj = {};
        const item_id = $(this).data('item');
        // const action = $(this).data('action');
        // wishObj['action'] = action;
        wishObj['item_id'] = item_id;
        console.log(e.target);
        $.ajax({
            url:`${URL}`+"order/manageWish/",
            type : 'POST',
            headers:{
                'X-CSRFToken': csrftoken,
            },
            data: wishObj,
            dataType: 'json',
            success: function(json){
                if(json.action=='add'){
                    popupAlert("Item was added");
                    $(`#wish-heart-${item_id}`).removeClass("bi-heart");
                    $(`#wish-heart-${item_id}`).addClass("bi bi-heart-fill");
                }else{
                    popupAlert("Item was removed");
                    $(`#wish-heart-${item_id}`).removeClass();
                    $(`#wish-heart-${item_id}`).addClass("bi bi-heart");
                }

            },
            error: function(err){
                console.log(err);
            }
        })
    });
    // when click the X button, remove wish item in wishList page.
    $(".remove_wish_item").click( function(e){
        let wishObj = {};
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const item_id = $(this).data('item');
        wishObj['item_id']= item_id;
        $.ajax({
            url:`${URL}`+"order/manageWish/",
            type : 'POST',
            headers:{
                'X-CSRFToken': csrftoken,
            },
            data: wishObj,
            dataType: 'json',
            success: function(json){
                location.reload();
            },
            error: function(err){
                console.log(err);
            }
        });
    });
});