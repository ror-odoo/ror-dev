odoo.define('practice_module', function(require) {
	"use strict";
	var core = require('web.core');
	var Widget = require('web.Widget');
	var Model = require('web.DataModel');

	var LiveDashboard = Widget.extend({
		template : 'LiveDashboard',

		events : {
			"click .total_package" : "total_package",
		},

		init : function(parent) {
			return this._super(parent);
		},
		total_package : function() {
			return this.do_action({
				name :"Package Book",
				type : 'ir.actions.act_window',
				res_model : "package.book",
				views : [ [false, 'list'], [false, 'form'] ],
				view_type: "list",
	            view_mode: "list",
			});
		},
		willStart : function() {
			var self = this;
			var res = this._super.apply(this, arguments).then(function() {
				return (new Model('package.book')).call('get_live_info');
			}).then(function(result) {
				self.data = result
			});
			return res;
		},

		start : function() {
			console.log("Start Function Call");
		},

	});
	core.action_registry.add('practice_module.livedashboard', LiveDashboard);
});