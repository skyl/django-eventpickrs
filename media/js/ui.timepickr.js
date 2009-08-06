/*
  jQuery ui.timepickr - @VERSION
  http://code.google.com/p/jquery-utils/

  (c) Maxime Haineault <haineault@gmail.com> 
  http://haineault.com

  MIT License (http://www.opensource.org/licenses/mit-license.php

  Note: if you want the original experimental plugin checkout the rev 224 

  Dependencies
  ------------
  - jquery.utils.js
  - jquery.strings.js
  - jquery.ui.js
  - ui.dropslide.js
  
*/

(function($) {
    $.tpl('timepickr.menu',   '<span class="ui-helper-reset ui-dropslide ui-timepickr ui-widget" />');
    $.tpl('timepickr.row',    '<ol class="ui-timepickr" />');
    $.tpl('timepickr.button', '<li class="{className:s}"><span>{label:s}</span></li>');

    $.widget('ui.timepickr', {
        _init: function() {
            var ui = this;
            var menu = ui._buildMenu();
            var element = ui.element;
            element.data('timepickr.initialValue', element.val());
            menu.insertAfter(ui.element);
            element
                .addClass('ui-timepickr')
                .dropslide(ui.options.dropslide)
                .bind('select', ui.select);
            
            element.blur(function(e) {
                $(this).dropslide('hide');
                if (ui.options.resetOnBlur) {
                    $(this).val($(this).data('timepickr.initialValue'));
                }
            });

            if (ui.options.val) {
                element.val(this.options.val);
            }

            if (ui.options.handle) {
                $(this.options.handle).click(function() {
                    $(element).dropslide('show');
                });
            }

            if (ui.options.resetOnBlur) {
                menu.find('li > span').bind('mousedown.timepickr', function(){
                    $(element).data('timepickr.initialValue', $(element).val()); 
                });
            }
            if (ui.options.updateLive) {
                menu.find('li').bind('mouseover.timepickr', function() {
                    $(element).timepickr('update'); 
                });
            }
            var hrs = menu.find('ol:eq(1)').find('li:first').addClass('hover').find('span').addClass('ui-state-hover').end().end();
            var min = menu.find('ol:eq(2)').find('li:first').addClass('hover').find('span').addClass('ui-state-hover').end().end();
            var sec = menu.find('ol:eq(3)').find('li:first').addClass('hover').find('span').addClass('ui-state-hover').end().end();

            if (this.options.convention === 24) {
                var day        = menu.find('ol:eq(0) li:eq(0)');
                var night      = menu.find('ol:eq(0) li:eq(1)');
                var dayHours   = hrs.find('li').slice(0, 12);
                var nightHours = hrs.find('li').slice(12, 24);
                var index      = 0;
                var selectHr   = function(id) {
                    hrs.find('li').removeClass('hover');
                    hrs.find('span').removeClass('ui-state-hover');
                    hrs.find('li').eq(id).addClass('hover').find('span').addClass('ui-state-hover')
                };

                day.mouseover(function() {
                    nightHours.hide();
                    dayHours.show(0);
                    index = hrs.find('li.hover').data('id') || hrs.find('li:first').data('id');
                    selectHr(index > 11 && index - 12 || index);
                    element.dropslide('redraw');
                });

                night.mouseover(function() {
                    dayHours.hide();
                    nightHours.show(0);
                    index = hrs.find('li.hover').data('id') || hrs.find('li:first').data('id');
                    selectHr(index < 12 && index + 12 || index);
                    element.dropslide('redraw');
                });
            }
            element.dropslide('redraw');
            element.data('timepickr', this);
        },

        update: function() {
            var frmt = this.options.convention === 24 && 'format24' || 'format12';
            var val = {
                h: this.getValue('hour'),
                m: this.getValue('minute'),
                s: this.getValue('second'),
                prefix: this.getValue('prefix'),
                suffix: this.getValue('suffix')
            };
            var o = $.format(this.options[frmt], val);

            $(this.element).val(o);
        },

        select: function(e) {
            var dropslide = $(this).data('dropslide');
            $(dropslide.element).timepickr('update');
            e.stopPropagation();
        },

        getHour: function() {
            return this.getValue('hour');
        },

        getMinute: function() {
            return this.getValue('minute');
        },

        getSecond: function() {
            return this.getValue('second');
        },

        getValue: function(type) {
            return $('.ui-timepickr.'+ type +'.hover', this.element.next()).text();
        },
        
        activate: function() {
            this.element.dropslide('activate');
        },

        destroy: function() {
            this.element.dropslide('destroy');
        },
        
        /* UI private methods */
        
        _createButton: function(i, format, className) {
            var o  = format && $.format(format, i) || i;
            var cn = className && 'ui-timepickr '+ className || 'ui-timepickr';
            return $.tpl('timepickr.button', {className: cn, label: o}).data('id', i);
        },

        _createRow: function(range, format, className) {
            var row = $.tpl('timepickr.row');
            var button = this._createButton;
            // Thanks to Christoph Müller-Spengler for the bug report
            $.each(range, function(idx, val){
                row.append(button(val, format || false, className || false));
            });
            return row;
        },
        
        _getRanges12: function() {
            var o = [], opt = this.options;
            if (opt.hours)   { o.push(this._createRow($.range(1, 13), '{0:0.2d}', 'hour')); }
            if (opt.minutes) { o.push(this._createRow(opt.rangeMin,   '{0:0.2d}', 'minute')); }
            if (opt.seconds) { o.push(this._createRow(opt.rangeSec,   '{0:0.2d}', 'second')); }
            if (opt.suffix)  { o.push(this._createRow(opt.suffix,     false,      'suffix')); }
            return o;
        },

        _getRanges24: function() {
            var o = [], opt = this.options;
            o.push(this._createRow(opt.prefix, false, 'prefix')); // prefix is required in 24h mode
            if (opt.hours)   { o.push(this._createRow($.range(0, 24),   '{0:0.2d}', 'hour')); }
            if (opt.minutes) { o.push(this._createRow(opt.rangeMin, '{0:0.2d}', 'minute')); }
            if (opt.seconds) { o.push(this._createRow(opt.rangeSec, '{0:0.2d}', 'second')); }
            return o;
        },

        _buildMenu: function() {
            var menu   = $.tpl('timepickr.menu');
            var ranges = this.options.convention === 24 
                         && this._getRanges24() || this._getRanges12();

            $.each(ranges, function(idx, val){
                menu.append(val);
            });
            return menu;
        }
    });

    // These properties are shared accross every instances of timepickr 
    $.extend($.ui.timepickr, {
        version:     '@VERSION',
        eventPrefix: '',
        getter:      '',
        defaults:    {
            convention:  24, // 24, 12
            dropslide:   { trigger: 'focus' },
            format12:    '{h:02.d}:{m:02.d} {suffix:s}',
            format24:    '{h:02.d}:{m:02.d}',
            handle:      false,
            hours:       true,
            minutes:     true,
            seconds:     false,
            prefix:      ['am', 'pm'],
            suffix:      ['am', 'pm'],
            rangeMin:    $.range(0, 60, 15),
            rangeSec:    $.range(0, 60, 15),
            updateLive:  true,
            resetOnBlur: true,
            val:         false
        }
    });

})(jQuery);
