/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const cmdbRelease = (releaseId) => {
    fixtures().release({
        id: releaseId,
        title: 'Update CMDB',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Update CMDB',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateCMDB',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    environment: 'testenv',
                    applicationName: 'testapp',
                    company: 'testcompany',
                    configAdminGroup: 'testadmingroup',
                    version: 'v1',
                    virtualMachine: 'testvirtualMachine'
                }
            }]
        }]
    });
};

const testSteps = async (releaseId) => {
    let release = Page.openRelease(releaseId);
    release.start().waitForTaskCompleted('Update CMDB');

    let task = release.openCustomScriptDetails('Update CMDB');
    var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    task.close();

    return release.waitForCompletion();
};

describe('Update CMDB (without XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(false);
        cmdbRelease('ReleaseUpdateCMDB');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update cmdb', async () => {
        await testSteps('ReleaseUpdateCMDB');
    });
});

describe('Update CMDB (with XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(true);
        cmdbRelease('ReleaseUpdateCMDBWithApp');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update cmdb', async () => {
        await testSteps('ReleaseUpdateCMDBWithApp');
    });
});
