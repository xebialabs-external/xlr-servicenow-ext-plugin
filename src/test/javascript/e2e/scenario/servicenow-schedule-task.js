describe('Schedule Task', function () {
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
                        type: 'servicenowxl.ScheduleTask',
                        startField : 'start_date',
                        targetPhase: 'Prod',
                        targetTask: 'Update CMDB',
                        snData: {'start_date':'2018-07-07 14:34:23'}
                    }
                }, {
                    title: 'Update CMDB',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenowxl.UpdateCMDB',
                        servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                        environment : 'testenv',
                        applicationName: 'testapp',
                        company: 'testcompany',
                        configAdminGroup: 'testadmingroup',
                        version: 'v1',
                        virtualMachine: 'testvirtualMachine'
                    }
                }]
            }]
        });
        return LoginPage.login('admin', 'admin');
    });

    it('should create schedule task', async () => {
        let release = Page.openRelease('ReleaseCreateScheduleTask');
        release.start().waitForTaskCompleted('Schedule Task');

        let task = release.openCustomScriptDetails('Update CMDB');
        var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
        task.close();

        return release.waitForCompletion();

    });

});
