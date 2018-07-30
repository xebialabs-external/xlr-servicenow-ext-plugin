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
                }]
            }]
        });
        return LoginPage.login('admin', 'admin');
    });

    it('Run release', function () {
        let release = Page.openRelease('ReleaseCreateServiceItem');

        // const task = release.openCustomScriptDetails('Control task check connection');
        // Browser.waitFor(".modal:visible #server");
        //
        // let ciNameEditor = new InlineEditor('.modal:visible #ciId');
        // ciNameEditor.set('Infrastructure/testHost');
        //
        // let taskNameEditor = new InlineEditor('.modal:visible #taskName');
        // taskNameEditor.set('checkConnection');
        // task.close();
        //
        return release.start().waitForCompletion();

    });

    // it('should not run a invalid control task on configuration item', function () {
    //     let release = Page.openRelease('ReleaseControltask');
    //     const task = release.openCustomScriptDetails('Control task check connection');
    //     Browser.waitFor(".modal:visible #server");
    //
    //     let ciNameEditor = new InlineEditor('.modal:visible #ciId');
    //     ciNameEditor.set('Infrastructure/testHost');
    //
    //     let taskNameEditor = new InlineEditor('.modal:visible #taskName');
    //     taskNameEditor.set('invalidTask');
    //     task.close();
    //
    //     release.start();
    //     return release.waitForTaskFailed('Control task check connection',10000);
    //
    // });
});
