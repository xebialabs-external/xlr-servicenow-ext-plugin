/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
describe('Update CMDB', function () {
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
            id: 'ReleaseUpdateCMDB',
            title: 'Update CMDB',
            status: 'planned',
            scheduledStartDate: moment().subtract(3, 'days'),
            dueDate: moment().add(8, 'days'),
            phases: [{
                title: 'Prod',
                status: 'planned',
                tasks: [{
                    title: 'Update CMDB',
                    type: 'xlrelease.CustomScriptTask',
                    status: 'planned',
                    owner: 'admin',
                    pythonScript: {
                        type: 'servicenow.UpdateCMDB',
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

    it('should create update cmdb', async () => {
        let release = Page.openRelease('ReleaseUpdateCMDB');
        release.start().waitForTaskCompleted('Update CMDB');

        let task = release.openCustomScriptDetails('Update CMDB');
        var sysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
        task.close();

        return release.waitForCompletion();

    });

});
