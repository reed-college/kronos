$(document).ready(function() {
    //initializing select2
    $("#stu-select").select2({
        placeholder: "Students"
    });
    $("#prof-select").select2({
        placeholder: "Professors"
    });
    //initializing fullCalendar
    $('#calendar').fullCalendar({
        defaultDate: startday,
        defaultView: 'agendaWeek',         
        weekends: false,
        allDaySlot: false,
        header: false,
        events: {
            url: '/eventsjson',
            data: function() { 
                return {
                    department: $('#department option:selected').text(),
                    division: $('#division option:selected').text()
                };
            }
        }
    });
});
$(document).on('change', 'select', function() {
    $('#calendar').fullCalendar( 'refetchEvents');
});
