$(document).ready(function () {
    
    var filterObj = {};
    $(".form-check-input").click(() => {
        $(".form-check-input").each(function() {
            var _filterVal = $(this).val();
            var _filterKey = $(this).data("filter");
            console.log(filterObj)
            filterObj[_filterKey]=Array.from(document.querySelectorAll(`input[data-filter="${_filterKey}"]:checked`)
            ).map((el)=>{
                return el.value;
            })

        })
        $.ajax({
            url:"filter-list/",
            data:filterObj,
            dataType:'json',
            success: function(res) {
                $(".itemlist").html(res.data);
                review_cal();
            }
        })
    });
    
});
// review image generated
function review_cal(){
    $('span.review-star').each( function(){
        var star_count = $(this).data('star');
        console.log($(this));
        if(isNaN(star_count)) star_count=0;
        console.log(Math.round(star_count));
        let element = document.createElement("i");
        element.classList.add("bi");
        element.classList.add("bi-star-fill");
        element.classList.add("text-warning");
        for(let i=0; i<Math.round(star_count); i++){
            // n the loop, in each iteration you need to create a new object,
            // else it will be just like replacing the same element so many times
            // So you can just clone() the element in the loop
            $(this).append(element.cloneNode());
        }
        element.classList.remove("bi-star-fill");
        element.classList.add("bi-star");
        for(let i=0; i<5-Math.round(star_count); i++){
            $(this).append(element.cloneNode());
        }
    });
}