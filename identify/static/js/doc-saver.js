/* FileSaver.js
 * A saveAs() FileSaver implementation.
 * 1.3.2
 * 2016-06-16 18:25:19
 *
 * By Eli Grey, http://eligrey.com
 * License: MIT
 *   See https://github.com/eligrey/FileSaver.js/blob/master/LICENSE.md
 */

/*global self */
/*jslint bitwise: true, indent: 4, laxbreak: true, laxcomma: true, smarttabs: true, plusplus: true */

/*! @source http://purl.eligrey.com/github/FileSaver.js/blob/master/FileSaver.js */

var saveAs = saveAs || (function (view) {
    "use strict";
    // IE <10 is explicitly unsupported
    if (typeof view === "undefined" || typeof navigator !== "undefined" && /MSIE [1-9]\./.test(navigator.userAgent)) {
        return;
    }
    var
        doc = view.document
        // only get URL when necessary in case Blob.js hasn't overridden it yet
        , get_URL = function () {
            return view.URL || view.webkitURL || view;
        }
        , save_link = doc.createElementNS("http://www.w3.org/1999/xhtml", "a")
        , can_use_save_link = "download" in save_link
        , click = function (node) {
            var event = new MouseEvent("click");
            node.dispatchEvent(event);
        }
        , is_safari = /constructor/i.test(view.HTMLElement)
        , is_chrome_ios = /CriOS\/[\d]+/.test(navigator.userAgent)
        , throw_outside = function (ex) {
            (view.setImmediate || view.setTimeout)(function () {
                throw ex;
            }, 0);
        }
        , force_saveable_type = "application/octet-stream"
        // the Blob API is fundamentally broken as there is no "downloadfinished" event to subscribe to
        , arbitrary_revoke_timeout = 1000 * 40 // in ms
        , revoke = function (file) {
            var revoker = function () {
                if (typeof file === "string") { // file is an object URL
                    get_URL().revokeObjectURL(file);
                } else { // file is a File
                    file.remove();
                }
            };
            setTimeout(revoker, arbitrary_revoke_timeout);
        }
        , dispatch = function (filesaver, event_types, event) {
            event_types = [].concat(event_types);
            var i = event_types.length;
            while (i--) {
                var listener = filesaver["on" + event_types[i]];
                if (typeof listener === "function") {
                    try {
                        listener.call(filesaver, event || filesaver);
                    } catch (ex) {
                        throw_outside(ex);
                    }
                }
            }
        }
        , auto_bom = function (blob) {
            // prepend BOM for UTF-8 XML and text/* types (including HTML)
            // note: your browser will automatically convert UTF-16 U+FEFF to EF BB BF
            if (/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(blob.type)) {
                return new Blob([String.fromCharCode(0xFEFF), blob], {type: blob.type});
            }
            return blob;
        }
        , FileSaver = function (blob, name, no_auto_bom) {
            if (!no_auto_bom) {
                blob = auto_bom(blob);
            }
            // First try a.download, then web filesystem, then object URLs
            var
                filesaver = this
                , type = blob.type
                , force = type === force_saveable_type
                , object_url
                , dispatch_all = function () {
                    dispatch(filesaver, "writestart progress write writeend".split(" "));
                }
                // on any filesys errors revert to saving with object URLs
                , fs_error = function () {
                    if ((is_chrome_ios || (force && is_safari)) && view.FileReader) {
                        // Safari doesn't allow downloading of blob urls
                        var reader = new FileReader();
                        reader.onloadend = function () {
                            var url = is_chrome_ios ? reader.result : reader.result.replace(/^data:[^;]*;/, 'data:attachment/file;');
                            var popup = view.open(url, '_blank');
                            if (!popup) view.location.href = url;
                            url = undefined; // release reference before dispatching
                            filesaver.readyState = filesaver.DONE;
                            dispatch_all();
                        };
                        reader.readAsDataURL(blob);
                        filesaver.readyState = filesaver.INIT;
                        return;
                    }
                    // don't create more object URLs than needed
                    if (!object_url) {
                        object_url = get_URL().createObjectURL(blob);
                    }
                    if (force) {
                        view.location.href = object_url;
                    } else {
                        var opened = view.open(object_url, "_blank");
                        if (!opened) {
                            // Apple does not allow window.open, see https://developer.apple.com/library/safari/documentation/Tools/Conceptual/SafariExtensionGuide/WorkingwithWindowsandTabs/WorkingwithWindowsandTabs.html
                            view.location.href = object_url;
                        }
                    }
                    filesaver.readyState = filesaver.DONE;
                    dispatch_all();
                    revoke(object_url);
                }
            ;
            filesaver.readyState = filesaver.INIT;

            if (can_use_save_link) {
                object_url = get_URL().createObjectURL(blob);
                setTimeout(function () {
                    save_link.href = object_url;
                    save_link.download = name;
                    click(save_link);
                    dispatch_all();
                    revoke(object_url);
                    filesaver.readyState = filesaver.DONE;
                });
                return;
            }
            fs_error();
        }
        , FS_proto = FileSaver.prototype
        , saveAs = function (blob, name, no_auto_bom) {
            return new FileSaver(blob, name || blob.name || "download", no_auto_bom);
        }
    ;
    // IE 10+ (native saveAs)
    if (typeof navigator !== "undefined" && navigator.msSaveOrOpenBlob) {
        return function (blob, name, no_auto_bom) {
            name = name || blob.name || "download";

            if (!no_auto_bom) {
                blob = auto_bom(blob);
            }
            return navigator.msSaveOrOpenBlob(blob, name);
        };
    }

    FS_proto.abort = function () {
    };
    FS_proto.readyState = FS_proto.INIT = 0;
    FS_proto.WRITING = 1;
    FS_proto.DONE = 2;

    FS_proto.error = FS_proto.onwritestart = FS_proto.onprogress = FS_proto.onwrite =
        FS_proto.onabort = FS_proto.onerror = FS_proto.onwriteend = null;
    return saveAs;
}(
    typeof self !== "undefined" && self
    || typeof window !== "undefined" && window
    || this.content
));
// `self` is undefined in Firefox for Android content script context
// while `this` is nsIContentFrameMessageManager
// with an attribute `content` that corresponds to the window

