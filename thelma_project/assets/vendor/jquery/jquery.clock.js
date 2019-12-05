(function( $ ) {
    $.fn.extend({
        clock: function(options) {
            var clocks = this;

            var defaults = { utc: true, utc_label: true, interval: 500  };
            options = $.extend(defaults, options);

            setInterval(function(){ update_clock(); }, options.interval);

            function update_clock() {
                var today = new Date();
                var value = "";

                if ( options.utc ) {
                    value = today.toUTCString();

                } else {
                    value = today.toString();
                }

                if ( options.utc_label ) {
                    value = value.replace("GMT", "UTC");
                }

                clocks.each(function(){
                    this.innerHTML = value;
                });
            }
        }
    });
})( jQuery );