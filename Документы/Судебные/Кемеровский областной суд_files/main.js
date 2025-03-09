$(document).ready(function () {
	var htmlObj = $("html");
	var htmlBody = $("body");

	htmlBody.filter(".repositionPopups").resize(function () {
		repositionPopups();
	});

	var bez_otveta = $("#bez_otveta");
	if(bez_otveta.is(":checked")) {
		$('#smail,#semail,#of_otvet,#zv').hide();
	}
	bez_otveta.click(function () {
		$('#smail,#semail,#of_otvet,#zv').toggle();
	});

	$("#assist,#adopt,#norm").click(function (event) {
		event.preventDefault();
		var type_theme = $(this).attr('id');
		$.cookie('theme', type_theme, {expires: 14, path: '/'});

		if(!htmlObj.hasClass(type_theme)) {
			htmlObj.removeClass();
			if(type_theme != "norm") {
				htmlObj.addClass(type_theme);
			}
		}
	});

	$("#switch-norm").click(function () {
		htmlObj.removeClass();
		$.cookie('theme', 'norm', {expires: 14, path: '/'});
	});

	$('.col_left .m-left_m #left_menu .menu__item:last, .menu_horizontal .menu__item:last').addClass("menu__item_last");

	var assist_font_size_selector = $(".assist_font_size_selector");
	assist_font_size_selector.css("font-size", assist_font_size_selector.css("font-size"));
	var assistFontSize = $.cookie('assistFontSize');
	switch(parseInt(assistFontSize)) {
		case 2:
			htmlBody.addClass("assist_font_size_medium");
			assist_font_size_selector.children(".assist_font_size_medium").addClass("active");
			$.cookie('assistFontSize', 2, {expires: 14, path: '/'});
			break;
		case 3:
			htmlBody.addClass("assist_font_size_large");
			assist_font_size_selector.children(".assist_font_size_large").addClass("active");
			$.cookie('assistFontSize', 3, {expires: 14, path: '/'});
			break;
		default:
			assist_font_size_selector.children(".assist_font_size_norm").addClass("active");
			htmlBody.addClass("assist_font_size_norm");
			$.cookie('assistFontSize', 1, {expires: 14, path: '/'});
	}
	assist_font_size_selector.find("a").click(function (e) {
		e.preventDefault();
		var parentLi = $(this).parent();
		parentLi.parent().children().removeClass("active");
		$("body").removeClass("assist_font_size_norm").removeClass("assist_font_size_medium").removeClass("assist_font_size_large")
			.addClass(parentLi.attr("class"));
		switch(parentLi.attr("class")) {
			case "assist_font_size_medium":
				$.cookie('assistFontSize', 2, {expires: 14, path: '/'});
				break;
			case "assist_font_size_large":
				$.cookie('assistFontSize', 3, {expires: 14, path: '/'});
				break;
			default:
				$.cookie('assistFontSize', 1, {expires: 14, path: '/'});
		}
		parentLi.addClass("active");
	});
	$("div.menu__item a.norm_selector").click(function () {
		$("body").removeClass("assist_font_size_norm").removeClass("assist_font_size_medium").removeClass("assist_font_size_large");
		$('html').removeClass('assist');
		$.removeCookie('assistFontSize');
		$.removeCookie('theme');
		assist_font_size_selector.find("li").removeClass("active").filter(":first").addClass("active");
	});

	if(document.location.href.indexOf("sud_delo") > -1) {
		hideRightBlockOnSmallViewport();
		$(window).resize(function () {
			hideRightBlockOnSmallViewport();
		});
	}

	$(".mapTreeRevealAll").click(function (e) {
		e.preventDefault();
		var contentBox = $(this).parentsUntil(".box").parent();
		contentBox.find("table.mapSubtree").show();
		contentBox.find("img.mapSubtreeToggle").attr("src", 'images/minus.gif');
		$('#YMapsID').hide();
		$('#tblSudTree').show();
		if(typeof myMap != 'undefined')myMap.destroy();
	});
	$(".mapTreeCollapseAll").click(function (e) {
		e.preventDefault();
		var contentBox = $(this).parentsUntil(".box").parent();
		contentBox.find("table.mapSubtree").hide();
		contentBox.find("img.mapSubtreeToggle").attr("src", 'images/plus.gif');
		$('#YMapsID').hide();
		$('#tblSudTree').show();
		if(typeof myMap != 'undefined')myMap.destroy();
	});

	if(ymaps){ymaps.ready(init);}

	function init() {
		var myMap;
		$('.allSudOnMap').click(function () {
			if(!myMap) {
				$('#tblSudTree').hide();
				$('#YMapsID').show();
				myMap = new ymaps.Map('YMapsID', {
					center: [57.767265, 40.925358], // Новосибирск
					zoom: 9
				}, {
					searchControlProvider: 'yandex#search'
				});

				jQuery.getJSON('/modules.php?name=sud&act=all&region_id=".UPKOD."', function (json) {
					var geoObjects = ymaps.geoQuery(json)
						.addToMap(myMap)
						.applyBoundsToMap(myMap, {
							checkZoomRange: true
						});
				});

			}
			else {
				$('#tblSudTree').hide();
				$('#YMapsID').show();

			}
		});

	}

	$(".mapSubtreeToggle").click(function (e) {
		e.preventDefault();
		var parentTr = $(this).parentsUntil("tr").parent();
		var icon = parentTr.find("> td:first img.mapSubtreeToggle");
		var childTable = parentTr.find("> td > table.mapSubtree");
		if(childTable.filter(":visible").length > 0) {

			childTable.hide();
			icon.attr("src", 'images/plus.gif');
		}
		else {

			childTable.show();
			icon.attr("src", 'images/minus.gif');
		}
	});

	$(".admList > tr, .admList tbody tr")
		.mouseenter(function () {
			$(this).addClass('hovered');
		})
		.mouseleave(function () {
			$(this).removeClass('hovered');
		});

	$('.open-fancybox').fancybox();

	$('.open-calendar').datepicker();

	function printVersion(titleObj, contentObj) {
		var title = titleObj.html();
		var content = contentObj.html();
		var currScrollPos = $(document).scrollTop();
		htmlObj.animate({"scrollTop": 0}, 0);
		htmlBody.animate({"scrollTop": 0}, 0);
		var pageTitle = htmlObj.find('title');

		var page = "<div id='divPrintHeader' style='border-bottom: 1px solid #cecece;'>" +
			"<table><tr><td id='tdCredits'>Информация предоставлена Интернет–порталом ГАС «Правосудие»</td>" +
			"<td id='tdCreditsGoBack'><a class='serviceLinks' style='margin-left: 1em' href='#'>Закрыть</a></td></tr></table>" +
			"</div><div id='div{$html_pref}DocPrint' class='divDocPrint'><div id='div{$html_pref}DocPrintTitle' class='divDocPrintTitle'>" +
			title + ((typeof pageTitle !== 'undefined') ? ' — ' + pageTitle.html() : '') + "</div>" +
			"<div id='divDocPrintBody' class='divDocPrintBody'>" + content + "</div></div>";
		var pageObj = $("<div></div>").append(page);
		var bodyChildren = htmlBody.children(':visible');
		bodyChildren.hide();
		htmlBody.append(pageObj);
		htmlObj.addClass('printVersion');

		function closePrintVersion() {
			pageObj.remove();
			htmlObj.removeClass('printVersion');
			bodyChildren.show();
			htmlObj.animate({"scrollTop": currScrollPos}, 0);
			htmlBody.animate({"scrollTop": currScrollPos}, 0);
		}

		$(document).keydown(function (e) {
			if(e.which == 27) closePrintVersion();
		});
		pageObj.find('.serviceLinks').click(function (e) {
			e.preventDefault();
			closePrintVersion();
		});
	}

	$(".showPrintVersion").click(function (e) {
		e.preventDefault();
		var printTitle = $(".printVersionTitle");
		var printBody = $(".printVersionBody");
		if(typeof printTitle !== 'undefined' && typeof printBody !== 'undefined') {
			printVersion(printTitle, printBody);
		}
	});
});

