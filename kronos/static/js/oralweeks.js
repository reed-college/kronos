$("#add").click(function(){
    //this function adds a new oralweek
    numRows = parseInt($(this).data("form-row-counter"));
    input = $('#copy-row').html();
    input = input.replace("desc-0", "desc-" + numRows);
    input = input.replace("date-0", "date-" + numRows);
    input = input.replace("rm-0", "rm-" + numRows);
    $(input).insertBefore($(this).parent().parent());
    $(this).data("form-row-counter", numRows + 1);
    
    
    $(".rm-btn").click(function(){
        //this removes the corresponging oralweek
        $(this).parents(".row").remove();    
    });

});

$(document).ready(function(){
    $("#add").click();
});
