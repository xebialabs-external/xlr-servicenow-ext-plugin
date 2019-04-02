/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const requestItemsRelease = () => {
    fixtures().release({
        id: 'ReleaseCreateServiceRequestItem',
        title: 'Create Service Item',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Create Service item',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateRequestItem',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: 'description',
                    comments: 'comments'
                }
            }, {
                title: 'Create New Service item',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateNewRequestItem',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    content: '{"short_description":"New","comments":"New"}'
                }
            }, {
                title: 'Manual Task',
                type: 'xlrelease.Task',
                status: 'planned',
                owner: 'admin'
            }, {
                title: 'Update Service item',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateRequestItem',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    content: '{"short_description":"Updated","comments":"Updated"}',
                    sysId: ''
                }
            }, {
                title: 'Find Service item',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.FindRequestItemByTicket',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    ticket: ''
                }
            }]
        }]
    });
};

const testSteps = async () => {
    let release = Page.openRelease('ReleaseCreateServiceRequestItem');
    release.start().waitForTaskCompleted('Create New Service item');

    let task = release.openCustomScriptDetails('Create New Service item');
    var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    var ticket = await task.taskDetails.element(By.$(`#Ticket .field-readonly`)).getText();
    task.close();

    task = release.openCustomScriptDetails('Update Service item');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(sysId);
    task.close();

    task = release.openCustomScriptDetails('Find Service item');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #ticket').set(ticket);
    task.close();

    release.openManualTaskDetails('Manual Task').skipTask("WAIT DONE");

    return release.waitForCompletion();
};

describe('Service Item (without XL Release App)', function () {
    globalForEach();

    beforeEach(function () {
        createServiceNowCI(false);
        requestItemsRelease();
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find service request item', testSteps);
});

describe('Service Item (with XL Release App)', function () {
    globalForEach();

    beforeEach(function () {
        createServiceNowCI(true);
        requestItemsRelease();
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find service request item', testSteps);
});
