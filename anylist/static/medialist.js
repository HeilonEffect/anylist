var just = new JUST({root: "/static/view", useCache: false, ext: ".html"});
function select_genre (element) {
	var dict = url_resolve();
	// если мы отметили ранее не отмеченный элемент, то
	// добавляем в словарь новое значение, иначе - удаляем старое
	console.log(dict);
	if (element.checked) {
		console.log(element.id);
		var elem = element.id.split(":");
		if (dict[elem[0]].indexOf(elem[1]) == -1)
			dict[elem[0]].push(elem[1]);
	} else {
		var elem = element.id.split(":");
		console.log(dict);
		console.log(elem);
		// удаляем элемент, с которого снято выделение
		dict[elem[0]] = dict[elem[0]].filter(function(element) {
			return decodeURIComponent(element) != elem[1];
		});
		console.log(dict);
	}
	window.location.href = construct_url(dict);
}
function update_checkboxes(dict) {
	//var elements = $("");
	for (var i in dict['old_limit']) {
		var selector = "old_limit:" + dict['old_limit'][i];
		document.getElementById(selector).checked = true;
		//$("#old_limit:" + dict['old_limit'][i]).attr("checked", true);
	}
	for (var i in dict['genres']) {
		var selector = '#genres:' + dict['genres'][i];
		selector = "genres:" + dict['genres'][i];
		document.getElementById(decodeURIComponent(selector)).checked = true;
	}
}
function url_resolve() {
	// сначала получаем в форме словаря текущий урл
	// (в словарь проще добавить в нужное место изменения)
	var keys = ['old_limit', 'genres'];	// добавлять по мере надобности новые категории
	var current_url = document.location.pathname;
	var dict = {};
	var arr = current_url.split("/").slice(3);
	if (arr.length == 0) {
		// обрабатываем ситуацию, когда фильтры ещё не применялись
		dict['old_limit'] = [];
		dict['genres'] = [];
	} else {
		// ситуация, когда либо жанров, либо рейтинга нет
		// тогда мы добавляем их
		arr = arr.filter(function(element) {
			return element;
		});
		for (var i = 0; i < arr.length; i += 2) {
			dict[arr[i]] = arr[i + 1].split(",");
		}
		for (var i in keys) {
			if (!(keys[i] in dict))
				dict[keys[i]] = [];
		}
	}
	return dict;
}
function show_menu () {
	var global_menu = $("#global_menu");
	if (global_menu.css("display") == "none")
		global_menu.css("display", "block");
	else
		global_menu.css("display", "none");
}
function show_panel() {
	var left_menu = $("#left_menu");
	if (left_menu.css("display") == 'none') {
		left_menu.css("display", 'block');
		$("main").css("right", "11.6em");
	} else {
		left_menu.css("display", "none");
		$("main").css("right", "0");
	}
}

function construct_url(dict) {
	// конструируем новый url (позже сделать его универсальным)
	// на основе старого + изменения
	var category = window.location.pathname.split("/")[1];
	var new_url = '/' + category + '/filter/';
	for (var key in dict) {
		if (dict[key].length) {
			new_url += key + '/';
			for (var i in dict[key]) {
				new_url +=  dict[key][i] + ','
			}
			new_url = new_url.slice(0, new_url.length - 1) + '/';
		}
	}
	if (new_url == '/' + category + '/filter/')
		new_url = '/' + category;
	return new_url;
}

