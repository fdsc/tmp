// JavaScript Document

function show_search(n_n, c_t) {
	document.location.href = '/modules.php?name=sud_delo' + (srv_num ? '&srv_num=' + srv_num : '') + '&name_op=sf&delo_id=1540005' + (c_t != 1 ? '&new=5' : '');
}

function hearing_list() {
	document.getElementById('calformH').submit();
}

function back() {
	history.back();
}

function urlencode(text) {
	var trans = [];
	for(var i = 0x410; i <= 0x44F; i++) trans[i] = i - 0x350;//алфавит
	trans[0x401] = 0xA8;//Ё
	trans[0x451] = 0xB8;//ё
	trans[0x2116] = 0xB9;//№
	var ret = [];
	for(var i = 0; i < text.length; i++) {
		var n = text.charCodeAt(i);
		if(typeof trans[n] != 'undefined') n = trans[n];
		if(n <= 0xFF) ret.push(n);
	}
	return escape(String.fromCharCode.apply(null, ret));
}

function addFieldN() {  //alert(document.getElementById('calform').length);
	for(var e = 0; e < document.getElementById('calform').length; e++) {
		if(document.getElementById('calform').elements[e].name == fieldnam) {
			document.getElementById('calform').elements[e].value = urlencode(n);
			document.getElementById('calform').elements[e + 1].value = n;
		}
	}
}

function clearFieldN() {  //alert(document.getElementById('calform').length);
	for(var e = 0; e < document.getElementById('calform').length; e++) {
		if(document.getElementById('calform').elements[e].name == fieldnam) {
			document.getElementById('calform').elements[e].value = '';
			document.getElementById('calform').elements[e + 1].value = '';
		}
	}
}

function showCatalog(w, h, _curent_delo_table, _fieldname) {
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');
	w = parseInt(w);
	h = parseInt(h);
	if(popupDivB && popupDivT) {
		popupDivB.style.width = popupDivB.parentNode.offsetWidth + 'px';
		popupDivB.style.height = popupDivB.parentNode.offsetHeight + 'px';
		popupDivT.style.width = w + 'px';
		popupDivT.style.height = h + 'px';
		popupDivT.InnerHTML = '<img src="/images/ajax-loader.gif" hspace="217" vspace="193">'
		url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=cat&nc=1&curent_delo_table=' + _curent_delo_table + '&fieldname=' + _fieldname + '&h=' + h + '';
		//alert (url);
		loadXMLDoc(url);
		if(getClientWidth() - w > 40) popupDivT.style.left = (((getClientWidth() - w) / 2) + getBodyScrollLeft()) + 'px';
		else popupDivT.style.left = 0 + getBodyScrollLeft() + 20 + 'px';
		if(getClientHeight() - h > 40) popupDivT.style.top = (((getClientHeight() - h) / 2) + getBodyScrollTop()) + 'px';
		else popupDivT.style.top = 0 + getBodyScrollTop() + 20 + 'px';
		showPopup();
		//if (popupDivB){
		//popupDivB.style.display='block';
		//}
		//popupDivT.style.display='block';
	}
}

function showCatalogInst(w, h, court_type, n_n) {
	//document.getElementById('content').innerHTML='';
	//document.getElementById('srch').innerHTML='';
	//alert(document.getElementById('content').innerHTML);
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');
	w = parseInt(w);
	h = parseInt(h);
	if(popupDivB && popupDivT) {
		popupDivB.style.width = popupDivB.parentNode.offsetWidth + 'px';
		popupDivB.style.height = popupDivB.parentNode.offsetHeight + 'px';
		popupDivT.style.width = w + 'px';
		popupDivT.style.height = h + 'px';
		popupDivT.InnerHTML = '<img src="/images/ajax-loader.gif" hspace="217" vspace="193">'
		url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=cat_i&nc=1&h=' + h + '&c_t=' + court_type + '&n_n=' + n_n + '';
		//alert (url);
		loadXMLDoc(url);
		if(getClientWidth() - w > 40) popupDivT.style.left = (((getClientWidth() - w) / 2) + getBodyScrollLeft()) + 'px';
		else popupDivT.style.left = 0 + getBodyScrollLeft() + 20 + 'px';
		if(getClientHeight() - h > 40) popupDivT.style.top = (((getClientHeight() - h) / 2) + getBodyScrollTop()) + 'px';
		else popupDivT.style.top = 0 + getBodyScrollTop() + 20 + 'px';
		showPopup();
		//if (popupDivB){
		//popupDivB.style.display='block';
		//}
		//popupDivT.style.display='block';
	}
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
	var a = self.pageXOffset || (document.documentElement && document.documentElement.scrollLeft) || (document.body && document.body.scrollLeft);
	return parseInt(a);
}

