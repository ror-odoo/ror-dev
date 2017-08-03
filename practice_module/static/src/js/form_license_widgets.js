odoo.define('practice_module.form_license_widgets', function(require) {
	"use strict";

	var ajax = require('web.ajax');
	var core = require('web.core');
	var data = require('web.data');
	var framework = require('web.framework');
	var Model = require('web.DataModel');
	var Formwidget = require('web.form_widgets')

	var _t = core._t;

	var FieldLicense = Formwidget.FieldChar.extend({
		init : function() {
			this._super.apply(this, arguments);
		},
		store_dom_value : function() {
			var value = this.$input.val()
			if (value) {
				var license = new RegExp("([A-Z]){2}([0-9]){2}([0-9]){4}([0-9]){7}$");
				if (license.test(value)) {
					this._super(value);
				} else {
					alert("Enter valid License No")
				}
			}
			// this._super();
		}
	});
	core.form_widget_registry.add('licenseno', FieldLicense)
});
