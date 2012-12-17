$(document).ready(function() {
	var widgetContents = $('.widget-content');

	// loop through all the widget contents to check for size
	for(var i=0; i<widgetContents.length; i=i+1)
	{
		var widgetContent = widgetContents[i].innerHTML;
		// clear out whitespace
		widgetContent = trim11(widgetContent);
		
		if (widgetContent.length > 10) {
			// grab the font size in the CSS so that we don't have to modify the JS every time we modify CSS
			var fontSize = $(widgetContents[i]).css('font-size');
			// strip out the last two characters, which are "px" and will prevent calculating
			fontSize = fontSize.substr(0,fontSize.length-2);

			// set the new font size so that the string can fit comfortably in the div
			fontSize = (fontSize-(widgetContent.length*0.5))+'px';
			$(widgetContents[i]).css('font-size', fontSize);
		}
	}

	/* Persona Code */
	$('#signin').click(function() {
		navigator.id.request();
	});

	$('#signout').click(function () {
		console.log("CLICK");
		navigator.id.logout();
	});

	navigator.id.watch({
		onlogin: function(assertion) {
			$.ajax({
				type: 'POST',
				url: '/auth/login',
				data: {assertion: assertion},
				success: function(res, status, xhr) {
					console.log('Logged in!');
					console.log(res);
					console.log(status);
					$('#logged_out').css('visibility', 'hidden');
					$('#logged_in').css('visibility', 'visible');
				},
				error: function(xhr, status, err) { console.log("Login failure: " + err); }
			});
		},
		onlogout: function() {
			$('#logged_out').css('visibility', 'visible');
			$('#logged_in').css('visibility', 'hidden');
			$.ajax({
				type: 'POST',
				url: '/auth/logout',
				success: function(res, status, xhr) { window.location.reload(); },
				error: function(xhr, status, err) { console.log("Logout failure: " + err); }
			});
		}
	});
});

/**
 * Trim the whitespace around characters
 */
function trim11 (str) {
    str = str.replace(/^\s+/, '');
    for (var i = str.length - 1; i >= 0; i--) {
        if (/\S/.test(str.charAt(i))) {
            str = str.substring(0, i + 1);
            break;
        }
    }
    return str;
}

