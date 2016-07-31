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
        defaultView: 'basicWeek',         
        weekends: false,
        allDaySlot: false,
        editable: edit,
        header: false,
        slotDuration: '00:15:00',
        scrollTime: '10:00:00',
        events: {
            url: '/eventsjson',
            data: getFilters,
        },
        //most of what is in this function is for crating the qtip for the event
        eventRender: function(event, element, view) {
            $(element).attr('tabindex', '0');
            //making the content to go in the qtip
            var content = "";
            if (event.type == "oral") {
                //gets the hidden oral template div and replaces some data
                var div = $("#oral-qtip-template").html();
                div = div.replace("{student}", event.student);
                readers = "";
                for (let reader of event.readers){
                      readers += reader + ", ";
                }
                div = div.replace("{readers}", readers);
            }
            else {
                var div = $('#event-qtip-template').html()
                div = div.replace("{user}", event.user)
            }
            div = div.replace("{start}", event.start.format("H:mm"));
            div = div.replace("{end}", event.end.format("H:mm"));
            div = div.replace("{location}", event.location);
            content += div;

            //initilizing the qtips
            $(element).qtip({
                show: 'click',
                hide: {
                    event: 'click unfocus',
                },
                style: {
                    classes: 'cal-qtip qtip-bootstrap',
                },
                position: {
                    my: 'left center',
                    at: 'right center',
                    //makes sure that the qtips don't go outside fullcalendar
                    viewport: $('#calendar'),
                },   
                content: {
                    text: content,
                    title: "<span class='edit-title'>" + event.title + "</span>",
                    button: true,
                },
                events: {
                    render: function(qevent, api) {
                        //making the fields on the qtip editable
                        if (edit){
                            //initializing jeditables
                            $('.edit-start').editable(function(value, settings) {
                                //editing time to include date
                                dt = event.start.format('YMMDD ') + value;
                                $.post("/submitevent", { 
                                    event_id: event.id, 
                                    start   : dt}, 
                                    function(data){
                                        $(this).text(data);
                                        return data;
                                    });
                                return value;
                            },{
                                type       : 'time',
                                submit     : '<button class="btn btn-success" type="submit" >Ok</button>',
                                callback   : function(value, settings){
                                    $('#calendar').fullCalendar( 'refetchEvents');
                                },
                            });
                            $('.edit-end').editable(function(value, settings) {
                                //editing time to include date
                                //TODO abstract this function so it doesn't appear twice for both start and end
                                dt = event.end.format('YMMDD ') + value;
                                $.post("/submitevent", { 
                                    event_id: event.id, 
                                    end     : dt}, 
                                    function(data){
                                        $(this).text(data);
                                        return data;
                                    });
                                return value;
                            },{    
                                type       : 'time',
                                submit     : '<button class="btn btn-success" type="submit" >Ok</button>',
                                callback   : function(value, settings){
                                    $('#calendar').fullCalendar( 'refetchEvents');
                                },
                            });
                            $('.edit-user').editable('/submitevent',{
                                loadurl    : '/usersjson',
                                type       : 'select',
                                submit     : '<button class="btn btn-success" type="submit" >Ok</button>',
                                name       : 'user_id',
                                submitdata : {event_id: event.id},
                            });
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
                                callback   : function(value, settings){
                                    $('#calendar').fullCalendar( 'refetchEvents');
                                },
                            }); 
                            $('.edit-location').editable('/submitevent',{
                                name       : 'location',
                                submitdata : {event_id: event.id},
                                callback   : function(value, settings){
                                    $('#calendar').fullCalendar( 'refetchEvents');
                                },
                            }); 
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
                            $('.edit-delete-event').removeClass('hidden');
                            $('.edit-delete-event').click(function() {
                                $.post( "deletevent", { event_id: event.id} );
                                $('#calendar').fullCalendar( 'refetchEvents');
                                $(".qtip").remove();
                            });
                        }
                    }
                },
            });
        },
        eventResize: function(event, delta, revertFunc) {
            $.post("/submitevent", { event_id: event.id, 
                                     start   : event.start.format('YMMDD hh:mm:ss A'), 
                                     end     : event.end.format('YMMDD hh:mm:ss A'),
            });
        },
        eventDrop: function(event, delta, revertFunc) {
            $.post("/submitevent", { event_id: event.id, 
                                     start   : event.start.format('YMMDD hh:mm:ss A'), 
                                     end     : event.end.format('YMMDD hh:mm:ss A'),
            });
        },
        dayClick: function(date, jsEvent, view) {
            if (edit){
                start = "'" + date.format('YMMDD hh:mm:ss A') + "'"
                end = "'" + date.add(2, 'hours').format('YMMDD hh:mm:ss A') + "'"
                //{start} and {end} are parameters for the addEvent and addOral functions
                content = $("#add-event-oral-qtip-template").html().replace(/{start}/g,start).replace(/{end}/g,end)
                //popup to add event
                $(this).qtip({
                    show: {
                        ready: true,
                        event: "click",
                    },
                    hide: {
                        event: false,
                    },
                    style: {
                        classes: 'new-event-qtip qtip-bootstrap',
                    },
                    position: {
                        target: 'mouse',
                        my: 'bottom center',
                        at: 'top center',
                        adjust: {
                            mouse: false,
                        },
                        //makes sure that the qtips don't go outside fullcalendar
                        viewport: $('#calendar'),
                    },
                    content:{
                        text: content,
                        button: true,
                    },
                    events: {
                        render: function(event, api) {
                        }
                    },
                });
            }
        },
        viewRender: function(view, element){
            //makes it so the print page gets start and end times matching the calendar
            $("#filter-start").attr("value", view.start.format("YYYY-MM-DD"));
            $("#filter-end").attr("value", view.end.format("YYYY-MM-DD"));
        },
    });
});
$(document).on('change', '#filter-well select', updateQuery);

$(".clr-btn").click(function() {
    select = $(this).data("select"); //gets id of the select attached to this button
    $(select +  " > .default").prop('selected', true);
    updateQuery();
});

function updateQuery() {
    /*
    This Function gets called whenever the filters get changed and it updates
    the data in the calendar and the querystring that gets sent to printsched
    so that they reflect the filters
    */
    $('#calendar').fullCalendar( 'refetchEvents');
}

function addEvent(start, end, type) {
    /*
    Sends a new post request to add a new oral or event
    */
    $.post("/submitevent", { start : start, 
                             end   : end,
                             type  : type,
    });
    $('#calendar').fullCalendar( 'refetchEvents');
    cancel();
}

function cancel(){
    $('.qtip', window.parent.document).qtip("hide");
}

function getFilters(){
    //gets data from the filters to send put in the events query
    return {
        department: $('#department option:selected').text(),
        division: $('#division option:selected').text(),
        'professors[]': $('#prof-select').val(),
        'students[]': $('#stu-select').val()
    };
} 