if (typeof module !== "undefined" && module.exports) {
    module.exports.saveAs = saveAs;
} else if ((typeof define !== "undefined" && define !== null) && (define.amd !== null)) {
    define([], function () {
        return saveAs;
    });
}

/* jquery-word-Export */
(function ($) {
    $.fn.wordExport = function (fileName, pixelRatio, no_clone) {
        fileName = typeof fileName !== 'undefined' ? fileName : "jQuery-Word-Export";
        var options = {
            make_mhtml: function (style_sheet, bodyhtml, bottom) {
                return ["Mime-Version: 1.0",
                    "Content-Base: " + location.href,
                    'Content-Type: Multipart/related;boundary="NEXT.ITEM-BOUNDARY";type="text/html"',
                    '',
                    '--NEXT.ITEM-BOUNDARY',
                    'Content-Type: text/html; charset="utf-8"',
                    "Content-Location: " + location.href,
                    '',
                    '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">',
                    "<style>",
                    style_sheet,
                    "</style></head><body>",
                    bodyhtml,
                    "</body></html>",
                    bottom,
                    "\n--NEXT.ITEM-BOUNDARY--"
                ].join('\n');
            },
            maxWidth: 550,
        };

        ec_option = {type: 'png', pixelRatio: pixelRatio || 3, backgroundColor: 'transparent'};

        var markup = $(doc_body = document.createElement('body'));
        doc_body.offsetWidth = options.maxWidth;
        doc_body.clientWidth = options.maxWidth;
        markup.html(no_clone ? this : $(this).clone());
        markup.each(function () {
            var self = $(this);
            if (self.is(':hidden'))
                self.remove();
        });
        markup.find('script').remove();
        markup.find('input').remove();
        markup.find('button').remove();
        markup.find('.nodoc').remove();
        // Embed all images using Data URLs

        var images = Array();

        markup.find('[_echarts_instance_],img').each(function (idx) {
            var h, w, uri;
            if (this.attributes._echarts_instance_) {
                chart = echarts.getInstanceByDom(this);
                W = chart.getWidth();
                uri = chart.getDataURL(ec_option);
                w = Math.min(W, options.maxWidth);
                h = chart.getHeight() * (w / W);
                //src = '#' + this.getAttribute('_echarts_instance_')
            } else {
                H = this.height || this.naturalHeight || parseInt(this.style.maxHeight);
                W = this.width || this.naturalWidth || parseInt(this.style.maxWidth);
                w = Math.min(W, options.maxWidth);
                h = H * (w / (W));
                var canvas = document.createElement("canvas");
                canvas.width = W;
                canvas.height = H;
                context = canvas.getContext('2d');
                context.drawImage(this, 0, 0, W, H);
                uri = canvas.toDataURL();
                //src = this.src
            }
            src = 'img_' + idx;
            $(this).after(img = document.createElement('img')).remove();
            img.style = 'margin:auto';
            img.src = src;
            img.width = w;
            img.height = h;
//       console.debug('id', ima, 'v', this, img.width, img.height);
            images.push(
                "\n--NEXT.ITEM-BOUNDARY" +
                "\nContent-Location: " + src +
                "\nContent-Type: " + uri.substring(uri.indexOf(":") + 1, uri.indexOf(";")) +
                "\nContent-Transfer-Encoding: " + uri.substring(uri.indexOf(";") + 1, uri.indexOf(",")) + "\n\n" +
                uri.substring(uri.indexOf(",") + 1) + ""
            );
        });

        var mhtmlBottom = images.join('\n');

        $.ajax({
            url: "/static/css/doc.min.css", type: 'get', async: false, cache: false, success: function (styles) {
                var fileContent = options.make_mhtml(styles, markup.html(), mhtmlBottom);
                var blob = new Blob([fileContent], {
                    type: "application/msword;charset=utf-8"
                });
                saveAs(blob, fileName + ".doc");
            }
        });
        markup.remove();
    };
})(jQuery);