/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const recordRelease = (releaseId) => {
    fixtures().release({
        id: releaseId,
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

const testSteps = (releaseId) => {
    let release = Page.openRelease(releaseId);
    return release.start().waitForCompletion();
};

describe('Record (without XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(false);
        recordRelease('ReleaseRecord');
        return LoginPage.login('admin', 'admin');
    });

    it('should create record and request ', async () => {
        await testSteps('ReleaseRecord');
    });
});

describe('Record (with XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(true);
        recordRelease('ReleaseRecordWithApp');
        return LoginPage.login('admin', 'admin');
    });

    it('should create record and request ', async () => {
        await testSteps('ReleaseRecordWithApp');
    });
});
