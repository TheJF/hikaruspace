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


/**
 * Web Socketry
 */

var ws = new WebSocket("ws://moncton.zombievolk.com:9999/interface_data");
ws.onopen = function() {
    ws.send("update");
};
ws.onmessage = function (evt) {
  console.log(evt.data);  
};

});
