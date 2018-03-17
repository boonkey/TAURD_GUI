
/**
 * ---------------------
 *     Gauge Options
 * ---------------------
 */


var SpeedGaugeOptions = {
    angle: -0.1, // The span of the speedGauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 0.8, // Relative radius
    pointer: {
        length: 0.6, // // Relative to speedGauge radius
        strokeWidth: 0.035, // The thickness
        color: '#EEEEEE' // Fill color
    },

    staticLabels: {
        font: "14px sans-serif",  // Specifies font
        labels: [0, 20, 40, 60, 80, 100, 120],  // Print labels at these values
        color: "#000000",  // Optional: Label text color
        fractionDigits: 0  // Optional: Numerical precision. 0=round off.
    },

    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the speedGauge will be fixed


    // generateGradient: true,
    highDpiSupport: true,     // High resolution support

    staticZones: [
        {strokeStyle: "#333333", min: 0, max: 120, height: 1.0},  // Red
        // {strokeStyle: "#F03E3E", min: 100, max: 120, height: 1.5}  // Red
    ],

    renderTicks: {
        divisions: 6,
        divWidth: 1.1,
        divLength: 0.4,
        divColor: "#cccccc",
        subDivisions: 4,
        subLength: 0.2,
        subWidth: 0.6,
        subColor: "#cccccc"
    }
};

var rpmGaugeOptions = {
    angle: -0.1, // The span of the speedGauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 0.8, // Relative radius
    pointer: {
        length: 0.6, // // Relative to speedGauge radius
        strokeWidth: 0.035, // The thickness
        color: '#EEEEEE' // Fill color
    },

    staticLabels: {
        font: "14px sans-serif",  // Specifies font
        labels: [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],  // Print labels at these
        // values
        color: "#000000",  // Optional: Label text color
        fractionDigits: 0  // Optional: Numerical precision. 0=round off.
    },

    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the speedGauge will be fixed


    // generateGradient: true,
    highDpiSupport: true,     // High resolution support

    staticZones: [
        {strokeStyle: "#333333", min: 0, max: 6500, height: 1.5},  // Black
        {strokeStyle: "#A08800", min: 6500, max: 7000, height: 1.5},  // Yellow
        {strokeStyle: "#F03E3E", min: 7000, max: 8000, height: 1.5}  // Red
    ],

    renderTicks: {
        divisions: 8,
        divWidth: 1.1,
        divLength: 0.4,
        divColor: "#cccccc",
        subDivisions: 2 ,
        subLength: 0.2,
        subWidth: 0.6,
        subColor: "#cccccc"
    }
};

var brakingGaugeOptions = {
    angle: -0.1, // The span of the speedGauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 0.8, // Relative radius
    pointer: {
        length: 0.6, // // Relative to speedGauge radius
        strokeWidth: 0.035, // The thickness
        color: '#EEEEEE' // Fill color
    },

    staticLabels: {
        font: "14px sans-serif",  // Specifies font
        labels: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],  // Print labels at these values
        color: "#000000",  // Optional: Label text color
        fractionDigits: 0  // Optional: Numerical precision. 0=round off.
    },

    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the speedGauge will be fixed


    // generateGradient: true,
    highDpiSupport: true,     // High resolution support

    staticZones: [
        {strokeStyle: "#333333", min: 0, max: 100, height: 1.5},  // Red
        // {strokeStyle: "#F03E3E", min: 200, max: 220, height: 1.5}  // Red
    ],

    renderTicks: {
        divisions: 10,
        divWidth: 1.1,
        divLength: 0.4,
        divColor: "#cccccc",
        subDivisions: 2,
        subLength: 0.2,
        subWidth: 0.6,
        subColor: "#cccccc"
    }
};

var throttleGaugeOptions = {
    angle: -0.1, // The span of the speedGauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 0.8, // Relative radius
    pointer: {
        length: 0.6, // // Relative to speedGauge radius
        strokeWidth: 0.035, // The thickness
        color: '#EEEEEE' // Fill color
    },

    staticLabels: {
        font: "14px sans-serif",  // Specifies font
        labels: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],  // Print labels at these values
        color: "#000000",  // Optional: Label text color
        fractionDigits: 0  // Optional: Numerical precision. 0=round off.
    },

    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the speedGauge will be fixed


    // generateGradient: true,
    highDpiSupport: true,     // High resolution support

    staticZones: [
        {strokeStyle: "#333333", min: 0, max: 100, height: 1.5},  // Red
        // {strokeStyle: "#F03E3E", min: 200, max: 220, height: 1.5}  // Red
    ],

    renderTicks: {
        divisions: 10,
        divWidth: 1.1,
        divLength: 0.4,
        divColor: "#cccccc",
        subDivisions: 2,
        subLength: 0.2,
        subWidth: 0.6,
        subColor: "#cccccc"
    }
};

var wingPosGaugeOptions = {
    angle: -0.2, // The span of the speedGauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 0.8, // Relative radius
    pointer: {
        length: 0.6, // // Relative to speedGauge radius
        strokeWidth: 0.035, // The thickness
        color: '#EEEEEE' // Fill color
    },

    staticLabels: {
        font: "14px sans-serif",  // Specifies font
        labels: [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100],  // Print labels at these values
        color: "#000000",  // Optional: Label text color
        fractionDigits: 0  // Optional: Numerical precision. 0=round off.
    },

    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the speedGauge will be fixed


    // generateGradient: true,
    highDpiSupport: true,     // High resolution support

    staticZones: [
        {strokeStyle: "#F03E3E", min: -100, max: -90, height: 0.7},  // Red
        {strokeStyle: "#333333", min: -90, max: 90, height: 0.7},  // Red
        {strokeStyle: "#F03E3E", min: 90, max: 100, height: 0.7}  // Red
    ],

    renderTicks: {
        divisions: 10,
        divWidth: 1.1,
        divLength: 0.4,
        divColor: "#cccccc",
        subDivisions: 4,
        subLength: 0.2,
        subWidth: 0.6,
        subColor: "#cccccc"
    }
};