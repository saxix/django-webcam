function base64_encode(s) {
    var base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.split("");
    var r = '';
    var p = '';
    var c = s.length % 3;
    if (c > 0) {
        for (; c < 3; c++) {
            p += '=';
            s += '\0';
        }
    }
    for (c = 0;
        c < s.length;
        c += 3
    ) {
        if (c > 0 && (c / 3 * 4) % 76 == 0) {
            r += '\r\n';
        }
        var n = (
            (s.charCodeAt(c) << 16) +
            (s.charCodeAt(c+1) << 8) +
            s.charCodeAt(c+2)
        );
        n = [
            (n >>> 18) & 63,
            (n >>> 12) & 63,
            (n >>> 6) & 63,
            n & 63
        ];
        r += (
            base64chars[n[0]] +
            base64chars[n[1]] +
            base64chars[n[2]] +
            base64chars[n[3]]
        )
    }
    return r.substring(0, r.length - p.length) + p
}

function Webcam(options /* { parent, width, height, swffile, quality, mode } */) {
    webcam = this; // avoids 'this' confusion in event handlers
    var source = (
        '<object id="XwebcamXobjectX" '+
            'type="application/x-shockwave-flash"'+
            ' data="' + options.swffile + '"'+
            ' width="' + options.width + '"'+
            ' height="' + options.height + '"'+
        '>'+
            '<param name="movie" value="' +  options.swffile + '" />'+
            '<param name="FlashVars" value="mode=' +  options.mode + '&amp;quality=' +  options.quality + '" />'+
            '<param name="allowScriptAccess" value="always" />'+
        '</object>'
    );
    $cam = $(source);
    options.parent.append($cam);
    webcam.onLoad = function () {
        cam = document.getElementById('XwebcamXobjectX')
        webcam.setCamera = function (camera_index) {
            return cam.setCamera(camera_index);
        };
        webcam.getCameraList = function () {
            return cam.getCameraList();
        };
        webcam.capture = function (use_data) {
            webcam.use_data = use_data;
            return cam.capture();
        };
        webcam.save = function () {
            return cam.save();
        };
        webcam.onCapture = function () {
            cam.save()
        };
        options.onLoad(cam)
    };
    webcam.debug = function(message_type, message) {
        console.debug(message_type, message)
    };
    webcam.capturedPhoto = function (jpeg_data) {
        webcam.use_data(jpeg_data)
    }
}

function CameraMonitor(options /* { width, height, swffile, quality, mode } */) {
    try {
        if (typeof window.cameramonitor != "undefined") {
            return window.cameramonitor
        }
        else {
            window.cameramonitor = this;
            var _ = gettext;
            $("body").append(
                $(
                    '<div id="webcam-monitor-layer">'+
                        '<div id="webcam-monitor">'+
                            '<div id="camera-frame" class="camera">'+
                                '<div id="camera-flv" class="camera"></div>'+
                            '</div>'+
                            '<form id="camera-commands" class="camera">'+
                                '<input type="button" id="camera-snap" class="btn" value="Snap" />'+
                                '<input type="button" id="camera-cancel" class="btn" value="Cancel" />'+
                            '</form>'+
                        '</div>'+
                    '</div>'
                )
            );
            $("#webcam-monitor-layer").click(function (event) {
                $("#webcam-monitor-layer").hide();
                event.stopPropagation()
            });
            $("#camera-cancel").click(function (event) {
                $("#webcam-monitor-layer").hide();
                event.stopPropagation()
            });
            $("#webcam-monitor").click(function (event) {
                event.stopPropagation()
            });
            var webcam = new Webcam({
                parent: $("#camera-flv"),
                width: options.width,
                height: options.height,
                mode: "callback",
                swffile: options.swffile,
                onLoad: function (camera) {
                    // show camera drop down
                    $("#camera-commands").show();
                    var cameras = camera.getCameraList();
                    $("#cams").remove();
                    if (cameras.length > 1) {
                        var $camera_select = $('<select id="cams"></select>');
                        for(var i in cameras) {
                            var $camera_option = $("<option value='"+i+"'>" + cameras[i] + "</option>");
                            $camera_select.append($camera_option);
                            jQuery("#camera-commands").append($camera_select);
                        }
                        $camera_select.change(function (event) {
                            event.stopPropagation();
                            var camera_index = parseInt($camera_select.attr("value"));
                            webcam.setCamera(camera_index)
                        })
                    } else {
                        if (cameras.length == 0) {
                            alert("No camera detected!")
                        }
                    }
                }
            });
            var $snap = $("#camera-snap");
            $snap.click(function (event) {
                webcam.capture()
            });
            var $webcam_monitor_layer = $("#webcam-monitor-layer");
            this.show_monitor = function(widget, monitor) {
                var $widget_input = $("#"+widget);
                var $widget_monitor = $("#"+monitor);
                $widget_input.attr("value", "");
                $webcam_monitor_layer.show();
                $snap.unbind('click');
                $snap.click(
                    function(event) {
                        webcam.capture(
                            /* Tried to do this in a setTimeout so as to give the user back control of the UI
                            * whilst the jpeg capture takes place (by hiding the flash).
                            * However, this doesn't work as the flash seems to need to be showing whilst capturing.
                            * */
                            function (jpeg_hex_string) {
                                var jpeg_bytes = new Array(jpeg_hex_string);
                                for (var i = 0, len=jpeg_hex_string.length;i<len;i+=2) {
                                    jpeg_bytes[i/2] = String.fromCharCode(parseInt("0x"+jpeg_hex_string.substr(i,2)))
                                }
                                var base64_jpeg_data = base64_encode(jpeg_bytes.join(""));
                                var base64_jpeg_data_uri = "data:image/jpeg;base64,"+base64_jpeg_data;
                                $widget_input.attr('value', base64_jpeg_data_uri);
                                $widget_monitor.attr('src', base64_jpeg_data_uri)
                            }
                        );
                        $webcam_monitor_layer.hide();
                        event.stopPropagation();
                    }
                );
                $snap.focus()
            }
        }
    }
    catch (exception) {
        console.debug(exception)
        throw exception
    }
}