function detectIE6() {
	var browser = navigator.appName;
	if(browser == "Microsoft Internet Explorer") {
		var b_version = navigator.appVersion;
		var re = /MSIE\s+(\d\.\d\b)/;
		var res = b_version.match(re);
		if(res[1] <= 6) {
			return true;
		}
	}
	return false;
}

function getClientWidth() {
	//return document.compatMode=='CSS1Compat' && !window.opera?document.documentElement.clientWidth:document.body.clientWidth;
	var a = document.documentElement.clientWidth ? document.documentElement.clientWidth : document.body.clientWidth;
	return parseInt(a);
}

function getClientHeight() {
	//return document.compatMode=='CSS1Compat' && !window.opera?document.documentElement.clientHeight:document.body.clientHeight;
	var a = document.documentElement.clientHeight ? document.documentElement.clientHeight : document.body.clientHeight;
	return parseInt(a);
}

function getBodyScrollTop() {
	var a = self.pageYOffset || (document.documentElement && document.documentElement.scrollTop) || (document.body && document.body.scrollTop);
	return parseInt(a);
}

function getBodyScrollLeft() {
	var a = self.pageXOffset || (document.documentElement && document.documentElement.scrollLeft) ||
		(document.body && document.body.scrollLeft);
	return parseInt(a);
}

