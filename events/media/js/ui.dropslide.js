/*
  jQuery ui.dropslide - 0.4
  http://code.google.com/p/jquery-utils/

  (c) Maxime Haineault <haineault@gmail.com> 
  http://haineault.com

  MIT License (http://www.opensource.org/licenses/mit-license.php

*/

(function($) {
    $.widget('ui.dropslide', $.extend({}, $.ui.mouse, {
        getter: 'showLevel showNextLevel getSelection',
        _init: function() {
            var widget   = this;
            this.wrapper = this.element.next();

            this.element.bind(this.options.trigger +'.dropslide', function(){
                widget.show();
            });
            this.wrapper
                .data('dropslide', this)
                .css({width:this.options.width})
                .find('li, li ol li')
                    .bind('mouseover.dropslide', function(e){
                        $(this).siblings().removeClass('hover')
                            .find('ol').hide().end()
                            .find('span').removeClass('ui-state-hover').end();
                        $(this).find('ol').show().end().addClass('hover').children(0).addClass('ui-state-hover');
                        widget.showNextLevel();
                    })
                   .bind('click.dropslide', function(e){
                        $(widget.element).triggerHandler('dropslideclick', [e, widget], widget.options.click); 
                        $(widget.element).triggerHandler('select', [e, widget], widget.options.select); 
                    }).end()
                .find('ol')
                    .bind('mousemove.dropslide', function(e){
                       return widget._redraw();
                    })
                   .addClass('ui-widget ui-helper-clearfix ui-helper-reset')
                   .hide().end()
                .find('span').addClass('ui-state-default ui-corner-all');

            this._redraw();
        },

        // show specified level, id is the DOM position
        showLevel: function(id) {
            var ols = this.wrapper.find('ol');
            var ds  = this;
            if (id == 0) {            
                ols.eq(0).css('left', this.element.position().left);
                this.wrapper.css('top', ds.element.position().top + ds.element.height() + ds.options.top);
                this.wrapper.css('z-index', 1000);
            }
            setTimeout(function() {
                ols.removeClass('active').eq(id).addClass('active').show(ds.options.animSpeed);
            }, ds.options.showDelay);
        },

        // guess what it does
        showNextLevel: function() {
            this.wrapper.find('ol.active')
                .removeClass('active')
                .next('ol').addClass('active').show(this.options.animSpeed);
        },

        getSelection: function(level) {
            return level 
                    && this.wrapper.find('ol').eq(level).find('li span.ui-state-hover')
                    || $.makeArray(this.wrapper.find('span.ui-state-hover').map($.iterators.getText));
        },

        // essentially reposition each ol
        _redraw: function() {
            var prevLI ,prevOL, nextOL, pos = false;
            var offset = this.element.position().left + this.options.left;
            var ols    = $(this.wrapper).find('ol');

            $(this.wrapper).css({
                top: this.element.position().top + this.element.height() + this.options.top,
                left: this.element.position().left
            });
            
            // reposition each ol
            ols.each(function(i) {
                prevOL = $(this).prevAll('ol:visible:first');
                if (prevOL.get(0)) {
                    prevLI = prevOL.find('li.hover').get(0) && prevOL.find('li.hover') || prevOL.find('li:first');
                    $(this).css('margin-left', prevLI.position().left);
                }
            });
        },

        // show level 0 (shortcut)
        show: function(e) {
            this.showLevel(0);
        },

        // hide all levels
        hide: function() {
            var widget = this;
            setTimeout(function() {
                widget.wrapper.find('ol').hide();
            }, widget.options.hideDelay);
        },

        activate: function(e) {
            this.element.focus();
            this.show(this.options.animSpeed);
        },
                  
        destroy: function(e) {
            this.wrapper.remove();
        }
    }));

    $.ui.dropslide.defaults = {
        // options
        tree:      false,
        trigger:   'mouseover',
        top:       6,
        left:      0,
        showDelay: 0,
        hideDelay: 0,
        animSpeed: 0,
        // events
        select:  function() {},
        click:   function(e, ui) { ui.hide(); }
    };
})(jQuery);
