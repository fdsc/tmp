var type_sear = false;
var elem;

function ajax_box(param, element) {

	var bool = false;
	$.ajax({
		async: false,
		url: '/modules.php?name=sud_delo',
		data: param,
		type: 'GET',
		beforeSend: function () {
			$(element).html('<div class="ajaxLoading">»дет загрузка данных...</div>');
		},
		success: function (data) {
			bool = true;
			$(element).html(data);
		},
		error: function (data, status, e) {
			$(element).html('ќшибка ответа сервера');
		}
	});
	return bool;
}

function getDicRow(type, element) {
	elem = element;
	//if(type_sear!==type){
	//if(ajax_box({'vidpr':type,'act':'ajax_search_srp'},'#poptxt'))
	type_sear = type;
	//}
	$('#poptxt').append('<div id="ajax_DicRow"></div>');
	ajax_box({'vidpr': type, 'act': 'ajax_search_srp'}, '#poptxt #ajax_DicRow')
	modWin("open", "ajax_DicRow");
}

function subOpense(pn) {
//$("#sublevel-"+pn).show();
	var el = document.getElementById('sublevel-' + pn);
	el.style.display = 'block';
	if(el.innerHTML.length == 0)
		ajax_box({'vidpr': type_sear, 'act': 'ajax_search_srp', 'pn': pn}, el)
}

function subViewse(pn, elem) {
	if(!document.getElementById('sublevel-' + pn).style.display || document.getElementById('sublevel-' + pn).style.display == 'block') {
		//$('#sublevel-'+pn).hide();
		document.getElementById('sublevel-' + pn).style.display = 'none';
		elem.innerHTML = '&nbsp;+&nbsp;';
	}
	else {
		subOpense(pn);
		elem.innerHTML = '&nbsp;Ц&nbsp;';
	}
}

function subClose(id) {
	$(document.getElementById('lwbart-' + id)).remove();
	$(document.getElementById('lwbart-txt-' + id)).remove();
	/*	var st=document.getElementById('lwbart-'+id);
	 if(st) {
	 var targetTd=st.parentNode;
	 targetTd.removeChild(st);
	 }

	 var st_text=document.getElementById('lwbart-txt-'+id);
	 if(st_text) {
	 var targetxt=st_text.parentNode;
	 targetxt.removeChild(st_text);
	 }
	 */
	//$('#lwbart-'+id+',#lwbart-txt-'+id).remove();
	//$('#lwbart-inp-'+id).removeAttr('checked');
	document.getElementById('lwbart-inp-' + id).checked = false;
}

/* function del_allse(){
 $('.lwbarthidden,.spanStShortTxt,.divStShortTxt').remove();
 }
 */
function changeSubmValuese(id, id_txt, obj) {
	var newStTxtEl;
	if(obj.checked) {
		$(elem).before("<input type='hidden' class='lwbarthidden' name='lawbookarticles[]' id='lwbart-" + id + "'>");
		document.getElementById("lwbart-" + id).value = id_txt;
		//	$("#lwbart-"+id).val(id_txt);
		if(type_sear != 2 && type_sear != 4) {
			newStTxtEl = "<div class='spanStShortTxt'  style='padding-bottom:5px; padding-left: 5px;' id='lwbart-txt-" + id + "'><a href=\"#\" onclick=\"subClose('" + id + "');return false;\" title=\"удалить\"><img src='/images/delete.gif' width='14'></a> <nobr>" + id_txt + "</nobr></div>";
		}
		else {
			newStTxtEl = "<div class='divStShortTxt' style='padding-bottom:5px; padding-left: 5px;' id='lwbart-txt-" + id + "'><a href=\"#\" onclick=\"subClose('" + id + "');return false;\" title=\"удалить\"><img src='/images/delete.gif' width='14'></a> " + id_txt + ";</div>";
		}
		$(elem).before(newStTxtEl);
	}
	else {
		subClose(id);
	}
}