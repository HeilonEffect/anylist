function select_genre (element) {
	console.log(element.id + ',' + element.checked);
	$.load();
}
function show_menu () {
	var display = document.getElementById("global_menu").style.display;
	var opacity = document.getElementById("global_menu").style.opacity;
	if (display == 'none') {
		document.getElementById("global_menu").style.display = 'block';
		document.getElementById("global_menu").style.opacity = 1;
	} else {
		document.getElementById("global_menu").style.display = 'none';
		document.getElementById("global_menu").style.opacity = 0;
	}
}