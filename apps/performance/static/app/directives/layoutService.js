(function () {
    'use strict';

    angular
        .module('hcs-template')
        .factory("templateService", layoutService);
    var fac = {}
    function layoutService() {

        fac.__templatePath = '../performance/static/app/directives/';
        fac.onClickFunctionLeftMenu = onClickFunctionLeftMenu;
        fac.onClickBreadCumbDropdownMenu = onClickBreadCumbDropdownMenu;
        fac.onClickHideLeftMenufunction = onClickHideLeftMenufunction;
        fac.getTemplatePath = getTemplatePath;

        /**
        * Handle when click function button on left side screen
        * @param id : function_id
        */
        function onClickFunctionLeftMenu(f, event) {
            /* Inactive present function*/
            $('.hcs-system-admin-menu-contain ul li a.hcs-admin-system-selected').removeClass('hcs-admin-system-selected');
            $('.hcs-system-admin-menu-contain ul li.hcs-admin-system-selected').removeClass('hcs-admin-system-selected');

            $('#hcs-admin-system-panel-content div.in').removeClass('in');
            $('#hcs-admin-system-panel-content div.active').removeClass('active');

            /* Active present tab function*/
            $('#' + f.function_id).addClass('in');
            $('#' + f.function_id).addClass('active');

            /*Active present function on left menu*/
            $('#admin-system-' + f.function_id).addClass('hcs-admin-system-selected');
        }

        function onClickBreadCumbDropdownMenu() {
            $("#dropdownFunction").toggleClass("show");
        }

        /* Collapse or expand aside left menu */
        function onClickHideLeftMenufunction(){
            //Hide menu
            $('#hcs-system-admin-menu').fadeToggle(50);

            //Change icon 
            var cssClass = $('#toggleMenuFucntion span i').attr('class') == 'la la-angle-left' ?
                'la la-bars' :
                'la la-angle-left';
            $('#toggleMenuFucntion span i').removeAttr('class');
            $('#toggleMenuFucntion span i').prop('class', cssClass);


            $('.hcs-system-admin-content').hasClass('hcs-system-admin-content-expand') == true ?
                $('.hcs-system-admin-content').removeClass('hcs-system-admin-content-expand') :
                $('.hcs-system-admin-content').addClass('hcs-system-admin-content-expand');

            $('#hcs-admin-system-breadcrumb').hasClass('hcs-admin-system-breadcrumb-collapse') == true ?
                $('#hcs-admin-system-breadcrumb').removeClass('hcs-admin-system-breadcrumb-collapse') :
                $('#hcs-admin-system-breadcrumb').addClass('hcs-admin-system-breadcrumb-collapse');

        }

        function getTemplatePath(filePath) {
            /*Example: '../performance/static/app/directives/breadcumb/breadcumb.html'*/
            return fac.__templatePath + filePath + '/' + filePath + '.html';
        }
        return fac;
    }
})();