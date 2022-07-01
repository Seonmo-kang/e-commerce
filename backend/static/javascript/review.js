window.onload = function(){
    $('span.review-star').each( function(index){
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