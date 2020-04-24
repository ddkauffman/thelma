$(document).ready(function(){

    const THELMA = {} || THELMA;

    THELMA.Base = {

        init: function(){
            this.initUTCClock();
            this.setDayOfYear();
            this.onClickAboutModal();
        },

         /** @method Creates a instance of a UTC clock for the entire app */
        initUTCClock: function() {
            $('#utc-clock').clock();
        },

        getDayOfYear: function() {
            const now = new Date();
            const start = new Date(now.getFullYear(), 0, 0);
            const diff = now - start;
            const oneDay = 1000 * 60 * 60 * 24;
            const doy = Math.floor(diff / oneDay);

            return doy;
        },

        setDayOfYear: function() {
            const dayOfYearText = String(this.getDayOfYear()) + ' DOY';
            $('#day-of-year').text(dayOfYearText);
        },

        onClickAboutModal: function(){

            $('#js-about-button').off('click');
            $('#js-about-button').on('click', function(event){
                event.preventDefault();

                $.ajax({
                    url: window.location + 'core/api/info',
                    method: 'get',
                    success: function(response){
                        $('#js-about-modal-content').html(response);
                        $('#js-about-modal').foundation('open');
                        $('#js-about-modal').blur();
                    },
                    error: function(){
                        new Noty({
                            text: 'Error: failed to get info',
                            type: 'error',
                        });
                    }
                });
            });
        },
    }

    THELMA.Base.init();

});