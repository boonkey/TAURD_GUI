// all gauge objects stored here
var gauges = {}

// flag for if gauges are ready for manipulation
var gaugesReady = false;

/**
 * Handle UI elements when doc is ready
 */
$(document).ready(function () {
    //get all gauge info
    getGaugeInfo();

    //get constant updates
    setInterval(function () {
        getGaugeUpdate();
    }, 50);

});

// static variables for timeout counter
var getInfoTimeoutCounter = 0;
var getInfoTimeoutThreshold = 50;
/**
 * AJAX request all meta data of the gauges
 */
function getGaugeInfo() {

    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/?task=get_info',
        success: function (data) {
            if (!gaugesReady) {
                createGauges(JSON.parse(data));
                gaugesReady = true;
            }
        },
        error: function () {
            console.log("Failure to get info")

            if (getInfoTimeoutCounter >= getInfoTimeoutThreshold) {
                console.log('retry' + ++getInfoTimeoutCounter);
                getGaugeInfo();
            } else {
                console.log('get gauge info timeout, failed ' + getInfoTimeoutThreshold + ' times');
            }
        }
    });
}

/**
 * creates all the gauges received from server
 * @param {all the info on all the gauges to be created} gaugeInfo 
 */
function createGauges(gaugeInfo) {
    for (var sensor in gaugeInfo) {
        if (gaugeInfo.hasOwnProperty(sensor)) {
            var sensorInfo = gaugeInfo[sensor];
            var container = TauGauge.addNewGaugeElement(sensorInfo['name']);
            gauges[sensorInfo['name']] = new TauGauge(sensorInfo['name'], sensorInfo['low_val'], sensorInfo['high_val'], sensorInfo['value']);
        }
    }
}

/**
 * AJAX request to get updated gauge values
 */
function getGaugeUpdate() {
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/?task=get_data',
        success: function (data) {
            if (gaugesReady) {
                updateAllGauges(JSON.parse(data));
            }

        },
        error: function () {
            console.log("Failure to get data")
        }
    });
}

/**
 * updates gauges with data from the server
 * @param {updated values from gauges} newValues 
 */
function updateAllGauges(newValues) {
    for (var sensor in newValues) {
        if (newValues.hasOwnProperty(sensor)) {
            gauges[sensor].updateGauge(newValues[sensor]);
        }
    }
}