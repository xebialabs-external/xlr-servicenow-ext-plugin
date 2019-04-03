/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const serviceRequestRelease = (releaseId) => {
    fixtures().release({
        id: releaseId,
        title: 'Create Service',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Create Service',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateServiceRequest',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: 'description',
                    comments: 'comments'
                }
            }, {
                title: 'Create New Service',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateNewServiceRequest',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    content: '{"short_description":"New","comments":"New"}'
                }
            }, {
                title: 'Manual Task',
                type: 'xlrelease.Task',
                status: 'planned',
                owner: 'admin'
            }, {
                title: 'Update Service',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateServiceRequest',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    content: '{"short_description":"Updated","comments":"Updated"}',
                    sysId: ''
                }
            }, {
                title: 'Find Service',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.FindServiceRequestItemByTicket',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    ticket: ''
                }
            }]
        }]
    });
};

const testSteps = async (releaseId) => {
    let release = Page.openRelease(releaseId);
    release.start().waitForTaskCompleted('Create New Service');

    let task = release.openCustomScriptDetails('Create New Service');
    var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    var ticket = await task.taskDetails.element(By.$(`#Ticket .field-readonly`)).getText();
    task.close();

    task = release.openCustomScriptDetails('Update Service');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(sysId);
    task.close();

    task = release.openCustomScriptDetails('Find Service');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #ticket').set(ticket);
    task.close();

    release.openManualTaskDetails('Manual Task').skipTask("WAIT DONE");

    return release.waitForCompletion();
};

describe('Service Request (without XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(false);
        serviceRequestRelease('ReleaseCreateServiceItem');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find service request', async () => {
        await testSteps('ReleaseCreateServiceItem');
    });
});

describe('Service Request (with XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(true);
        serviceRequestRelease('ReleaseCreateServiceItemWithApp');
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find service request', async () => {
        await testSteps('ReleaseCreateServiceItemWithApp');
    });
});
