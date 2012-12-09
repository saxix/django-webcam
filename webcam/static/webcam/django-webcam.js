function SingleMonitor(options) {
    if (typeof window.cameramonitor != "undefined") {
        return;
    }
    options = (typeof options == 'undefined') ? {} : options;
    options.format = (typeof options.format == 'undefined') ? 'jpeg' : options.format;
    options.width = (typeof options.width == 'undefined') ? 320 : options.width;
    options.height = (typeof options.height == 'undefined') ? 240 : options.height;
    options.swffile = (typeof options.swffile == 'undefined') ? 'jscam.swf' : options.swffile;
    options.quality = (typeof options.quality == 'undefined') ? 85 : options.quality;
    options.mode = (typeof options.mode == 'undefined') ? 'callback' : options.mode;

    console.log('initialize single monitor', options);
    $("body").append('<div id="webcam-monitor">' +
            '<div class="camera-frame">' +
            '</div>' +
            '<form id="camera-commands" class="camera">' +
            '<input type="button" class="btn snap" value="Snap" />' +
            '<input type="button" class="btn cancel" value="Cancel" />' +
            '</form>' +
            '</div>');
    window.cameramonitor = this;
    var $webcam_monitor = $("#webcam-monitor");
    $("#webcam-monitor .cancel").click(function (event) {
        console.log('hiding monitor');
        $("#webcam-monitor").hide();
        event.stopPropagation();
    });
    this.clear = function (widget, monitor) {
        widget.attr('value', '-1');
        monitor.attr('src', '');
    };
    this.show_monitor = function (format, widget, monitor) {
        console.log('showing monitor for', widget, monitor);
        var pos = 0, ctx = null, saveCB, image = [];
        var canvas = document.createElement("canvas");
        canvas.setAttribute('width', options.width);
        canvas.setAttribute('height', options.height);
        ctx = canvas.getContext("2d");
        image = ctx.getImageData(0, 0, options.width, options.height);

        $webcam_monitor.show();
        window.webcam.init();

        $("#webcam-monitor .snap").unbind('click').click(function (event) {
            window.webcam.onSave = function (data) {
                var col = data.split(";");
                var img = image;

                for (var i = 0; i < options.width; i++) {
                    var tmp = parseInt(col[i]);
                    img.data[pos + 0] = (tmp >> 16) & 0xff;
                    img.data[pos + 1] = (tmp >> 8) & 0xff;
                    img.data[pos + 2] = tmp & 0xff;
                    img.data[pos + 3] = 0xff;
                    pos += 4;
                }
                if (pos >= 4 * options.width * options.height) {
                    console.log(pos);
                    ctx.putImageData(img, 0, 0);
                    var png = canvas.toDataURL("image/" + format)
                    monitor.attr('src', png);
                    widget.attr('value', png);
                    pos = 0;
                }
            };
            window.webcam.capture();
            $("#webcam-monitor").hide();
            event.stopPropagation();
        });
    };

    $("#webcam-monitor .camera-frame").webcam({
        width:options.width,
        height:options.height,
        quality:options.quality,
        swffile:options.swffile,
        onCapture:function () {
            webcam.save()
        }
    });
}