function showTooltip(event, insText) {
	var ttObj = document.getElementById('divTooltip');
	if(typeof ttObj != 'undefined') {
		if(typeof arguments[2] != 'undefined') {
			var w = arguments[2];
		}
		else {
			w = 250;
		}
		if(typeof w == 'number') {
			ttObj.style.width = w + 'px';
		}
		else {
			ttObj.style.width = w;
		}

		if(typeof arguments[3] != 'undefined') {
			var h = arguments[3];
			if(typeof h == 'number') {
				ttObj.style.height = h + 'px';
			}
			else {
				ttObj.style.height = h;
			}
		}
		ttObj.style.overflow = 'hidden';
		ttObj.innerHTML = insText;
		ttObj.style.left = '-1000px';
		ttObj.style.top = '-1000px';
		ttObj.style.display = 'block';
		repositionElement(event, ttObj);
	}
}

function repositionElement(event, el) {
	if(typeof el != 'undefined') {
		if(!event) {
			event = window.event;
		}

		var clientX = parseInt(event.clientX);
		var clientY = parseInt(event.clientY);
		var elWidth = parseInt(el.offsetWidth);
		var elHeight = parseInt(el.offsetHeight);

		if(getClientWidth() - elWidth - 10 > clientX) {
			el.style.left = clientX + 'px';
		}
		else {
			el.style.left = clientX - elWidth + 'px';
		}
		if(getClientHeight() - elHeight - 32 > clientY) {
			el.style.top = clientY + 22 + 'px';
		}
		else {
			el.style.top = clientY - elHeight - 3 + 'px';
		}
	}
}

function hideTooltip() {
	var ttObj = document.getElementById('divTooltip');
	if(typeof ttObj != 'undefined') {
		ttObj.style.display = 'none';
		ttObj.innerHTML = '';
	}
}

function moveTooltip(event) {
	var ttObj = document.getElementById('divTooltip');
	if(typeof ttObj != 'undefined') repositionElement(event, ttObj);
}

function showPopup() {
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');
	if(typeof popupDivB != 'undefined' && typeof popupDivT != 'undefined') {
		popupDivB.style.display = 'block';
		popupDivT.style.display = 'block';
		repositionPopups();
	}
}

function hidePopupDiv() {
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');
	if(typeof popupDivB != 'undefined' && typeof popupDivT != 'undefined') {
		popupDivB.style.display = 'none';
		popupDivT.style.display = 'none';
		popupDivT.innerHTML = '';
	}
}

function repositionPopups() {
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');
	var browserW = getClientWidth();
	var browserH = getClientHeight();
	var bodyScrollLeft = getBodyScrollLeft();
	var bodyScrollTop = getBodyScrollTop();

	if(typeof popupDivB != 'undefined' && popupDivB.style.display == 'block') {
		popupDivB.style.width = browserW + 'px';
		popupDivB.style.height = browserH + 'px';
	}
	if(typeof popupDivT != 'undefined' && popupDivT.style.display == 'block') {
		var popupDivTWidth = popupDivT.offsetWidth;
		var popupDivTHeight = popupDivT.offsetHeight;

		if(popupDivTWidth + 40 < browserW) {
			popupDivT.style.left = parseInt((browserW - popupDivTWidth) / 2) + 20 + bodyScrollLeft + 'px';
		}
		else {
			popupDivT.style.left = 20 + bodyScrollLeft + 'px';
		}
		if(popupDivTHeight + 40 < browserH) {
			popupDivT.style.top = parseInt((browserH - popupDivTHeight) / 2) + 20 + bodyScrollTop + 'px';
		}
		else {
			popupDivT.style.top = 20 + bodyScrollTop + 'px';
		}
	}
}

function resizePopup() {
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');
	if(typeof popupDivB != 'undefined' && typeof popupDivT != 'undefined') {
		popupDivB.style.width = getClientWidth() + 'px';
		popupDivB.style.height = getClientHeight() + 'px';
	}
}

