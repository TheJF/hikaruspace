$(document).ready(function() {

function fitText() {
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

function dashboardInit() {
    console.log("Initializing dashboard...");
    $.ajax({
        url: "dashboard.json",
    }).done(function( data ) {
        widgets = JSON.parse(data);
        console.log(widgets);

        for (var i=0; i<widgets.length; i++) {
            var widget = renderWidget(widgets[i]);
            $('#widgetbox').append(widget);
        }
        fitText();

    });
}

function dashboardUpdate(message) {
    console.log("Updating dashboard...");
    // Double check it has the correct message
    if (message['command_type'] == 'dashboard_update') {
        var widget = renderWidget(message);

        // If the widget exists, replace it. If not, refresh the whole dashboard.
        var widget_id = '#widget-'+message['widget_num'];
        if ( $(widget_id).length ) {
            console.log('Updating widget...');
            $(widget_id).replaceWith(widget);

        } else {
            console.log('Refreshing dashboard...');
            dashboardInit();
        }
        //$('#widgetbox').html(widget);
        fitText();
    }
}

function renderWidget(widget) {
    var widget = ['<span id="widget-'+widget['widget_num']+'" class="widget status_'+widget['status']+'">',
                  '    <span id="widget-'+widget['widget_num']+'-title" class="widget-title">',
                  '        '+widget['label']+'',
                  '    </span>',
                  '    <span id="widget-'+widget['value']+'-content" class="widget-content">',
                  '        '+widget["value"]+'',
                  '    </span>',
                  '</span>'
                 ].join('\n');
    return widget;
}

/**
 * Web Socketry
 */

var ws = new WebSocket("ws://{{ template_info['host'] }}:{{ template_info['port'] }}/interface_data");
ws.onopen = function() {
    ws.send("update");
};
ws.onmessage = function (evt) {
    var message = evt.data;
    message = JSON.parse(message);
    
    if (message['command_type'] == 'dashboard_update') {
        dashboardUpdate(message);
    }

};

dashboardInit();
fitText();

});
