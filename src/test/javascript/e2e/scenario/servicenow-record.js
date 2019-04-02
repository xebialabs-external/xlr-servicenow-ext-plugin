/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const recordRelease = () => {
    fixtures().release({
        id: 'ReleaseRecord',
        title: 'Create Record ',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Create Record Request',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateRecord',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: 'description',
                    comments: 'comments'
                }
            }, {
                title: 'Create Request',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateRequest',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: 'description',
                    comments: 'comments'
                }
            }]
        }]
    });
};

const testSteps = () => {
    let release = Page.openRelease('ReleaseRecord');
    return release.start().waitForCompletion();
};

describe('Record (without XL Release App)', function () {
    globalForEach();

    beforeEach(function () {
        createServiceNowCI(false);
        recordRelease();
        return LoginPage.login('admin', 'admin');
    });

    it('should create record and request ', testSteps);
});

describe('Record (with XL Release App)', function () {
    globalForEach();

    beforeEach(function () {
        createServiceNowCI(true);
        recordRelease();
        return LoginPage.login('admin', 'admin');
    });

    it('should create record and request ', testSteps);
});
