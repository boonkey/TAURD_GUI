var isBrowserReady = false;

var speedGauge;
var rpmGauge;
var breakingGauge;
var throttleGauge;
var wingPosGauge;


var $speedLabel;
var $rpmLabel;
var $breakingLabel;
var $throttleLabel;
var $wingPosLabel;


/**
 * Handle UI elements when doc is ready
 */
$(document).ready(function(){


    // speed
    var gauge = $("#speedGauge");

    var target = gauge.find(".gauge")[0]; // your canvas element
    speedGauge = new Gauge(target).setOptions(SpeedGaugeOptions); // create sexy speedGauge!
    speedGauge.maxValue = 120; // set max speedGauge value
    speedGauge.setMinValue(0);  // Prefer setter over speedGauge.minValue = 0
    speedGauge.animationSpeed = 3;
    speedGauge.set(0); // set actual value
    $speedLabel = gauge.find('.display').find('label')[0];

    // rpm
    gauge = $("#rpmGauge");

    target = gauge.find(".gauge")[0]; // your canvas element
    rpmGauge = new Gauge(target).setOptions(rpmGaugeOptions); // create sexy speedGauge!
    rpmGauge.maxValue = 8000; // set max speedGauge value
    rpmGauge.setMinValue(0);  // Prefer setter over speedGauge.minValue = 0
    rpmGauge.animationSpeed = 3;
    rpmGauge.set(1); // set actual value
    $rpmLabel = gauge.find('.display').find('label')[0];

    // breaking
    gauge = $("#breakingGauge");

    target = gauge.find(".gauge")[0]; // your canvas element
    breakingGauge = new Gauge(target).setOptions(breakingGaugeOptions); // create sexy speedGauge!
    breakingGauge.maxValue = 100; // set max speedGauge value
    breakingGauge.setMinValue(0);  // Prefer setter over speedGauge.minValue = 0
    breakingGauge.animationSpeed = 3;
    breakingGauge.set(0); // set actual value
    $breakingLabel = gauge.find('.display').find('label')[0];


    // throttle
    gauge = $("#throttleGauge");

    target = gauge.find(".gauge")[0]; // your canvas element
    throttleGauge = new Gauge(target).setOptions(throttleGaugeOptions); // create sexy speedGauge!
    throttleGauge.maxValue = 100; // set max speedGauge value
    throttleGauge.setMinValue(0);  // Prefer setter over speedGauge.minValue = 0
    throttleGauge.animationSpeed = 3;
    throttleGauge.set(0); // set actual value
    $throttleLabel = gauge.find('.display').find('label')[0];

    // wingPos
    gauge = $("#wingPosGauge");

    target = gauge.find(".gauge")[0]; // your canvas element
    wingPosGauge = new Gauge(target).setOptions(wingPosGaugeOptions); // create sexy speedGauge!
    wingPosGauge.maxValue = 100; // set max speedGauge value
    wingPosGauge.setMinValue(-100);  // Prefer setter over speedGauge.minValue = 0
    wingPosGauge.animationSpeed = 3;
    wingPosGauge.set(0); // set actual value
    $wingPosLabel = gauge.find('.display').find('label')[0];
});

updateGauge = function(gaugeData) {
    console.log('new gauge data');
    console.log(gaugeData);


    speedGauge.set(parseFloat(gaugeData.speed));
    $speedLabel.innerHTML = gaugeData.speed;

    rpmGauge.set(parseFloat(gaugeData.rpm));
    $rpmLabel.innerHTML = gaugeData.rpm;

    breakingGauge.set(parseFloat(gaugeData.breaking));
    $breakingLabel.innerHTML = gaugeData.breaking;

    throttleGauge.set(parseFloat(gaugeData.throttle));
    $throttleLabel.innerHTML = gaugeData.throttle;

    wingPosGauge.set(parseFloat(gaugeData.wing_position));
    $wingPosLabel.innerHTML = gaugeData.wing_position;
};

/**
 * get request
 */
function getGaugeUpdate(){
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/?task=1',
        success: function(data) {
            updateGauge(data)
        },
        error: function(){S
            console.log("bulbul")
        }
    });
}

setInterval(function () {
    getGaugeUpdate()
}, 50);