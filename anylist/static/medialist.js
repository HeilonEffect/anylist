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
	var _renderStatusBlock = function (tag, active) {
		$.get("/api/status?format=json").done(function (data) {
			var statuses = data.map(function (element) {
				return element.name;
			});
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
		});
	};
	var command = {};
	command["Удалить из списка"] = function (element) {
		$.post(
			window.location.pathname + "/remove_from_list"
		).done(function () {
			element.textContent = "Добавить в список";
			$("section.status-options").remove();
			return true;
		});
		return false;
	}
	command["Добавить в список"] = function (element) {
		var product = window.location.pathname.split("/")[2].split("-")[0];
		console.log(product);
		$.post(
			"/add_to_list",
			"product=" + product
		).done(function (data) {
			element.textContent = "Удалить из списка";
			console.log(data)
			_renderStatusBlock("nav", "Planned");
			return true;
		});
		return false;
	}
	return {
		renderStatusBlock: function (tag, statuses, active) {
			_renderStatusBlock(tag, statuses, active);
		},
		renderOptionsBlock: function (tag, in_list) {
			just.render(
				"options_block",
				{in_list: in_list},
				function (err, html) {
					if (!err) {
						$(tag).append(html);
						$(".select-options").click(function (eventObject) {
							command[eventObject.target.textContent](eventObject.target);
						});
					} else {
						console.log(err);
					}
				}
			);
		}
	}
}());

// Рендеринг списка серий
// Сделано сразу так, что-бы при редактировании, когда требуется интерактивность
// не пихать html ручками в jQuery функции, как делалось в прошлых версиях
var seriesModule = (function () {
	_renderVolume = function (tag, number, is_auth, series, numbers) {
		just.render(
			"add_serie_form",
			{number: number, is_auth: is_auth, series: series, numbers: numbers},
			function (err, html) {
				if (!err) {
					$(tag).append(html);
					$(".strt").datetimepicker();
					
					// добавление новой серии
					$(".add-serie-form").submit(function (eventObject) {
						var season = eventObject.target.id;
						console.log(season);
						
						var result = [
							$(".add-serie-form").serialize(),"&season=", season].join();
						$.post(
							[window.location.pathname, "add"].join("/"),
							$(".add-serie-form").serialize() + "&season=" + season
						).done(function (data) {
							console.log(data);
						});
						return false;
					});
					// Добавление/удаление новой серии в список/из списка просмотренных
					$(".serie_action").click(function (eventObject) {
						var txt = eventObject.target.textContent;
						var num_serie = eventObject.target.parentElement.parentElement.id.split("-")[1];
						var product = window.location.pathname.split("/")[2].split("-")[0];
						var url = "";
						if (txt == "Добавить в список")
							url = "/mylist/series/add";
						else if (txt == "Удалить из списка")
							url = "/mylist/series/del";
						$.ajax({
							url: url,
							data: {
								number: num_serie,
								product: product,
								season: number
							},
							type: "POST"
						}).done(function () {
							if (url.endsWith("add"))
								eventObject.target.textContent = "Удалить из списка";
							else
								eventObject.target.textContent = "Добавить в список";
						});
					});

					// Изменение данных серии
					$(".serie_edit").click(function (eventObject) {
						var tr = eventObject.target.parentElement.parentElement;
						var num_serie = tr.id.split("-")[1];
						var num_season = tr.parentElement.parentElement.id.split("-")[1];
						tr = document.getElementById("s-" + num_serie);
						var dict = {number: "", name: "", start_date: "", length: ""};
						var ident;
						
						// Извлекаем текущие данные указанной серии
						var i = 0;
						for (var key in dict) {
							dict[key] = tr.children[i].textContent;
							i++;
						}
						// рендерим формочку для изменения данных указанной серии
						just.render("input_serie", dict, function (err, html) {
							if (!err) {
								// вставляем input'ы в таблицу
								$("#s-" + num_serie).html(html);
								$("#start_date").datetimepicker();
								$("#serie-update").click(function (eventObject) {
									// при нажатии на кнопку отправки данных проверяем,
									// действительно ли значения были изменены,
									// если это так - то отправляем данные
									i = 0;
									var update_flag = false;
									for (var key in dict) {
										var tmp = tr.children[i].children[0].value;
										if (dict[key] != tmp) {
											dict[key] = tmp;
											ident = num_serie;
											update_flag = true;
										}
										i++;
										if (i == 4)
											break;
									}
									// Логика для отправки измененных данных на сервер
									if (update_flag) {
										var lnk = window.location.pathname.split("/")[1];
										dict['product'] = window.location.pathname.split("/")[2].split("-")[0];
										dict['season'] = 1;
										dict['ident'] = ident;
										$.ajax({
											url: "/" + lnk + "/series/edit",
											data: dict,
											type: "POST"
										}).done(function (data) {
											if (data != "success") {
												// подсвечивание невалидных полей
												var keys = JSON.parse(data);
												for (var i in keys) {
													$("input[name='" + keys[i] + "'][class=dd_sr]").css("border-color", "red");
												}
											} else {
												// перерисовка с учетом новых данных
												just.render(
													"result_serie", dict,
													function (err, html) {
														if (!err) {
															$("#s-" + num_serie).html(html);
														} else
															console.log(err);
													});
											}
										});
									} else {
										just.render(
													"result_serie", dict,
													function (err, html) {
														if (!err) {
															$("#s-" + num_serie).html(html);
														} else
															console.log(err);
													});
									}
								});
							} else
								console.log(err);
						});
					});
				} else {
					console.log(err);
				}
			}
		);
	};
	return {
		renderVolume: _renderVolume
	}
}());
