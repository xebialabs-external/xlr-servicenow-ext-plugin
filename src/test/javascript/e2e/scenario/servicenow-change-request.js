describe('Change Request', function () {
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
            id: 'ReleaseCreateChangeRequest',
            title: 'Create Change Request',
            status: 'planned',
            scheduledStartDate: moment().subtract(3, 'days'),
            dueDate: moment().add(8, 'days'),
            phases: [{
                title: 'Prod',
                status: 'planned',
                tasks: [{
                    title: 'Create Change Request',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.CreateChangeRequest',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        shortDescription : 'description',
                        comments: 'comments'
                    }
                }, {
                    title: 'Create New Change Request',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.CreateNewChangeRequest',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"New","comments":"New"}'
                    }
                }, {
                    title: 'Manual Task',
                    type: 'xlrelease.Task',
                    status: 'planned',
                    owner: 'admin'
                }, {
                    title: 'Update Change Request',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.UpdateChangeRequest',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"Updated","comments":"Updated"}',
                        sysId: ''
                    }
                }, {
                    title: 'Find Change Request',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.FindChangeRequestByTicket',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        ticket : ''
                    }
                }, {
                    title: 'Poll Change Request status',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.PollingCheckStatus',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        sysId : '',
                        checkForStatus : "New"
                    }
                }, {
                    title: 'Get Change Request',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.GetChangeRequest',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        number : '',
                        fieldNames : ['state']
                    }
                }]
            }]
        });
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find change request', async () => {
        let release = Page.openRelease('ReleaseCreateChangeRequest');
        release.start().waitForTaskCompleted('Create New Change Request');

        let task = release.openCustomScriptDetails('Create New Change Request');
        var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
        var ticket = await task.taskDetails.element(By.$(`#Ticket .field-readonly`)).getText();
        task.close();

        task = release.openCustomScriptDetails('Update Change Request');
        Browser.waitFor(".modal:visible #servicenowServer");
        new InlineEditor('.modal:visible #sysId').set(sysId);
        task.close();

        task = release.openCustomScriptDetails('Find Change Request');
        Browser.waitFor(".modal:visible #servicenowServer");
        new InlineEditor('.modal:visible #ticket').set(ticket);
        task.close();

        task = release.openCustomScriptDetails('Poll Change Request status');
        Browser.waitFor(".modal:visible #servicenowServer");
        new InlineEditor('.modal:visible #sysId').set(sysId);
        task.close();

        task = release.openCustomScriptDetails('Get Change Request');
        Browser.waitFor(".modal:visible #servicenowServer");
        new InlineEditor('.modal:visible #number').set(ticket);
        task.close();

        release.openManualTaskDetails('Manual Task').skipTask("WAIT DONE");

        return release.waitForCompletion();

    });

});
