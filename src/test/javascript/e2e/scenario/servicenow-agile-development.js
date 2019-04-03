/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const agileDevRelease = (releaseId) => {
    fixtures().release({
        id: releaseId,
        title: 'Do Agile Development',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Epic',
            status: 'planned',
            tasks: [{
                title: 'Find Sprint',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.FindSprint',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    ticket: "SPNT0010001"
                }
            }, {
                title: 'Create Epic',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateEpic',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: "This is an epic created from XLR!!",
                    product: "We have a product"
                }
            }, {
                title: 'Manual Task for Epic',
                type: 'xlrelease.Task',
                status: 'planned',
                owner: 'admin'
            }, {
                title: 'Update Epic',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateEpic',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    state: "Ready",
                    workNotes: "This is the work note!!",
                    sysId: ''
                }
            }, {
                title: 'Find Epic',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.FindEpic',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    ticket: ''
                }
            }, {
                title: 'Update Sprint',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateSprint',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    workNotes: 'Just adding work notes from XL Release',
                    sysId: ''
                }
            }]
        }, {
            title: 'Story',
            status: 'planned',
            tasks: [{
                title: 'Create Story',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateStory',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: "We need even better coffee...",
                    description: "All the previous stuff aint good enough",
                    assignmentGroup: "Demo Agile ReleaseXL",
                    storyPoints: "21",
                    acceptanceCriteria: "Test should be world class!",
                    epic: '',
                    sprint: ''
                }
            }, {
                title: 'Manual Task for Story',
                type: 'xlrelease.Task',
                status: 'planned',
                owner: 'admin'
            }, {
                title: 'Update Story',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateStory',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: "We need even better tea",
                    workNotes: "Just leaving a comment",
                    sysId: ''
                }
            }, {
                title: 'Find Story',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.FindStory',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    ticket: ''
                }
            }]
        }, {
            title: 'Scrum Task',
            status: 'planned',
            tasks: [{
                title: 'Create Scrum Task',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.CreateScrumTask',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: "Do google search",
                    description: "Do google search to find best tea in the world",
                    taskType: "Analysis",
                    story: ''
                }
            }, {
                title: 'Manual Task for Scrum Task',
                type: 'xlrelease.Task',
                status: 'planned',
                owner: 'admin'
            }, {
                title: 'Find Scrum Task by story',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.FindScrumTaskByStory',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    shortDescription: "Do",
                    story: ''
                }
            }, {
                title: 'Update Scrum Task',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateScrumTask',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    workNotes: "Just leaving a comment for scrum task",
                    taskType: "Testing",
                    sysId: ''
                }
            }]
        }, {
            title: 'Closure',
            status: 'planned',
            tasks: [{
                title: 'Close Scrum Task',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateScrumTask',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    workNotes: "closure comments from XL Release",
                    state: "Complete",
                    story: ''
                }
            }, {
                title: 'Close Story',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateStory',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    state: "Complete",
                    sysId: ''
                }
            }, {
                title: 'Close Epic',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.UpdateEpic',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    state: "Complete",
                    workNotes: "Closure from XL Release!!",
                    sysId: ''
                }
            }]
        }]
    });
};

const testSteps = async (releaseId) => {
    let release = Page.openRelease(releaseId);
    release.start().waitForTaskCompleted('Create Epic');

    let task = release.openCustomScriptDetails('Find Sprint');
    let sprintSysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    task.close();

    task = release.openCustomScriptDetails('Create Epic');
    let epicSysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    let epicNo = await task.taskDetails.element(By.$(`#Ticket .field-readonly`)).getText();
    task.close();

    task = release.openCustomScriptDetails('Update Epic');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(epicSysId);
    task.close();

    task = release.openCustomScriptDetails('Find Epic');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #ticket').set(epicNo);
    task.close();

    task = release.openCustomScriptDetails('Update Sprint');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(sprintSysId);
    task.close();

    task = release.openCustomScriptDetails('Create Story');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #epic').set(epicSysId);
    new InlineEditor('.modal:visible #sprint').set(sprintSysId);
    task.close();

    release.openManualTaskDetails('Manual Task for Epic').skipTask("WAIT DONE");

    release.waitForTaskCompleted('Create Story');

    task = release.openCustomScriptDetails('Create Story');
    let storySysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    let storyNo = await task.taskDetails.element(By.$(`#Ticket .field-readonly`)).getText();
    task.close();

    task = release.openCustomScriptDetails('Update Story');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(storySysId);
    task.close();

    task = release.openCustomScriptDetails('Find Story');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #ticket').set(storyNo);
    task.close();

    task = release.openCustomScriptDetails('Create Scrum Task');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #story').set(storySysId);
    task.close();

    task = release.openCustomScriptDetails('Find Scrum Task by story');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #story').set(storySysId);
    task.close();

    release.openManualTaskDetails('Manual Task for Story').skipTask("WAIT DONE");

    release.waitForTaskCompleted('Create Scrum Task');

    task = release.openCustomScriptDetails('Create Scrum Task');
    let scrumSysId = await task.taskDetails.element(By.$(`#sysId .field-readonly`)).getText();
    task.close();

    task = release.openCustomScriptDetails('Update Scrum Task');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(scrumSysId);
    task.close();

    task = release.openCustomScriptDetails('Close Scrum Task');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(scrumSysId);
    task.close();

    task = release.openCustomScriptDetails('Close Story');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(storySysId);
    task.close();

    task = release.openCustomScriptDetails('Close Epic');
    Browser.waitFor(".modal:visible #servicenowServer");
    new InlineEditor('.modal:visible #sysId').set(epicSysId);
    task.close();

    release.openManualTaskDetails('Manual Task for Scrum Task').skipTask("WAIT DONE");

    return release.waitForCompletion();
};

describe('Agile Development (without XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(false);
        agileDevRelease('ReleaseAgileDevelopment');
        return LoginPage.login('admin', 'admin');
    });

    it('should do agile development', async () => {
        await testSteps('ReleaseAgileDevelopment');
    });
});

describe('Agile Development (with XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(true);
        agileDevRelease('ReleaseAgileDevelopmentWithApp');
        return LoginPage.login('admin', 'admin');
    });

    it('should do agile development', async () => {
        await testSteps('ReleaseAgileDevelopmentWithApp');
    });
});
