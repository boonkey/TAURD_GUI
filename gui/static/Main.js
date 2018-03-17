var isBrowserReady = false;

var textBox;
var gauge;
var $speedLabel;

var exports = {}

var require = function(path) {
    return exports;
}


/**
 * ---------------------
 *     Gauge Options    
 * ---------------------
 */


var SpeedGaugeOptions = {
    angle: -0.1, // The span of the gauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 0.8, // Relative radius
    pointer: {
        length: 0.6, // // Relative to gauge radius
        strokeWidth: 0.035, // The thickness
        color: '#EEEEEE' // Fill color
    },

    staticLabels: {
        font: "14px sans-serif",  // Specifies font
        labels: [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220],  // Print labels at these values
        color: "#000000",  // Optional: Label text color
        fractionDigits: 0  // Optional: Numerical precision. 0=round off.
    },

    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the gauge will be fixed
    

    // generateGradient: true,
    highDpiSupport: true,     // High resolution support

    staticZones: [
        {strokeStyle: "#333333", min: 0, max: 200, height: 1.5},  // Red
        {strokeStyle: "#F03E3E", min: 200, max: 220, height: 1.5}  // Red
     ],

    renderTicks: {
        divisions: 11,
        divWidth: 1.1,
        divLength: 0.7,
        divColor: "#cccccc",
        subDivisions: 4,
        subLength: 0.5,
        subWidth: 0.6,
        subColor: "#cccccc"
      }
}


/**
 * Handle UI elements when doc is ready
 */
$(document).ready(function(){
    isBrowserReady = true
    
    var target = document.getElementById('testGauge'); // your canvas element
    gauge = new Gauge(target).setOptions(SpeedGaugeOptions); // create sexy gauge!
    
    gauge.maxValue = 220; // set max gauge value
    gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
    gauge.animationSpeed = 3;
    gauge.set(0); // set actual value

    $speedLabel = $('#textField');

    // gauge.setTextField(document.getElementById("textField"));

    textBox = document.getElementById('value');

});


function buttonClicked(){
    updateGauge(parseFloat(textBox.value, 10));
}

updateGauge = function(newValue) {
    if (isBrowserReady) {
        gauge.set(parseFloat(newValue));
        $speedLabel.text(newValue);
    }
}

/**
 * get request
 */
function getGaugeUpdate(){
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8080/?dan=shakdan',
        success: function(data) {
            console.log(data.speed);
            updateGauge(data.speed)
        },
        error: function(){
            alert("error loading user count");
        }
    });
}