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
";

//  dictionary for known gauge ooptions
var gaugeOptions = {
    "speed": SpeedGaugeOptions,
    "rpm": rpmGaugeOptions,
    "braking": brakingGaugeOptions,
    "throttle": throttleGaugeOptions,
    "wing_position": wingPosGaugeOptions,
};

// dictionary for known gauge units
var gaugeUnits = {
    "speed": "Kmph",
    "rpm": "rpm",
    "braking": "%",
    "throttle": "%",
    "wing_position": "°",
};

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
        const $container = $("#" + name);
        $container.find('.title').find('label')[0].innerHTML = name;

        // choose correct opts
        let opts = defaultGaugeOptions;
        if(name in gaugeOptions) {
            opts = gaugeOptions[name];
        } else {
            const range = maxValue - minValue;
            const divisions = TauGauge.getTicksDivideFactor(range);

            const majorTick = range/divisions[0];

            const labels = [];

            let tickValue = parseFloat(minValue);

            while(tickValue <= maxValue) {
                labels.push(tickValue);
                tickValue += majorTick;
            }

            opts.staticLabels.labels = labels;
            opts.renderTicks.divisions = divisions[0];
            opts.renderTicks.subDivisions = divisions[1];

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

    /**
     * cretes new gauge DOM element using template
     * @param {name of the gauge to create} name 
     */
    static addNewGaugeElement(name) {
        const $container = $('<div class="gaugeContainer" id="' + name + '"></div>');
        $container.append(gaugeTemplate);
        $('body').append($container);
        return $container;
    }

    /**
     * finds a number to divide range by for a propper tick division
     * @param {gauge value range} range 
     */
    static getTicksDivideFactor(range) {
        const maxTicks = 11;
        const minTicks = 5;

        // main divisors
        const divisors = new Set();
        let sqrt = Math.sqrt(range);
        for(let i = 1; i < sqrt + 1; ++i) {
            if(range % i == 0) {
                divisors.add(i);
                divisors.add(range/i);
            }
        }

        // sub divisors
        const subDivisors = {};
        for(let j = maxTicks; j > minTicks - 1; j--) {

            // skip if not a good divisor
            if(!(divisors.has(j))) {
                continue;
            }

            const subRange = range/j;
            const subSqrt = Math.sqrt(subRange);
            for(let i = 1; i < subSqrt + 1; ++i) {
                if(subRange % i == 0) {
                    if(!(subRange in subDivisors)){
                        subDivisors[subRange] = new Set();
                    }

                    subDivisors[subRange].add(i);
                    subDivisors[subRange].add(subRange/i);
                }
            }
        }

        for(let i = maxTicks; i > minTicks - 1; i--) {
            for(let j = minTicks; j < maxTicks + 1; j++) {
                if(i in subDivisors && subDivisors[i].has(j)) {
                    return [i, j]
                }
            }
        }

        return [10, 5];

    }
}