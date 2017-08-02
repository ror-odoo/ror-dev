odoo.define("website.tour.vehicle", function (require) {
    "use strict";
    var core = require("web.core");
    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var _t = core._t;
    
    tour.register("vehicle", {
    	test: true,
        url: "/vehicles",
        wait_for: base.ready(),
    }, [
    {
        trigger: ".vehicle_no",
        content: _t("<b>Click </b> to Show Vehicle Information."),
        position: "bottom",
    },
    {
        content: _t("<b>Click </b> to Show Vehicle List."),
        position: "bottom",
        trigger: ".back",
    }
    ]);

});