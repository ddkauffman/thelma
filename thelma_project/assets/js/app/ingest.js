$(document).ready(function(){
        /**
         * @author David Kauffman
         * @summary TBD
         * @module TBD
         */

        const THELMA = {} || THELMA;

        THELMA.ingest = {

            taskId: null,
            archiveData: {},
            stagingAreaTable: null,
            statusCheckInterval: null,
            listOfIngestFiles: null,


            init: function(){
                THELMA.ingest.getStatistics();
                // THELMA.ingest.initStagingAreaTable(THELMA.ingest.archiveData.staging_dir_stats.sizes);
                THELMA.ingest.initEventHandling();
            },
            initEventHandling: function(){
                THELMA.ingest.onClickStartIngest();
                THELMA.ingest.onClickSubmitScheduleIngestUpdate();
            },
            initCheckIngestStatus: function(){
                $.ajax(
                    {
                        url: $('#ingest-status').attr('data-url'),
                        method: 'get',
                        data: {'task_id': THELMA.ingest.taskId},
                        success: function(json){
                            if (json['complete'] == true || json['failed'] == true){
                                clearInterval(THELMA.ingest.statusCheckInterval)
                                $('#startIngestButton').removeAttr('disabled')
                                $('#lastIngestEndTime').text(moment(json['end_time']).format('YYYY-MM-DD HH:mm:ss'));
                                $('#ingest-spinner').addClass('no-display');
                                THELMA.ingest.getStatistics();
                            }

                            console.log(json['task_inspection']);
                            $('#currentIngestStatus').text(json['state']);
                            $('#currentIngestStatus').removeClass();
                            $('#currentIngestStatus').addClass(String(json['state']).toLowerCase());
                        },
                        error: function(xhr, error, status){
                           console.log('error getting status');
                        }
                });
            },
            setNumberOfMnemonicsInArchive: function(numberOfMnemonics){
                $('#numberOfMnemonicsInArchive').text(numberOfMnemonics);
            },
            setArchiveSize: function(archiveSize){
                $('#archiveSize').text(numeral(archiveSize).format('0.00b'));
            },
            setStagingSize: function(stagingSize){
                $('#stagingSize').text(numeral(stagingSize).format('0.00b'));
            },
            setNumberOfStagedFiles: function(numberOfFiles){
                $('#numberOfFilesStaged, #ingestFilesToProcess').text(numberOfFiles);
            },
            getStatistics: function(){
                $.ajax({
                    url: $('#ingestStatistics').attr('data-url'),
                    method: 'get',
                    success: function(json){
                        THELMA.ingest.archiveData = json;
                        THELMA.ingest.setArchiveSize(THELMA.ingest.archiveData.archive_size);
                        THELMA.ingest.setStagingSize(THELMA.ingest.archiveData.staging_size);
                        THELMA.ingest.setNumberOfStagedFiles(THELMA.ingest.archiveData.staged_files.length);
                        THELMA.ingest.setNumberOfMnemonicsInArchive(THELMA.ingest.archiveData.number_of_mnemonics);
                        // THELMA.ingest.initStagingAreaTable(THELMA.ingest.archiveData.staging_dir_stats.sizes);
                    },
                });
            },
            initStagingAreaTable: function(dataSet){

                // if (THELMA.ingest.stagingAreaTable != null){
                //     //THELMA.ingest.stagingAreaTable.destory();
                // }

                THELMA.ingest.stagingAreaTable = $('#stagingAreaTable').DataTable({
                    data: dataSet,
                    columns: [
                        { title: "Ingest File" },
                        { title: "Size" },
                        { title: "Status" },
                    ],
                    columnDefs: [
                        {
                            "render": function ( data, type, row ) {

                                return data.replace(/^.*[\\\/]/, '');
                            },
                            "targets": 0
                        },
                        {
                            "render": function (data, type, row){
                                return numeral(data).format('0.00b');
                            },
                            "targets": 1
                        },
                        {
                            "render": function (data, type, row){
                                return "IDLE";
                            },
                            "targets": 2
                        },
                    ]
                });
            },

            testProcessProgress: function(ingestFile){
                return THELMA.ingest.listOfIngestFiles.indexOf(ingestFile) + 1;
            },
            setStatistics: function(json){

            },
            onClickSubmitScheduleIngestUpdate: function(){
                $('#submitScheduleIngestUpdate').off('click');
                $('#submitScheduleIngestUpdate').on('click', function(){
                    $.ajax({
                        url: $(this).attr('data-url'),
                        method: 'post',
                        data: {
                            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                        },
                        success: function(response){},
                        error: function(xhr, status, error){},
                    });
                });
            },
            onClickStartIngest: function(){
                $('#startIngestButton').off('click');
                $('#startIngestButton').on('click', function(){

                    $.ajax({
                        url: $(this).attr('data-url'),
                        method: 'post',
                        data: {
                            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                        },
                        success: function(response){

                            $('#nextScheduledIngest').text(moment().format('YYYY-MM-DD HH:mm:ss'));
                            $('#ingest-spinner').removeClass('no-display');
                            json = JSON.parse(response);

                            THELMA.ingest.taskId = json['task_id'];
                            THELMA.ingest.listOfIngestFiles = json['list_of_ingest_files']

                            $('#ingestFilesInProcessing').text(THELMA.ingest.listOfIngestFiles.length);
                            $('#ingestFilesProcessed').text(THELMA.ingest.testProcessProgress(THELMA.ingest.listOfIngestFiles[0]));

                            var noty = new Noty(
                                {
                                    text: THELMA.ingest.taskId,
                                    type: 'info'
                                }
                            );

                            noty.show();
                            $('#startIngestButton').attr('disabled', 'disabled')
                            THELMA.ingest.statusCheckInterval = setInterval(THELMA.ingest.initCheckIngestStatus, 2000);
                            $('#lastIngestStartTime').text(moment(JSON.parse(response)['end_time']).format('YYYY-MM-DD HH:mm:ss'));
                        },
                        error: function(xhr, status, error){
                            var noty = new Noty(
                                {
                                    text: 'error',
                                    type: 'error'
                                }
                            );
                            noty.show();
                        },
                    });
                });


            },
        }
        THELMA.ingest.init();
    });