function loadXMLDoc(url) {
	if(window.XMLHttpRequest) {
		req = new XMLHttpRequest();
		req.onreadystatechange = processReqChange;
		req.open("GET", url, true);
		//req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");
		req.send(null);

	}
	else
		if(window.ActiveXObject) {
			req = new ActiveXObject("Microsoft.XMLHTTP");
			if(req) {
				req.onreadystatechange = processReqChange;
				req.open("GET", url, true);
				//req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");
				req.send();
			}
		}
}

function processReqChange() {
	var popupDivT = document.getElementById('divFSPopupTop');
	if(req.readyState == 4) {

		if(req.status == 200) {

			if(req.responseText.indexOf("Warning") != -1) {
				popupDivT.style.display = 'block';
				popupDivT.innerHTML = "<div align='center'><font size='3'><b><font color='#ff0000'>ОШИБКА ЗАГРУЗКИ ДАННЫХ!</b></font></div>" + req.responseText;
			}
			else {
				popupDivT.style.display = 'block';
				popupDivT.innerHTML = req.responseText;
			}

		}
		else {
			alert("Ошибка:\n" + req.statusText);
		}
	}
}

function loadXMLDoc1(url) {
	if(window.XMLHttpRequest) {
		req = new XMLHttpRequest();
		req.onreadystatechange = processReqChange1;
		req.open("GET", url, true);
		//req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");
		req.send(null);

	}
	else
		if(window.ActiveXObject) {
			req = new ActiveXObject("Microsoft.XMLHTTP");
			if(req) {
				req.onreadystatechange = processReqChange1;
				req.open("GET", url, true);
				//req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");
				req.send();
			}
		}
}

function processReqChange1() {
	var content = document.getElementById('content');
	if(req.readyState == 4) {

		if(req.status == 200) {

			if(req.responseText.indexOf("Warning") != -1) {
				content.style.display = 'block';

				content.innerHTML = "<div align='center'><font size='3'><b><font color='#ff0000'>ОШИБКА ЗАГРУЗКИ ДАННЫХ!</b></font></div>" + req.responseText;
			}
			else {
				//alert(req.responseText);
				//content.style.display='block';

				content.innerHTML = req.responseText;
			}
		}
		else {
			alert("Ошибка:\n" + req.statusText);
		}
	}
}

function button_over(eButton) {
	eButton.style.backgroundColor = "#EFEBCE";
	eButton.style.borderColor = "darkblue darkblue darkblue darkblue";
}

function button_out(eButton) {
	eButton.style.backgroundColor = "";
	eButton.style.borderColor = "";
}

function button_down(eButton) {
	eButton.style.backgroundColor = "#8494B5";
	eButton.style.borderColor = "darkblue darkblue darkblue darkblue";
}

function button_up(eButton) {
	eButton.style.backgroundColor = "#B5BDD6";
	eButton.style.borderColor = "darkblue darkblue darkblue darkblue";
	eButton = null;
}

function getInfoAndUpdate(_n, _field) {
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');
	if(popupDivB && popupDivT) {
		fieldnam = _field;
		n = _n;
		addFieldN();
		hidePopupDiv();
	}
}