function appendNewFileInput(tblId) {
	if(document.getElementById(tblId) && document.getElementById('img_count')) {
		var tblObj = document.getElementById(tblId);
		var newTr = document.createElement('tr');
		var newTd = document.createElement('td');
		var newInput = document.createElement('input');
		newTr.setAttribute('id', 'imgFileInput' + (parseInt(document.getElementById('img_count').value) + 1));
		newInput.setAttribute('type', 'file');
		newInput.setAttribute('size', '90');
		newInput.setAttribute('id', 'prPhoto' + (parseInt(document.getElementById('img_count').value) + 1));
		newInput.setAttribute('name', 'prPhoto' + (parseInt(document.getElementById('img_count').value) + 1));
		newTd.appendChild(newInput);
		newTr.appendChild(newTd);
		if(tblObj.hasChildNodes()) {
			var tbodyEl = tblObj.firstChild;
			while(tbodyEl.nodeType != 1 && (tbodyEl.nodeName != 'TBODY' || tbodyEl.nodeName != 'tbody') && tbodyEl.nextSibling) {
				tbodyEl = tbodyEl.nextSibling;
			}
			if(tbodyEl.nodeType == 1 && (tbodyEl.nodeName == 'TBODY' || tbodyEl.nodeName == 'tbody')) {
				tbodyEl.appendChild(newTr);
			}
			else {
				tblObj.appendChild(newTr);
			}
		}
		else {
			tblObj.appendChild(newTr);
		}
		document.getElementById('img_count').value = parseInt(document.getElementById('img_count').value) + 1;
	}
}

function replace_inp(text) {
	return $.trim(text.replace(/[^а-яё0-9.,:;\n_ \-№]+/gi, ''));
}

var modal_div = [];

function modWin(type, creat_idDiv) {
	var popID = '#popup'; //Get Popup Name
	if(type == 'close') {
		$('#fade , ' + popID).fadeOut(function () {
			$('#fade').remove();  //fade them both out
		});
		return;
	}
	var add_m = true;
	for(var ind in modal_div) {
		if(modal_div[ind] == creat_idDiv) {
			add_m = false;
		}
	}

	if(add_m) modal_div.push(creat_idDiv);

	for(var index in modal_div) {
		if(modal_div[index] == creat_idDiv) {
			$('#poptxt #' + creat_idDiv).show();
		}
		else {
			$('#poptxt #' + modal_div[index]).hide();
		}
	}

	//Define margin for center alignment (vertical   horizontal) - we add 80px to the height/width to accomodate for the padding  and border width defined in the css
	var winH = $(window).height();
	var winW = $(window).width();

	//Fade in the Popup and add close button
	$(popID).css('max-width', parseInt(winW) - parseInt($(popID).css('padding-left')) - parseInt($(popID).css('padding-right')) - 10 + 'px');
	$(popID).css('max-height', parseInt(winH) - parseInt($(popID).css('padding-top')) - parseInt($(popID).css('padding-bottom')) - 10 + 'px');
	$(popID).css('top', winH / 2 - $(popID).outerHeight() / 2 + 'px');
	$(popID).css('left', winW / 2 - $(popID).outerWidth() / 2 + 'px');
	$(popID).fadeIn();

	//Fade in Background
	$('<div id="fade"></div>').click(function (e) {
		e.stopPropagation();
		modWin('close');
	}).appendTo($('body'));
	$('#fade').css({'filter': 'alpha(opacity=80)'}).fadeIn(); //Fade in the fade layer - .css({'filter' : 'alpha(opacity=80)'}) is used to fix the IE Bug on fading transparencies
}

//del

function addFileField() {
	var cont = $('#fileInputsCont');
	var filesCount = cont.children('input').length;
	if(filesCount > 8) {
		$('#crfld').hide();
	}
	if(cont.length > 0) {
		cont.append("<br><input type='file' id='attfile" + (filesCount + 1) + "' name='attfile" + (filesCount + 1) + "'>");
	}
}

function hideRightBlockOnSmallViewport() {
	var docWidth = parseInt($(document).width());
	var colRight = $(".col_right");
	if(colRight.length > 0) {
		if(docWidth < 1300) {
			colRight.filter(":visible").hide();
		}
		else {
			colRight.filter(":hidden").show();
		}
	}
}
$( function() {
    $( "#tabs" ).tabs();
  } );