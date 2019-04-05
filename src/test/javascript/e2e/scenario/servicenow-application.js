/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const generateRandomString = (string_length) => {
    let random_string = '';
    let random_ascii;
    for (let i = 0; i < string_length; i++) {
        random_ascii = Math.floor((Math.random() * 25) + 97);
        random_string += String.fromCharCode(random_ascii)
    }
    return random_string
};

const applicationRelease = (releaseId) => {
    let randomAppName = generateRandomString(10);
    fixtures().release({
        id: releaseId,
        title: 'ServiceNow Applications',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Create Application',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.Application',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    ciName: randomAppName,
                    description: 'Test App from XL Release',
                    environment: 'Resource',
                    version: '1.0.0',
                    company: 'XebiaLabs'
                }
            }, {
                title: 'Create Application',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateApplicationVersion',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    ciName: randomAppName,
                    description: 'Test App from XL Release',
                    environment: 'Resource',
                    version: '2.0.0',
                    company: 'XebiaLabs B.V.'
                }
            }]
        }]
    });
};

const testSteps = (releaseId) => {
    let release = Page.openRelease(releaseId);
    return release.start().waitForCompletion();
};

describe('Application (without XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(false);
        applicationRelease('ReleaseApplication');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update application ', async () => {
        await testSteps('ReleaseApplication');
    });
});

describe('Application (with XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(true);
        applicationRelease('ReleaseApplicationWithApp');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update application ', async () => {
        await testSteps('ReleaseApplicationWithApp');
    });
});
