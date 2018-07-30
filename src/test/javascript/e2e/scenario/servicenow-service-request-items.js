// /*
//  * Copyright (c) 2018. All rights reserved.
//  *
//  * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
//  */
// 'use strict'
//
// const serviceNowServer = 'ServiceNowServer';
//
// const openshiftClientConfig = 'Openshift Client Configuration';
//
// const timeout = 180000;
//
//
// describe('servicenow create and access service', () => {
//     beforeAll(()=>{
//         LoginPage.login('admin', 'admin');
//     });
//
//     afterAll(()=>{
//             LoginPage.logout();
//         });
//     beforeEach(() => {
//     fixtures().release({
//                 id: 'ReleaseWithServiceNowServiceRequestItem',
//                 title: 'ReleaseWithServiceNowServiceRequestItem',
//                 description: 'ReleaseWithServiceNowServiceRequestItem',
//                 status: 'planned',
//                 phases: [
//                     {
//                         title: 'Phase',
//                         status: 'PLANNED',
//                         tasks: []
//                     }
//                 ]
//             });
//     Page.openConfiguration()
//                 .addNewInstance('ServiceNow: Server')
//                 .setTextField('url', browser.params.servicenow.address)
//                 .setTextField('username', browser.params.servicenow.username)
//                 .setTextField('password', browser.params.servicenow.password)
//                 .save();
//
//     afterEach(() => {
//             fixtures().clean();
//             Page.openConfiguration().deleteInstance(openshiftClientConfig);
//             Page.openConfiguration().deleteInstance(serviceNowServer);
//         });
//
//     it('should create Servicerequest Items', () => {
//             utils.addFirstTask(addTaskTitle, 'openshift.createConf')
//                  .configureTask(addTaskTitle, jsonTaskConfig)
//                  .addAnotherTask(startCheckServiceTaskTitle, 'openshift.checkService')
//                  .configureTask(startCheckServiceTaskTitle, checkServiceTaskConfig)
//                  .addAnotherTask(deleteTaskTitle, 'openshift.removeConf')
//                  .configureTask(deleteTaskTitle, jsonTaskConfig)
//                  .startReleaseAndWait(timeout);
//              utils.assertOutput(startCheckServiceTaskTitle, 'Service hello-service is accessible')
//         });
// });
// });
