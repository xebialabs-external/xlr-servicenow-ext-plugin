/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
'use strict';
const os = require('os');
const { SpecReporter } = require('jasmine-spec-reporter');

const DEFAULT_TIMEOUT = 12000000;
const firefoxBinary = process.env.FIREFOX_BINARY || undefined;

exports.config = {
    capabilities: {
        "browserName": (process.env.SELENIUM_TEST_BROWSER || "chrome").toLowerCase(),
        "platform": (process.env.SELENIUM_TEST_PLATFORM || "linux").toLowerCase(),
        "requireWindowFocus": true,
        "firefox_binary": firefoxBinary,
        "elementScrollBehavior": 1,
    },
    baseUrl: "http://" + os.hostname() + ":" + (process.env.XL_RELEASE_PORT || "5516"),
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
    onPrepare: () => {
        require('babel-polyfill');
        require('babel-register')({
            presets: ['es2015', 'stage-0']
        });
        global.requestPromise = require('request-promise');
        global._ = require('lodash');
        global.moment = require('moment');
        global.EC = protractor.ExpectedConditions;

        jasmine.getEnv().addReporter(new SpecReporter({
            displayStacktrace: 'all',      // display stacktrace for each failed assertion, values: (all|specs|summary|none)
            displaySuccessesSummary: false, // display summary of all successes after execution
            displayFailuresSummary: true,   // display summary of all failures after execution
            displayPendingSummary: true,    // display summary of all pending specs after execution
            displaySuccessfulSpec: true,    // display each successful spec
            displayFailedSpec: true,        // display each failed spec
            displayPendingSpec: false,      // display each pending spec
            displaySpecDuration: false,     // display each spec duration
            displaySuiteNumber: false,      // display each suite number (hierarchical)
            colors: {
                success: 'green',
                failure: 'red',
                pending: 'yellow'
            },
            prefixes: {
                success: '✓ ',
                failure: '✗ ',
                pending: '* '
            },
            customProcessors: []
        }));

        require('./e2e/dsl/fixtures-ci-builder.js');

        let dslFiles = require("glob").sync("../../../build/e2e-dsl/**/*.js", {cwd: __dirname});
        _.each(dslFiles, require);
        By.addLocator("$", () => {
            let selector = arguments[0];
            let using = arguments[1] || document;
            let results = $(using).find(selector);
            let matches = [];
            if (!$.isArray(results)) {
                matches.push(results.get(0));
            } else {
                for (let i = 0; i < results.length; ++i) {
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
            address: 'https://ven02515.service-now.com',
            username: 'adm.mpl',
            password: 'uUsXwssOMOR9'
        }
    }
};
