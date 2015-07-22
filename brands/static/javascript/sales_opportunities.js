function bindCatSelection(divElem) {
    divElem.find('ul.dropdown-menu li').click(function() {
        divElem.find('button strong').text($(this).children('a').text());
        var selectedCatId = $(this).children('span.hidden').text();
        
        // The following line will show category id on URL, such as:?cat1=1&cat2=128&cat3=142
        // __IMPORTANT__, This shall be controlled by global variable in python: if g_URL_SHOW_CAT_ID_OR_NAME == 0
        //divElem.children('input[type="text"]').val(selectedCatId);
        
        // The following line will show category name on URL, such as:?cat1=Agriculture&cat2=Agricultural+equipment&cat3=Fishing+equipment
        // This shall be controlled by global variable in python: if g_URL_SHOW_CAT_ID_OR_NAME == 1
        divElem.children('input[type="text"]').val($(this).children('a').text());

        var nextDiv = divElem.next('div');
        if (nextDiv.length) {
            fillNextCat(nextDiv, selectedCatId);
        }
    });
    var reqVal = divElem.children('label.hidden').text();
    if (reqVal != '') {
        var reqLi = divElem.find('li').filter(function() {
            return $(this).children('span.hidden').text() == reqVal;
        });
        if (reqLi.length > 0) {
            reqLi.click();
        }
    }
}

function fillNextCat(nextDiv, catId) {
    var api = nextDiv.children('img.hidden').prop('name');
    $.get('/member-service/' + api + '/' + catId).done(function(data) {
        var ulElem = nextDiv.children('ul');
        ulElem.children().slice(1).remove();
        ulElem.children().first().click();
        if (data.length > 0) {
            $(data).each(function (idx, item) {
                $('<li><span class="hidden">' + item['id'] + '</span><a>' + item['eng_kw'] + '</a></li>').appendTo(ulElem);
            });
            nextDiv.children('button').removeClass('disabled');
        }
        else {
            nextDiv.children('button').addClass('disabled');
        }
        bindCatSelection(nextDiv);
    });
}

function createTrendChart(summary_div, divs, titles, names, datum, colorIndices) {
    summary_div.children().remove();
    summary_div.highcharts('StockChart', createChartDict('Demand and Supply For The Product Category in China', names, datum, colorIndices));
    summary_div.highcharts().reflow();
    for (var i = 0; i < divs.length; i++) {
        var div = divs[i];
        div.children().remove();
        div.highcharts('StockChart', createChartDict(titles[i], [names[i]], [datum[i]], [colorIndices[i]]));
        div.highcharts().reflow();
    }
}

function createChartDict(title, names, datum, colorIndices) {
    var chartDict = {
        title: { text: title },
        rangeSelector: { selected: 1 },
        yAxis: { minRange: 0 },
        series: []
    };
    for (var i = 0; i < names.length; i++) {
        var color = Highcharts.getOptions().colors[colorIndices[i]];
        var seriesOptions = {
            name: names[i],
            data: datum[i],
            color: color
        };
        if (names.length == 1) {
            seriesOptions.type = 'area';
            seriesOptions.fillColor = {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [ [0, color], [1, Highcharts.Color(color).setOpacity(0).get('rgba')] ]
            };
            chartDict.navigator = {
                series: { lineColor: color }
            };
        }
        chartDict.series.push(seriesOptions);
    }
    chartDict.plotOptions = {
        line: { shadow: true }
    };
    return chartDict;
}
