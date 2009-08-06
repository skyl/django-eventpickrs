$(function(){
    $('#main').hide().html($('<input id="timepickr-test12" type="text"><input id="timepickr-test24" type="text">'));

    function setup(opt) {
        return $('<input type="text">').appendTo('#main').timepickr(opt);
    }

    module('ui.timepickr.js');

    test('initialization', function(){
        expect(9);
        var tp = setup();
        ok(tp.next().is(':hidden'),               'wrapper is hidden OK');
        ok(tp.next().hasClass('ui-helper-reset'), 'wrapper has class ui-helper-reset OK');
        ok(tp.next().hasClass('ui-widget'),       'wrapper has class ui-widget OK');
        ok(tp.next().hasClass('ui-timepickr'),    'wrapper has class ui-timepickr OK');
        equals(tp.next().find('ol').length, 3,    'ol length OK');
        equals(tp.next().find('ol:eq(0) li').length, 2,  'ol:eq(0) > li length OK');
        equals(tp.next().find('ol:eq(1) li').length, 24, 'ol:eq(1) > li length OK');
        equals(tp.next().find('ol:eq(2) li').length, 4,  'ol:eq(2) > li length OK');
        equals(tp.next().text(), 'ampm00010203040506070809101112131415161718192021222300153045', 'Data integrity OK');
        tp.remove();
    });

    test('options.convention', function(){
        expect(5);
        var tp = setup({convention: 12});
        equals(tp.next().find('ol').length, 3,    'ol length OK');
        equals(tp.next().find('ol:eq(0) li').length, 12,  'ol:eq(0) > li length OK');
        equals(tp.next().find('ol:eq(1) li').length, 4, 'ol:eq(1) > li length OK');
        equals(tp.next().find('ol:eq(2) li').length, 2,  'ol:eq(2) > li length OK');
        equals(tp.next().text(), '01020304050607080910111200153045ampm', 'Data integrity OK');
        tp.remove();
    });

    test('options.val', function(){
        expect(1);
        var tp = setup({val: '04:20'});
        equals(tp.val(), '04:20', 'val OK');
        tp.remove();
    });
    
    test('options.resetOnBlur', function(){
        expect(4);
        var tp = setup({resetOnBlur: true});
        var val = tp.val();
        tp.focus();
        tp.next().find('ol > li:eq(4)').mouseover();
        ok(tp.val() != val, 'val changed OK');
        tp.blur();
        equals(tp.val(), val, 'val reseted OK');
        tp.remove();
        
        var tp = setup({resetOnBlur: false});
        var val = tp.val();
        tp.focus();
        tp.next().find('ol > li:eq(4)').mouseover();
        ok(tp.val() != val, 'val changed OK');
        tp.blur();
        ok(tp.val() != val, 'val not reseted OK');
        tp.remove();
    });
    
    test('options.updateLive', function(){
        expect(4);
        var tp = setup({updateLive: true});
        var val = tp.val();
        tp.focus();
        tp.next().find('ol > li:eq(4)').mouseover();
        ok(tp.val() != val, 'val changed OK');
        tp.blur();
        equals(tp.val(), val, 'val reseted OK');
        tp.remove();
        
        var tp = setup({updateLive: false});
        var val = tp.val();
        tp.focus();
        tp.next().find('ol > li:eq(4)').mouseover();
        equals(tp.val(), val, 'val not changed OK');
        tp.blur();
        equals(tp.val(), val, 'val not changed OK');
        tp.remove();
    });

    test('options.rangeMin', function(){
        expect(2);
        var tp = setup();
        equals(tp.next().find('ol:eq(2) > li').text(), '00153045', 'defaults OK');
        tp.remove();
        var tp = setup({rangeMin: $.range(0, 60, 30)});
        equals(tp.next().find('ol:eq(2) > li').text(), '0030', 'custom OK');
        tp.remove();
    });

    test('options.rangeSec', function(){
        expect(2);
        var tp = setup({seconds: true});
        equals(tp.next().find('ol:eq(3) > li').text(), '00153045', 'defaults OK');
        tp.remove();
        var tp = setup({rangeSec: $.range(0, 60, 30), seconds: true});
        equals(tp.next().find('ol:eq(3) > li').text(), '0030', 'custom OK');
        tp.remove();
    });
    
    test('options.seconds', function(){
        expect(2);
        var tp = setup({seconds: true});
        equals(tp.next().find('ol').length, 4, 'ol OK')
        tp.remove();
        var tp = setup({seconds: false});
        equals(tp.next().find('ol').length, 3, 'ol OK')
        tp.remove();
    });
    
    test('options.minutes', function(){
        expect(2);
        var tp = setup({minutes: true});
        equals(tp.next().find('ol').length, 3, 'ol OK')
        tp.remove();
        var tp = setup({minutes: false});
        equals(tp.next().find('ol').length, 2, 'ol OK')
        tp.remove();
    });
    
    test('options.hours', function(){
        expect(2);
        var tp = setup({hours: true});
        equals(tp.next().find('ol').length, 3, 'ol OK')
        tp.remove();
        var tp = setup({hours: false});
        equals(tp.next().find('ol').length, 2, 'ol OK')
        tp.remove();
    });

    test('options.prefix', function(){
        expect(2);
        var tp = setup();
        equals(tp.next().find('ol:eq(0) > li').text(), 'ampm', 'defaults OK');
        tp.remove();
        var tp = setup({prefix: ['day','night']});
        equals(tp.next().find('ol:eq(0) > li').text(), 'daynight', 'custom OK');
        tp.remove();
    });

    test('options.suffix', function(){
        expect(2);
        var tp = setup({convention: 12});
        equals(tp.next().find('ol:eq(2) > li').text(), 'ampm', 'defaults OK');
        tp.remove();
        var tp = setup({convention: 12, suffix: ['day','night']});
        equals(tp.next().find('ol:eq(2) > li').text(), 'daynight', 'custom OK');
        tp.remove();
    });
});
