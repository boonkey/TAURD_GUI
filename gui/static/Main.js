var hasGotInfo = false;

var speedGauge;
var rpmGauge;
var brakingGauge;
var throttleGauge;
var wingPosGauge;

var gauges = {}
var gaugeOptions = {
    "speed": SpeedGaugeOptions,
    "rpm": rpmGaugeOptions,
    "braking": brakingGaugeOptions,
    "throttle": throttleGaugeOptions,
    "wing_position": wingPosGaugeOptions,
}

var gaugeUnits = {
    "speed": "Kmph",
    "rpm": "rpm",
    "braking": "%",
    "throttle": "%",
    "wing_position": "°",
}

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

var getInfoTimeoutCounter = 0;
var getInfoTimeoutThreshold = 50;
function getGaugeInfo() {
    
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/?task=get_info',
        success: function (data) {
            if(!hasGotInfo){
                createGauges(JSON.parse(data));
                hasGotInfo = true;
            }
        },
        error: function () {
            console.log("Failure to get info")
            
            if(getInfoTimeoutCounter >= getInfoTimeoutThreshold) {
                console.log('retry' + ++getInfoTimeoutCounter);
                getGaugeInfo();
            } else {
                console.log('get gauge info timeout, failed '+ getInfoTimeoutThreshold +' times');
            }
        }
    });
}

function createGauges(gaugeInfo) {
    for (var sensor in gaugeInfo) {
        if (gaugeInfo.hasOwnProperty(sensor)) {
            var sensorInfo = gaugeInfo[sensor];
            var container = TauGauge.addNewGaugeElement(sensorInfo['name']);
            gauges[sensorInfo['name']] = new TauGauge(sensorInfo['name'], sensorInfo['low_val'], sensorInfo['high_val'], sensorInfo['value']);
        }
    }
}

function getGaugeUpdate() {
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/?task=get_data',
        success: function (data) {
            if(hasGotInfo) {
                updateAllGauges(JSON.parse(data));
            }
            
        },
        error: function () {
            console.log("Failure to get data")
        }
    });
}

function updateAllGauges(newValues) {
    for (var sensor in newValues) {
        if (newValues.hasOwnProperty(sensor)) {
            gauges[sensor].updateGauge(newValues[sensor]);
        }
    }
}