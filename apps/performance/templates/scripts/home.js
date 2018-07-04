(function (scope) {
    scope.mockNotify = [
        { "id": "notify001", "content": "1 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify002", "content": "2 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify003", "content": "3 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify004", "content": "4 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify005", "content": "5 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify006", "content": "6 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify007", "content": "7 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify008", "content": "8 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify009", "content": "9 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify010", "content": "10 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" },
        { "id": "notify011", "content": "11 Có một sự kiện diễn ra vào lúc 11:00 AM ngày 20/11/2018 tại Tp.HCM" }
    ];

    /**
     * Property Scope
     */
    scope.handleEvent = handleEvent;
    scope.$functions = scope.$root.$functions;
    scope.handleEvent = new handleEvent();

    /**
     * Handle events in page
     */
    function handleEvent() {

        //Event toggle group function
        this.onCollapse = (id, event) => {
            $("#hcs-body-" + id).slideToggle(400);
            //set css class when clicked header
            var cssClass = $('#icon-' + id).attr('class') == 'la la-angle-down'
                ? 'la la-angle-right'
                : 'la la-angle-down';
            $('#icon-' + id).removeAttr('class');
            $('#icon-' + id).prop('class', cssClass);
        };

        //Close notification
        this.onCloseNotify = ($event) => {
            //$($event.target).parent().parent().parent().fadeOut();
            $($event.target).parent().parent().parent().swipe({
                tap: function (event, target) {
                    alert('tap');
                },
                swipe: function (event, direction, distance, duration, fingerCount) {
                    //Handling swipe direction.
                    $($event.target).parent().parent().parent().hide("slide", { direction: "right" }, "fast");
                }
            });
        }

        this.redirectPage = function(child) {
            if (child.url.trim()) {
                scope.$root.currentModule = _.filter(scope.$root.$functions, function (d) {
                    return d["function_id"] == child.parent_id;
                })[0];//.custom_name.replace("/", " ");
                scope.$root.currentFunction = child;
            }
            location.href = '#page=' + child.function_id;
        }
    }

    

    /**
     * ===============================  Implementation - END  ==================================
     */
});