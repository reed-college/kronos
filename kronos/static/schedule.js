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
            $(element).attr('name','event-popover');
            $(element).attr('tabindex', '0');
            $(element).attr('data-toggle', 'popover');
            $(element).attr('title', event.title);
            //change this back to 'focus' when you're done with popover inspecting
            $(element).attr('data-trigger', 'click');
            $(element).attr('data-container', '.fc-time-grid');
            //if the day is after wednesday
            if (event.start.day() > 3) {
                $(element).attr('data-placement', 'left');
            }
            var content = "";
            var eventtime = event.start.format("H:mm") + "-" + event.end.format("H:mm");
            if (event.type == "oral") {
                var div = $("#popover-oral-template").html();
                div = div.replace("{time}", eventtime);
                div = div.replace("{student}", event.student);
                readers = "";
                for (let reader of event.readers){
                    readers += reader + ", ";
                }
                div = div.replace("{readers}", readers);
                content += div;
            }
            else {
                content += "Who: " + event.user + "\n";
            }
            $(element).attr('data-content', content)
            $(element).popover({html : true});
        },
        eventAfterAllRender: function(view) {
            $("[name='event-popover']").on('shown.bs.popover', function () {
                console.log("editable!");
                $('.edit').editable('/eventsjson');
            });
        },
    });
    $("[name='event-popover']").on('shown.bs.popover', function () {
        console.log("editable!");
        $('.edit').editable('/eventsjson');
    });
});
$(document).on('change', 'select', function() {
    $('#calendar').fullCalendar( 'refetchEvents');
});
