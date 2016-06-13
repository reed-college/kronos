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
                //gets data from the filters to send put in the events query
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
                //gets the hidden oral template div and replaces some data
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
            //initializing jeditable
            $(element).on('shown.bs.popover', function () {
                if (edit){
                    $('.edit').editable('/submitevent',{
                        loadurl    : '/usersjson',
                        loaddata   : {type: "student"},
                        type       : 'select',
                        submit     : '<button class="btn btn-success" type="submit" >Ok</button>',
                        name       : 'stu_id',
                        submitdata : {event_id: event.id},
                    });
                }
            });
        },
    });
});
$(document).on('change', 'select', function() {
    $('#calendar').fullCalendar( 'refetchEvents');
});
