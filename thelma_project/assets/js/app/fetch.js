$(document).ready(function(){
    /**
     * @author David Kauffman
     * @summary Fetch and Analysis Tool for JWST Mnemonics
     * @module TBD
     */
    // TODO: convert to es6 standard.
    // var Terminal = require('xterm').Terminal;
    /** The THELMA namespace declaration */
    const THELMA = {} || THELMA;

    //const socket ;

    // socket.onopen = function(event){
    //     console.log('Socket Open')
    // };



    THELMA.Fetch = {

        currentMnemonic: null,
        init: function(){
            this.onClickSubmit();
            this.getStatsTableMarkup('default');
            this.initTerminal();
            this.onSelectTab();
        },

        /**
         * This function initialzies the Datatable for dispalying statistics data for
         * each mnemonic.
         * @see https://datatables.net/
         */
        initStatisticTable: function(){

            $('#mnemonicStatisticsTable').DataTable().destroy();

            var five = {
                name: 'five-min',
                text: '5min',
                visibility: false,
                action: function(){
                    console.log("Selected 5min Stats");
                    if (THELMA.Fetch.currentMnemonic != null){
                        $('#mnemonicStatisticsTable').DataTable().destroy();
                        THELMA.Fetch.getStatsTableMarkup(THELMA.Fetch.currentMnemonic, '5min');
                    }
                },
            }

            var daily = {
                name: 'daily',
                text: 'Daily',
                visibility: false,
                action: function(){
                    console.log("Selected Daily Stats");
                    if (THELMA.Fetch.currentMnemonic != null){
                        $('#mnemonicStatisticsTable').DataTable().destroy();
                        THELMA.Fetch.getStatsTableMarkup(THELMA.Fetch.currentMnemonic, 'daily');
                    }
                },
            }

            $('#mnemonicStatisticsTable').DataTable({
                dom: "<'row'<'small-6 columns'l><'small-6 columns'f>Br>"+
                     "t"+
                     "<'row'<'small-6 columns'i><'small-6 columns'p>>",
                buttons: [
                    {
                        extend: 'collection',
                        text: 'Stats Interval',
                        buttons: [five, daily],
                        className: 'tiny margin-left',
                    },
                    {
                        text: 'Plot (min/mean/max)',
                        className: 'tiny margin-left',
                        action: function(){

                            $.ajax({
                                url:'/stats-plot/',
                                method: 'get',
                                data:{'mnemonic': $('#mnemonic').val()},
                                success: function(response){
                                    $('#plot').html(response);
                                },
                                error: function(xhr, status, error){
                                    new Noty({
                                        type: 'error',
                                        text: 'Cannot plot min/mean/max check logs.'
                                    }).show();
                                }
                            });
                        }
                    },
                    {
                        extend: 'copy',
                        text: 'Copy',
                        className: 'tiny margin-left',
                    },
                    {
                        extend: 'csv',
                        text: 'CSV',
                        className: 'tiny margin-left',
                    },
                    {
                        extend: 'print',
                        text: 'Print',
                        className: 'tiny margin-left',
                    }
                ],
                scrollY: "200px",
                scrollCollapse: true,
                pageLength: 5,
            });
        },

        initTerminal: function(){


            const term = new Terminal({
                cursorBlink: true,
                macOptionIsMeta: true,
                scrollback: true,
            });
            // const fitAddon = FitAddon();
            // term.loadAddon(fitAddon);

            term.open(document.getElementById('terminal'));

            console.log(`size: ${term.cols} columns, ${term.rows} rows`)

            term.write('Connecting to \x1B[1;3;31mjSka\x1B[0m ... ')
            term.onKey((event, ev) => {
                // console.log("Event Object:", event);
                // socket.send(event.key);
            });

            // socket.onmessage = function(event){
            //     console.log('Message from Socket', event.data)
            //     term.write(event.data)
            // };
        },

        /**
         *
         * @param {*} data
         */

         getStatsTableMarkup: function(mnemonic = 'default', interval = '5min'){
            $.ajax({
                url: $(`#${interval}StatsMarkup`).attr('data-url'),
                method: 'get',
                data: {
                    mnemonic: mnemonic,
                },
                success: function(html){
                    $('#mnemonicStatisticsTable').html(html);
                    THELMA.Fetch.initStatisticTable();
                },
                error: function(){

                }
            });
         },

         /**
         * A function for creating a plot with Plotly
         * @param {json} data - A json Object containing both the data to plot as well as
         * instructions for how to plot it.
         */
        plot: function(data){

            $('#plot').text('');

            var layout = {
                title: data[0]['mnemonic'],
                showlegend: false
            };

            options = {
                responsive: true,
                redisplayModeBar: true,
                displaylogo: false,
                displayModebar: true
            }

            Plotly.newPlot('plot', data, layout, options);
        },

        onSelectTab: function(){
            $('#example-tabs').off('change.zf.tabs');
            $('#example-tabs').on('change.zf.tabs', function() {
                $('#mnemonicStatisticsTable').DataTable().draw();
           });
        },

        /** This function binds the onClick event for fetching mnemonic data */
        onClickSubmit: function(){
            $('#submit').off('click');
            $('#submit').on('click', function(){

                $('#ingestLoadingSpinner').removeClass('no-display');

                mnemonic = String(document.getElementById('mnemonic').value)
                THELMA.Fetch.currentMnemonic = mnemonic;

                start_of_range = String(document.getElementById('startOfRangeInput').value)
                end_of_range = String(document.getElementById('endOfRangeInput').value)

                dataURL = $('#mnemonic-data').attr('data-url');
                $.ajax({
                    url: dataURL,
                    method: 'get',
                    data: {
                        mnemonic: mnemonic,
                        start_of_range: start_of_range,
                        end_of_range: end_of_range,
                    },
                    success: function(json){
                        $('#ingestLoadingSpinner').addClass('no-display');
                        THELMA.Fetch.plot(json)
                        THELMA.Fetch.getStatsTableMarkup(mnemonic);
                    },
                    error: function(xhr, status, error){
                        $('#ingestLoadingSpinner').addClass('no-display');
                        var noty = new Noty(
                            {
                                text: String($.parseJSON(xhr.responseText)['error']),
                                type: 'error'
                            }
                        ).show();
                    },
                });

            });
        },

    };


THELMA.Fetch.init();

});