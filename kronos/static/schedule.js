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
       events: '/eventsjson',
       defaultView: 'agendaWeek',         
       weekends: false,
       allDaySlot: false,
       header: false,
    });
});
