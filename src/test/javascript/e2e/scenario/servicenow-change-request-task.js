/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const changeRequestTaskRelease = (releaseId) => {
    fixtures().release({
        id: releaseId,
        title: 'Create Incident',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Create Change Request Task',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateTask',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    content: '{"short_description":"New","comments":"New"}'
                }
            }, {
                title: 'Manual Task',
                type: 'xlrelease.Task',
                status: 'planned',
                owner: 'admin'
            }, {
                title: 'Update Task',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateTask',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    sysId: '',
                    content: '{"short_description":"Update","comments":"Update"}'
                }
            }, {
                title: 'Check Status',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CheckStatus',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    statusField: 'state',
                    tableName: 'change_task',
                    sysId: ''
                }
            }]
        }]
    });
};

const testSteps = async (releaseId) => {
    let release = Page.openRelease(releaseId);
    release.start().waitForTaskCompleted('Create Change Request Task');

    let task = release.openCustomScriptDetails('Create Change Request Task');
    var sysId = await task.taskDetails.element(By.$(`#taskId .field-readonly`)).getText();
    task.close();

    task = release.openCustomScriptDetails('Update Task');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(sysId);
    task.close();

    task = release.openCustomScriptDetails('Check Status');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(sysId);
    task.close();

    release.openManualTaskDetails('Manual Task').skipTask("WAIT DONE");

    return release.waitForCompletion();
};

describe('Change Request Task (without XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(false);
        changeRequestTaskRelease('ReleaseCreateChangeRequestTask');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find change request task', async () => {
        await testSteps('ReleaseCreateChangeRequestTask');
    });
});

describe('Change Request Task (with XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(true);
        changeRequestTaskRelease('ReleaseCreateChangeRequestTaskWithApp');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find change request task', async () => {
        await testSteps('ReleaseCreateChangeRequestTaskWithApp');
    });
});
