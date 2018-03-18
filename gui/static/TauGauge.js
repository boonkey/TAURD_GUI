// template for gauge DOM element
var gaugeTemplate = "\n\
<div class='title'>\n\
    <label></label>\n\
</div>\n\
<canvas class='gauge'></canvas>\n\
<div class='display'>\n\
    <label></label>\n\
</div>\n\
<div class='units'>\n\
        <label></label>\n\
</div>\n\
"

//  dictionary for known gauge ooptions
var gaugeOptions = {
    "speed": SpeedGaugeOptions,
    "rpm": rpmGaugeOptions,
    "braking": brakingGaugeOptions,
    "throttle": throttleGaugeOptions,
    "wing_position": wingPosGaugeOptions,
}

// dictionary for known gauge units
var gaugeUnits = {
    "speed": "Kmph",
    "rpm": "rpm",
    "braking": "%",
    "throttle": "%",
    "wing_position": "°",
}

/**
 * A calss for a full gauge with all labels
 */
class TauGauge {

    /**
     * gauge expects element to have already been created
     * 
     * @param {gauge name} name 
     * @param {gauge min} minValue 
     * @param {gauge max} maxValue 
     * @param {gauge initial value} initValue 
     */
    constructor(name, minValue, maxValue, initValue){
        // set gauge title
        var $container = $("#" + name);
        $container.find('.title').find('label')[0].innerHTML = name

        // choose correct opts
        var opts = defaultGaugeOptions;
        if(name in gaugeOptions) {
            opts = gaugeOptions[name];
        }

        // create gauge canvas and set opts
        this.gauge = new Gauge($container.find(".gauge")[0]).setOptions(opts); // create speedgauge
        this.gauge.maxValue = maxValue; // set max speedGauge value
        this.gauge.setMinValue(minValue);  // Prefer setter over speedGauge.minValue = 0
        this.gauge.animationSpeed = 1;
        this.gauge.set(minValue); // set actual value

        // init display
        this.display = $container.find('.display').find('label')[0];
        this.display.innerHTML = "" + minValue;

        // init units
        if(name in gaugeUnits) {
            $container.find('.units').find('label')[0].innerHTML = gaugeUnits[name];
        }
    }

    /**
     * set new value for the gauge
     * @param {new value for the gauge} value 
     */
    updateGauge(value) {
        this.gauge.set(parseFloat(value));
        this.display.innerHTML = value;
    }

    static addNewGaugeElement(name) {
        var $container = $('<div class="gaugeContainer" id="' + name + '"></div>')
        $container.append(gaugeTemplate);
        $('body').append($container);
        return $container;
    }
}