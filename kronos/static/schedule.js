$(document).ready(function() {
    //initializing select2
    $("#stu-select").select2({
        placeholder: "Students",
        allowClear: true
    });
    $("#prof-select").select2({
        placeholder: "Professors",
        allowClear: true
    });
    //initializing fullCalendar
    $('#calendar').fullCalendar({
        defaultDate: startday,
        defaultView: 'agendaWeek',         
        weekends: false,
        allDaySlot: false,
        header: false,
        slotEventOverlap: false,
        events: {
            url: '/eventsjson',
            data: function() { 
                return {
                    department: $('#department option:selected').text(),
                    division: $('#division option:selected').text(),
                    'professors[]': $('#prof-select').val(),
                    'students[]': $('#stu-select').val()
                };
            }
        },
        eventRender: function(event, element, view) {
            $(element).attr('tabindex', '0');
            $(element).attr('data-toggle', 'popover');
            $(element).attr('title', event.title);
            $(element).attr('data-trigger', 'focus');
            $(element).attr('data-container', 'body');
            var content = "<div>";
            if (event.type == "oral") {
                content += "<b>" + event.student + "</b>\n";
                for (let reader of event.readers){
                    content += reader + "\n";
                }
            }
            content += "</div>"
            $(element).attr('data-content', content)
            $(element).popover({html : true});
        }
    });
});
$(document).on('change', 'select', function() {
    $('#calendar').fullCalendar( 'refetchEvents');
});
