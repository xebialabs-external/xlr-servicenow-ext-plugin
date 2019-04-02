/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const scheduleTaskRelease = () => {
    fixtures().release({
        id: 'ReleaseCreateScheduleTask',
        title: 'Create Schedule Task',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        scriptUsername: 'admin',
        scriptUserPassword: 'admin',
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Schedule Task',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.ScheduleTask',
                    startField: 'start_date',
                    targetPhase: 'Prod',
                    targetTask: 'Update CMDB',
                    snData: {'start_date': '2018-07-07 14:34:23'}
                }
            }, {
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

const testSteps = async () => {
    let release = Page.openRelease('ReleaseCreateScheduleTask');
    release.start().waitForTaskCompleted('Schedule Task');

    let task = release.openCustomScriptDetails('Update CMDB');
    var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    task.close();

    return release.waitForCompletion();
};

describe('Schedule Task (without XL Release App)', function () {
    globalForEach();

    beforeEach(function () {
        createServiceNowCI(false);
        scheduleTaskRelease();
        return LoginPage.login('admin', 'admin');
    });

    it('should create schedule task', testSteps);
});

describe('Schedule Task (with XL Release App)', function () {
    globalForEach();

    beforeEach(function () {
        createServiceNowCI(true);
        scheduleTaskRelease();
        return LoginPage.login('admin', 'admin');
    });

    it('should create schedule task', testSteps);
});
