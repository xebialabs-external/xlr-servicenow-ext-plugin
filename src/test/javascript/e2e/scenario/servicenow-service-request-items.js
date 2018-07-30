describe('Service Item', function () {
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
            title: 'Create Service Item',
            status: 'planned',
            scheduledStartDate: moment().subtract(3, 'days'),
            dueDate: moment().add(8, 'days'),
            phases: [{
                title: 'Prod',
                status: 'planned',
                tasks: [{
                    title: 'Create Service item ',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenowxl.CreateRequestItem',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        shortDescription : 'description',
                        comments: 'comments'
                    }
                }, {
                    title: 'Create Service item ',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenowxl.CreateNewRequestItem',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"New","comments":"New"}'
                    }
                }, {
                    title: 'Create Service item ',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenowxl.UpdateRequestItem',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        content : '{"short_description":"Updated","comments":"Updated"}',
                        sysId: ''
                    }
                }, {
                    title: 'Create Service item ',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenowxl.FindRequestItemByTicket',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        ticket : ''
                    }
                }]
            }]
        });
        return LoginPage.login('admin', 'admin');
    });

    it('Run release', function () {
        let release = Page.openRelease('ReleaseCreateServiceItem');

        return release.start().waitForCompletion();

    });

});