function select_delo_id(d_i, c_t) {

	var delo_id;
	var case_type;
	var popupDivB = document.getElementById('divFSPopupBottom');
	var popupDivT = document.getElementById('divFSPopupTop');

	delo_id = d_i;
	case_type = c_t;
	if(popupDivB && popupDivT) {
		//alert(delo_id);
		if(delo_id != '0') {
			if(delo_id == 1540006) {
				if(case_type == 1) {
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1540006';
				}
				if(case_type == 4) {
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1540006&new=4';
				}
				if(case_type == 50780001) {
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1540006&case_type=50780001';
				}
				loadXMLDoc1(url);
			}
			if(delo_id == 4) {
				//document.getElementById('inst1').innerHTML='Поиск по уголовным делам - кассация';
				//document.getElementById('inst2').style.display='none';
				if(case_type == 1) {
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=4';
				}
				if(case_type == 2450001) {
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=4&new=2450001';
				}
				loadXMLDoc1(url);
			}
			if(delo_id == 2450001) {
				//document.getElementById('inst1').innerHTML='Поиск по уголовным делам - надзор';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=2450001';
				loadXMLDoc1(url);
			}
			if(delo_id == 6) {
				//document.getElementById('inst1').innerHTML='Поиск по уголовным делам - надзорные жалобы';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=6';
				loadXMLDoc1(url);
			}
			if(delo_id == 8) {
				//document.getElementById('inst1').innerHTML='Поиск по уголовным делам - надзорные дела';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=8';
				loadXMLDoc1(url);
			}
			if(delo_id == 1540005) {
				if(case_type == 1) {
					//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - первая инстанция';
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1540005';
				}
				if(case_type == 5) {
					//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - первая инстанция';
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1540005&new=5';
				}
				if(case_type == 50520004) {
					//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - апелляция';
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1540005&case_type=50520004';
				}
				//document.getElementById('inst2').style.display='none';
				loadXMLDoc1(url);
			}
			if(delo_id == 5) {
				//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - кассация';
				//document.getElementById('inst2').style.display='none';
				if(case_type == 1) {
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=5';
				}
				if(case_type == 2800001) {
					//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - первая инстанция';
					url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=5&new=2800001';
				}
				loadXMLDoc1(url);
			}
			if(delo_id == 2800001) {
				//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - надзор';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=2800001';
				loadXMLDoc1(url);
			}
			if(delo_id == 1003) {
				//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - надзорные жалобы';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1003';
				loadXMLDoc1(url);
			}
			if(delo_id == 1002) {
				//document.getElementById('inst1').innerHTML='Поиск по гражданским делам - надзорные дела';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1002';
				loadXMLDoc1(url);
			}
			if(delo_id == 1500001) {
				//document.getElementById('inst1').innerHTML='Поиск по административным делам - первая инстанция';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1500001';
				loadXMLDoc1(url);
			}
			if(delo_id == 1502001) {
				//document.getElementById('inst1').innerHTML='Поиск по административным делам - первый пересмотр';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1502001';
				loadXMLDoc1(url);
			}
			if(delo_id == 1513001) {
				//document.getElementById('inst1').innerHTML='Поиск по административным делам - второй пересмотр';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1513001';
				loadXMLDoc1(url);
			}
			if(delo_id == 2550001) {
				//document.getElementById('inst1').innerHTML='Поиск по административным делам - надзор';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=2550001';
				loadXMLDoc1(url);
			}
			if(delo_id == 1006) {
				//document.getElementById('inst1').innerHTML='Поиск по административным делам - надзорные жалобы';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1006';
				loadXMLDoc1(url);
			}
			if(delo_id == 1008) {
				//document.getElementById('inst1').innerHTML='Поиск по административным делам - надзорные дела';
				//document.getElementById('inst2').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1008';
				loadXMLDoc1(url);
			}
			if(delo_id == 1610001) {
				//document.getElementById('inst1').innerHTML='Поиск по материалам';
				//document.getElementById('inst2').style.display='none';
				//document.getElementById('inst').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1610001';
				loadXMLDoc1(url);
			}
			if(delo_id == 1610002) {
				//document.getElementById('inst1').innerHTML='Поиск по материалам';
				//document.getElementById('inst2').style.display='none';
				//document.getElementById('inst').style.display='none';
				url = '/modules.php?name=sud_delo&srv_num=' + srv_num + '&name_op=sf&nc=1&delo_id=1610002';
				//alert(url);
				loadXMLDoc1(url);
			}
		}
		else {
			alert("Не выбран вид производства");
			document.getElementById('inst1').innerHTML = 'Для поиска по решениям необходимо выбрать вид производства';
			if(document.getElementById('case_type1').options[document.getElementById('case_type1').selectedIndex].value == 0)
				document.getElementById('inst').style.display = 'block';
			else
				document.getElementById('inst').style.display = 'none';
			document.getElementById('inst2').style.display = 'block';
			document.getElementById('search_content').style.display = 'none';
		}
		hidePopupDiv();

	}

}

