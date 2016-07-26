$("#add").click(function(){
    numRows = parseInt($(this).data("form-row-counter"));
    input = $('#copy-row').html();
    input = input.replace("desc-0", "desc-" + numRows);
    input = input.replace("date-0", "date-" + numRows);
    $(input).insertBefore($(this).parent().parent());
    $(this).data("form-row-counter", numRows + 1);
});
