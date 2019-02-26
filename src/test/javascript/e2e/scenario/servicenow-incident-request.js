/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
describe('Incident Request', function () {
    globalForEach();

    beforeEach(function () {
        fixtures().ci({
            id: 'Configuration/Custom/ConfigurationServiceNow',
            title: 'Service Now Server',
            type: 'servicenow.Server',
            url: browser.params.servicenow.address,
            username: browser.params.servicenow.username,
            password: browser.params.servicenow.password
        });

        fixtures().release({
            id: 'ReleaseCreateIncidentRequest',
            title: 'Create Incident',
            status: 'planned',
            scheduledStartDate: moment().subtract(3, 'days'),
            dueDate: moment().add(8, 'days'),
            phases: [{
                title: 'Prod',
                status: 'planned',
                tasks: [{
                    title: 'Create Incident Request',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.CreateIncident',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        shortDescription : 'description',
                        comments: 'comments'
                    }
                }, {
                    title: 'Create New Incident Request',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.CreateNewIncident',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"New","comments":"New"}'
                    }
                }, {
                    title: 'Manual Task',
                    type: 'xlrelease.Task',
                    status: 'planned',
                    owner: 'admin'
                }, {
                    title: 'Update Incident',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.UpdateIncident',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"Updated","comments":"Updated"}',
                        sysId: ''
                    }
                }, {
                    title: 'Find Incident',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.FindIncidentByTicket',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        ticket : ''
                    }
                }]
            }]
        });
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find incident request', async () => {
        let release = Page.openRelease('ReleaseCreateIncidentRequest');
        release.start().waitForTaskCompleted('Create New Incident Request');

        let task = release.openCustomScriptDetails('Create New Incident Request');
        var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
        var ticket = await task.taskDetails.element(By.$(`#Ticket .field-readonly`)).getText();
        task.close();

        task = release.openCustomScriptDetails('Update Incident');
        Browser.waitFor(".modal:visible #servicenowServer");
        new InlineEditor('.modal:visible #sysId').set(sysId);
        task.close();

        task = release.openCustomScriptDetails('Find Incident');
        Browser.waitFor(".modal:visible #servicenowServer");
        new InlineEditor('.modal:visible #ticket').set(ticket);
        task.close();

        release.openManualTaskDetails('Manual Task').skipTask("WAIT DONE");

        return release.waitForCompletion();

    });

});