function select_case_type(n_n) {
	var num1;
	num1 = document.getElementById('case_type1').options[document.getElementById('case_type1').selectedIndex].value;
	switch(num1) {
		case '0':
			alert("Не выбрана инстанция");
			document.getElementById('delo_id').innerHTML = '<select id="delo_id1" style="width:100%" onchange="select_delo_id()"><option value="0">-- производство --</option><option value="1610001"> Производство по материалам</option></select>';
			document.getElementById('inst').style.display = 'block';
			document.getElementById('inst2').style.display = 'block';
			document.getElementById('search_content').style.display = 'none';
			document.getElementById('case_type1').focus();
			break;
		case '1':
			document.getElementById('delo_id').innerHTML = '<select id="delo_id1" style="width:100%" onchange="select_delo_id()"><option value="0">-- производство --</option><option value="1540006">Производство по уголовным делам</option><option value="1540005">Производство по гражданским делам</option><option value="1500001">Материалы об административных правонарушениях</option></select>';
			document.getElementById('inst').style.display = 'none';
			document.getElementById('inst2').style.display = 'block';
			document.getElementById('search_content').style.display = 'none';
			break;
		case '2':
			document.getElementById('delo_id').innerHTML = '<select id="delo_id1" style="width:100%" onchange="select_delo_id()"><option value="0">-- производство --</option><option value="1540006">Уголовные дела</option><option value="1540005">Гражданские дела</option><option value="1502001">Материалы об административных правонарушениях</option></select>';
			document.getElementById('inst').style.display = 'none';
			document.getElementById('inst2').style.display = 'block';
			document.getElementById('search_content').style.display = 'none';
			break;
		case '3':
			document.getElementById('delo_id').innerHTML = '<select id="delo_id1" style="width:100%" onchange="select_delo_id()"><option value="0">-- производство --</option><option value="4">Уголовные дела</option><option value="5">Гражданские дела</option><option value="1513001">Материалы об административных правонарушениях</option></select>';
			document.getElementById('inst').style.display = 'none';
			document.getElementById('inst2').style.display = 'block';
			document.getElementById('search_content').style.display = 'none';
			break;
		case '4':
			if(n_n == 1) {
				document.getElementById('delo_id').innerHTML = '<select id="delo_id1" style="width:100%" onchange="select_delo_id()"><option value="0">-- производство --</option><option value="2450001">Уголовный надзор</option><option value="2800001">Гражданский надзор</option><option value="2550001">Административный надзор</option></select>';
				document.getElementById('inst').style.display = 'none';
				document.getElementById('inst2').style.display = 'block';
				document.getElementById('search_content').style.display = 'none';
			}
			else {
				document.getElementById('delo_id').innerHTML = '<select id="delo_id1" style="width:100%" onchange="select_delo_id()"><option value="0">-- производство --</option><option value="6">Жалобы по уголовным делам</option><option value="8">Уголовные дела</option><option value="1003">Жалобы по гражданским делам</option><option value="1002">Гражданские дела</option><option value="1006">Жалобы по административным делам</option><option value="1008">Материалы об административных правонарушениях</option></select>';
				document.getElementById('inst').style.display = 'none';
				document.getElementById('inst2').style.display = 'block';
				document.getElementById('search_content').style.display = 'none';
			}
			break;
		default :
			document.getElementById('delo_id').innerHTML = '<select id="delo_id1" style="width:100%" onchange="select_delo_id()"><option value="0">-- производство --</option></select>';
			document.getElementById('inst').style.display = 'block';
			document.getElementById('inst2').style.display = 'block';
			document.getElementById('search_content').style.display = 'none';
	}
}

function openPrintWin(contentTable) {
	myWin = open("", "displayWindow",
		"width=800,height=600,status=no,toolbar=no,menubar=no, resizable=Yes, scrollbars=yes");
	// открыть объект document для последующей печати
	myWin.document.open();
	// генерировать новый документ
	myWin.document.write("<html><head><title>Документ для печати");
	myWin.document.write("</title><link href='modules/sud_delo/css/styleSDP.css' type='text/css' rel='stylesheet'><meta http-equiv='Content-Type' content='text/html; charset=windows-1251'></head><body style='background-image: url(/images/none.gif);'>");
	myWin.document.write("<div id=divSDPcontainer>");
	myWin.document.write("<a href='javascript:window.print()'>Печать</a><br>");
	myWin.document.write("<Table id=tablcont border=0 cellpadding=3 cellspacing=0>" + contentTable.innerHTML + "</table>");
	myWin.document.write("</div></body></html>");
	myWin.document.close();
}

function openPrintWinHearing(Header, contentTable) {
	myWin = open("", "_blank",
		"width=800,height=600,status=no,toolbar=no,menubar=no, resizable=Yes, scrollbars=yes");
	// открыть объект document для последующей печати
	myWin.document.open();
	// генерировать новый документ
	myWin.document.write("<html><head><title>Документ для печати");
	myWin.document.write("</title><link href='modules/sud_delo/css/styleSDP.css' type='text/css' rel='stylesheet'><meta http-equiv='Content-Type' content='text/html; charset=windows-1251'></head><body>");
	myWin.document.write("<div id=divSDPcontainer>");
	myWin.document.write("<a href='javascript:window.print()'>Печать</a><br>");
	myWin.document.write("<div align='center'><font size='5'>" + Header.innerHTML + "</font></div>");
	myWin.document.write("<Table width=100% id=tablcont border=0 cellpadding=3 cellspacing=0>" + contentTable.innerHTML + "</table>");
	myWin.document.write("</div></body></html>");
	myWin.document.close();
}

function index(n, m) {
	for(i = 1; i <= m; i++) {
		document.getElementById('tab' + i).className = 'nonsel';
		document.getElementById('cont' + i).style.display = 'none'
	}
	document.getElementById('tab' + n).className = 'sel';
	document.getElementById('cont' + n).style.display = 'block';
}
