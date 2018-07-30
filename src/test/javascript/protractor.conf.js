/*
 * Copyright (c) 2018. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
 */
'use strict';
var os = require('os');

var DEFAULT_TIMEOUT = 12000000;
var firefoxBinary = process.env.FIREFOX_BINARY || undefined;

exports.config = {
    capabilities: {
        "browserName": (process.env.SELENIUM_TEST_BROWSER || "chrome").toLowerCase(),
        "platform": (process.env.SELENIUM_TEST_PLATFORM || "linux").toLowerCase(),
        "requireWindowFocus": true,
        "firefox_binary": firefoxBinary,
        "elementScrollBehavior": 1,
    },
    baseUrl: "http://localhost:" + (process.env.XL_RELEASE_PORT || "5516"),
    allScriptsTimeout: DEFAULT_TIMEOUT,
    rootElement: "body",
    getPageTimeout: DEFAULT_TIMEOUT,
    specs: [
        './e2e/scenario/**/*.js'
    ],
    jasmineNodeOpts: {
        showColors: true,
        defaultTimeoutInterval: DEFAULT_TIMEOUT
    },
    framework: 'jasmine2',
    seleniumAddress: (process.env.SELENIUM_TEST_ADDR || null),
    onPrepare: function () {
        require('babel-register')({
            presets: ['es2015', 'stage-0']
        });
        global.requestPromise = require('request-promise');
        global._ = require('lodash');
        global.moment = require('moment');
        global.EC = protractor.ExpectedConditions;


        let SpecReporter = require('jasmine-spec-reporter');
        jasmine.getEnv().addReporter(new SpecReporter({displayStacktrace: true}));

        require('./e2e/scenario/fixtures-ci-builder.js');

        let dslFiles = require("glob").sync("../../../build/e2e-dsl/**/*.js", {cwd: __dirname});
        _.each(dslFiles, require);
        By.addLocator("$", function () {
            var selector = arguments[0];
            var using = arguments[1] || document;
            var results = $(using).find(selector);
            var matches = [];
            if (!$.isArray(results)) {
                matches.push(results.get(0));
            } else {
                for (var i = 0; i < results.length; ++i) {
                    matches.push(results[i][0]);
                }
            }
            return matches; // Return the whole array for webdriver.findElements.
        });
        Browser.open();
        Browser.setSize(1200, 800);
        browser.manage().timeouts().setScriptTimeout(60 * 1000);

    },
    params: {
        scale: 'true',
        cleanFixtures: 'true',
        servicenow: {
            address: 'https://dev19998.service-now.com/',
            username: 'admin',
            password: 'qV5GjPPfPfw9'
        }
    }
};
