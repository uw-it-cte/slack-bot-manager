/* canvas course admin desktop javascript */

/*jslint browser: true, plusplus: true, regexp: true */
/*global $, jQuery, Handlebars, Highcharts, moment, alert, confirm, startImportMonitoring, stopImportMonitoring */


"use strict";


$(document).ready(function () {

    // prep for api post/put
    $.ajaxSetup({
        headers: { "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val() }
    });

    function format_date(dt) {
        return (dt !== null) ? moment(dt).format("MM/DD/YYYY h:mm a") : '';
    }

    function toggleBot() {
	    var input = $(this);
        $.ajax({
            url: 'botmgr/api/v1/bot/' + encodeURIComponent(input.attr('data-bot-id')),
            contentType: 'application/json',
            type: 'PUT',
            processData: false,
            data: '{"bot": {"is_active": ' + $(this).is(':checked') + '}}',
            success: function (data) {
		        if (data.hasOwnProperty('bot')) {
		            input.closest('td').prev()
                         .html(format_date(data.bot.changed_date) +
                               ' (' + data.bot.changed_by + ')');
		        }
            },
            error: function (xhr) {
                var json;
                try {
                    json = $.parseJSON(xhr.responseText);
                    console.log('Event service error:' + json.error);
                } catch (e) {
                    console.log('Unknown bot service error');
                }
            }
        });
    }

    function refreshSlackBotList() {
        $.ajax({
            url: 'botmgr/api/v1/bots',
            dataType: 'json',
            success: function (data) {
                var tpl = Handlebars.compile($('#bot-table-row').html()),
                    context = {bots: []};
                if (data.hasOwnProperty('bots')) {
                    $.each(data.bots, function () {
                        var bot = this;
                        context.bots.push({
                            bot_id: this.bot_id,
                            name: bot.name,
                            description: bot.description,
                            is_active: bot.is_active ? true : false,
                            changed_by: bot.changed_by ? bot.changed_by : '',
                            changed_date: bot.changed_date ? format_date(bot.changed_date) : ''
                        });
                    });
                    $('#bots-table tbody').html(tpl(context));
                    $('#bots-table tbody input.toggle-bot').each(function () {
                        $(this).bootstrapToggle().change(toggleBot);
                    });
                    $('#bots-table').dataTable({
                        'aaSorting': [[ 0, 'asc' ]],
                        'bPaginate': false,
                        'searching': false,
			            'bScrollCollapse': true
                    });
                }
            },
            error: function (xhr) {
                var json;
                try {
                    json = $.parseJSON(xhr.responseText);
                    console.log('admin service error:' + json.error);
                } catch (e) {
                    console.log('Unknown admin service error');
                }
            }
        });
    }

    refreshSlackBotList();

});
