describe('Service Request', function () {
    globalForEach();

    beforeEach(function () {
        fixtures().ci({
            id: 'Configuration/Custom/ConfigurationServiceNow',
            title: 'Service Now Server',
            type: 'servicenowxl.Server',
            url: browser.params.servicenow.address,
            username: browser.params.servicenow.username,
            password: browser.params.servicenow.password
        });

        fixtures().release({
            id: 'ReleaseCreateServiceItem',
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
                        type: 'servicenowxl.CreateServiceRequest',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        shortDescription : 'description',
                        comments: 'comments'
                    }
                }, {
                    title: 'Create New Service',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenowxl.CreateNewServiceRequest',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"New","comments":"New"}'
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
                        type: 'servicenowxl.UpdateServiceRequest',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"Updated","comments":"Updated"}',
                        sysId: ''
                    }
                }, {
                    title: 'Find Service',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenowxl.FindServiceRequestItemByTicket',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        ticket : ''
                    }
                }]
            }]
        });
        return LoginPage.login('admin', 'admin');
    });

    it('should create update find service request', async () => {
        let release = Page.openRelease('ReleaseCreateServiceItem');
        release.start().waitForTaskCompleted('Create New Service');

        let task = release.openCustomScriptDetails('Create New Service');
        var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
        var ticket = await task.taskDetails.element(By.$(`#ticket .field-readonly`)).getText();
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

    });

});