/*
	Отображает различные блоки, относящиеся к странице продукта
	Например, блок для боковой менюшки, переключающейся между разделами
	карточки продукта:
	infoBlockModule.renderLeftMenu("nav");
*/
var infoBlockModule = (function () {
	var link = window.location.pathname.split("/");
	var pre_url = [link[1], link[2]].join("/");
	// Для переключения между разделами
	var dict = {
		Main: pre_url,
		Series: [pre_url, "series"].join("/"),
		Heroes: [pre_url, "heroes"].join("/"),
		Creators: [pre_url, "creators"].join("/")
	};
	return {
		renderLeftMenu: function (tag) {
			just.render(
				"info_block",
				{dict: dict, url: window.location.pathname.slice(1)},
				function (err, html) {
					if (!err) {
						$(tag).append(html);
					} else {
						console.log(err);
					}
				}
			);
		}
	}
}());
var authFormModule = (function () {
	var id = "auth_form";
	var id1 = "#auth_form";
	var pos;
	return {
		render: function(tag) {
			pos = tag;
			$(tag).html("<form id='" + id + "'></form>");
			$(id1).append("<input name='username' type='text' placeholder='Username'>");
			$(id1).append("<input name='password' type='password' placeholder='Password'>");
			$(id1).append("<input name='email' type='email' placeholder='E-mail'>");
			$(id1).append("<input type='submit' value='Log In'>");
			$(id1).append("<input type='checkbox' id='is_reg'><label for='is_reg'>Register Me</label>");
			$(id1).submit(function () {
				var check = document.getElementById("is_reg").checked;
				var url = "login";
				if (check)
					url = "register";
				$.ajax({
					url: url,
					data: $(id1).serialize(),
					type: "POST"
				}).done(function () {
					var link = window.location.pathname;
					console.log(link);
					if (link.endsWith("/"))
						window.location.pathname = link + url;
					else
						window.location.pathname = link + "/" + url;
				});
				return false;
			});
		},
		hide: function () {
			$(pos).hide();
		},
		show: function () {
			$(pos).show();
		},
		hide_else_show: function () {
			if ($(pos).css("display") == "none")
				$(pos).show();
			else
				$(pos).hide();
		}
	}
}());

var addToListModule = (function () {
	return {
		renderStatusBlock: function (tag, statuses, active) {
			// отрисовывает статус промотра
			just.render(
				"status_block",
				{statuses: statuses, active: active},
				function (err, html) {
					if (!err) {
						$(tag).append(html);
						
						var activeEl = $(".status-select.active");

						$(".status-select").click(function (eventObject) {
							var val = eventObject.target.textContent;
							if (!$(this).attr("class").endsWith("active")) {
								if (activeEl)
									$(activeEl).attr("class", ".status-select");
								$(this).attr("class", ".status-select active");
								activeEl = this;
								$.post(
									window.location.pathname + "/status",
									"name=" + val
								);
							}
						});
					} else {
						console.log(err);
					}
				}
			);
		}
	}
}());

var addToListModule1 = (function () {
	var id = "add_to_list_el";
	var arr = ["Planned", "Watch", "ReWatching", "Watched", "Dropped", "Deffered"];
	var option_id;
	var url = window.location.pathname;
	var product = window.location.pathname.split("/")[2].split("-")[0];
	var _renderBlock = function (tag, active) {
			$(tag).append("<div id='" + id + "'><span class='bord_block'>Actions</span></div>");

			arr.map(function (element) {
				if (element == active)
					$("#" + id).append("<br><span class='actions active'>" + element + "</span>");
				else
					$("#" + id).append("<br><span class='actions'>" + element + "</span>");
			});
			$(".actions").click(function (eventObject) {
				$.post(
					window.location.pathname + "/status",
					"name=" + eventObject.target.textContent
				).done(function () {
					eventObject.target.style.background = "gray";
				});
			});
		}
	var _renderDelSetting = function (tag) {
		$("#" + option_id).append("<span id='remove_from'>Remove from list</span>");
		$("#remove_from").click(function () {
			$.post(
				window.location.pathname + "/remove_from_list"
			).done(function () {
				$("#add_to_list_el").remove();
				$("#remove_from").remove();
				_renderAddSetting(tag);
			});
		});
	}
	var _renderAddSetting = function (tag) {
		$("#" + option_id).append("<span id='add_to_list'>Add to list</span>");
		$("#add_to_list").click(function () {
			$.post(
				"/mylist/add",
				"product=" + product
			).done(function () {
				$("#add_to_list").remove();
				_renderDelSetting(tag);
				_renderBlock(tag);
			});
		});
	}
	return {
		renderBlock: function (tag, active) {
			_renderBlock(tag, active);
		},
		renderSetting: function (tag, is_list) {
			$(tag).append('<p id="' + option_id + '">Options</p>');
			if (is_list != "None")
				_renderDelSetting(tag);
			else
				_renderAddSetting(tag);
		},
		renderRecord: function (tag) {
			$(tag).append('<p id="add_to_list">Add To List</p>');
			$("#add_to_list").click(function () {
				var product = window.location.pathname.split("/")[2].split("-")[0];
				$.post(
					"/mylist/add",
					"product=" + product
				).done(function () {
					_renderBlock(tag, arr[0]);
				});
			});
		}
	}
}());
