XMLHttp.prototype.targetDiv = null;
XMLHttp.prototype.targetURL = null;
XMLHttp.prototype.xmlObj = null;
XMLHttp.prototype.showLoading = true;
XMLHttp.prototype.executeFunctionOnFinish = null;
XMLHttp.prototype.createXmlObj = function () {
	try {
		this.xmlObj = new XMLHttpRequest();
	}
	catch (e) {
		var vers = ['MSXML2.XMLHTTP.6.0', 'MSXML2.XMLHTTP.5.0', 'MSXML2.XMLHTTP.4.0', 'MSXML2.XMLHTTP.3.0', 'MSXML2.XMLHTTP', 'Microsoft.XMLHTTP'];
		for(var i = 0; i < vers.length && !this.xmlObj; i++) {
			try {
				this.xmlObj = new ActiveXObject(vers[i]);
			}
			catch (e) {
			}
		}
	}
};
XMLHttp.prototype.getInfo = function () {
	this.transerState = false;
	if(this.xmlObj && this.targetDiv && this.targetURL) {
		if(this.showLoading == true) this.targetDiv.innerHTML = "<div class='ajaxLoading'>Идет загрузка данных...</div>";
		try {
			var parentObj = this;
			this.xmlObj.open('GET', this.targetURL, true);
			this.xmlObj.onreadystatechange = function () {
				if(parentObj.targetDiv && parentObj.xmlObj && parentObj.xmlObj.readyState == 4 && parentObj.xmlObj.status == 200) {
					try {
						parentObj.targetDiv.innerHTML = parentObj.xmlObj.responseText;
						if(parentObj.executeFunctionOnFinish) parentObj.executeFunctionOnFinish();
					}
					catch (e) {
						parentObj.targetDiv.innerHTML = 'Ошибка чтения ответа от сервера.';
					}
				}
			};
			this.xmlObj.send(null);
		}
		catch (e) {
			this.targetDiv.innerHTML = 'Ошибка отправки HTTP запроса.';
		}
	}
	else {
		if(this.targetDiv) this.targetDiv.innerHTML = 'Невозможно создать XMLHTTP объект! Обновите ваш браузер.';
	}
};

function XMLHttp(targetDivId) {
	if(document.getElementById(targetDivId)) {
		this.targetDiv = document.getElementById(targetDivId);
		if(arguments.length == 2 && arguments[1] == false) this.showLoading = false;
		this.createXmlObj();
	}
}