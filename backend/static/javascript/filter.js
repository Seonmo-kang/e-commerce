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
            }
        })
    });
    
});