// button menu
$(document).ready(function () {
	"use strict";
	$(".btn_menu a").click(function () {
		$(".sidebar,.main_container").toggleClass("open");
	});
	$(".btn_full").click(function () {
		$(".content_3,.content_7").toggleClass("show_hidden");
	});
	$(".btn_expanded").click(function () {
		$(this).parents(".tr").toggleClass("expanded");
	});
	//tabs
	$("#main_tab_01 a").on("click", function (e) {
		e.preventDefault();
		$(this).tab('show');
	});
	//collapse
	$('.coll_show').collapse("show");
	$('#sandbox-container input').datepicker({});
});
$(document).ready(function () {
	"use strict";
	$('.dropdown-toggle').dropdown();
});
$(document).ready(function () {
	"use strict";
	$('.scroll-pane').jScrollPane();
});
$(document).ready(function () {
	"use strict";
	if ($(window).width() > 1024) {
		$(".modal-content-plus .title a").click(function (e) {
			var isOpen = $(".modal-content-plus,.modal-dialog,.modal-body-content").hasClass("open");
			var isSelected = $(e.target).hasClass("selected");
			if (((isOpen) !== true) && ((isSelected) !== true)) {
				$(".modal-content-plus,.modal-dialog,.modal-body-content").addClass("open");
				$(e.target).addClass("selected");
			}
			if (((isOpen) === true) && ((isSelected) === true)) {
				$(".modal-content-plus,.modal-dialog,.modal-body-content").removeClass("open");
				$(e.target).removeClass("selected");
			}
			if (((isOpen) === true) && ((isSelected) !== true)) {
				$(".modal-content-plus .title a.btn_modal.selected").removeClass("selected");
				$(e.target).addClass("selected");
			}
			if ($(".btn_link").hasClass("selected")) {
				$(".content_link").addClass("show");
				$(".content_data").removeClass("show");
			}
			if ($(".btn_data").hasClass("selected")) {
				$(".content_data").addClass("show");
				$(".content_link").removeClass("show");
			}
		});
	} else {}
});
$(document).ready(function () {
	"use strict";
	$(".sprint_plan dl dt").click(function () {
		$(this).toggleClass("arrow");
	});
});
