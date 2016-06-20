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
        editable: edit,
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
        //most of what is in this function is for crating the qtip for the event
        eventRender: function(event, element, view) {
            $(element).attr('tabindex', '0');
            //making the content to go in the qtip
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
                   // readers += "<span class='edit-reader'>" + reader + ", " + "</span>";
                }
                div = div.replace("{readers}", readers);
                content += div;
            }
            else {
                content += "Who: " + event.user + "\n";
            }
            //initilizing the qtips
            $(element).qtip({
                show: 'click',
                hide: 'unfocus',
                style: {
                    classes: 'cal-qtip qtip-bootstrap',
                },
                position: {
                    my: 'left center',
                    at: 'right center',
                    //makes sure that the qtips don't go outside fullcalendar
                    viewport: $('.fc-time-grid'),
                },   
                content: {
                    text: content,
                    title: "<span class='edit-title'>" + event.title + "</span>",
                },
                events: {
                        render: function(qevent, api) {
                            //making the fields on the qtip editable
                            if (edit){
                                //initializing jeditables
                                $('.edit-student').editable('/submitevent',{
                                    loadurl    : '/usersjson',
                                    loaddata   : {type: "student"},
                                    type       : 'select',
                                    submit     : '<button class="btn btn-success" type="submit" >Ok</button>',
                                    name       : 'stu_id',
                                    submitdata : {event_id: event.id},
                                });
                                $('.edit-title').editable('/submitevent',{
                                    name       : 'summary',
                                    submitdata : {event_id: event.id},
                                }); 
                                /*$('.edit-readers').editable('/submitevent',{
                                    loadurl    : '/usersjson',
                                    loaddata   : {type: "professor"},
                                    type       : 'select',
                                    submitdata : {event_id: event.id},
                                });*/
                                var readerselect = "<select id='reader-select' multiple='multiple'>" + $("#prof-select").html() + "</select>";
                                $('.edit-readers').replaceWith(readerselect);
                                $('#reader-select option').each(function(index,value){
                                    //if a reader is in event.readers, the select them
                                    if (event.readers.indexOf(value.text) >= 0){
                                        value.setAttribute("selected", true);
                                    }
                                });
                                $("#reader-select", this).select2({
                                    placeholder: "Readers",
                                    allowClear: true
                                });
                                $('#reader-select', this).on('change', function (evt) {
                                   $.post( "/submitevent", { event_id: event.id, readers: $(this).val() } );
                                });
                            }
                        }
                }
            });
        },
        eventResize: function(event, delta, revertFunc) {
            $.post("/submitevent", { event_id: event.id, start: event.start.format('YMMDD hh:mm:ss A'), end: event.end.format('YMMDD hh:mm:ss A')});
        },
        eventDrop: function(event, delta, revertFunc) {
            $.post("/submitevent", { event_id: event.id, start: event.start.format('YMMDD hh:mm:ss A'), end: event.end.format('YMMDD hh:mm:ss A')});
        },
    });
});
$(document).on('change', '#filter-well select', function() {
    $('#calendar').fullCalendar( 'refetchEvents');
});
