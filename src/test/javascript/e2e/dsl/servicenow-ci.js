/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */

export function createServiceNowCI(withApp) {
    fixtures().ci({
        id: 'Configuration/Custom/ConfigurationServiceNow',
        title: 'Service Now Server',
        type: 'servicenow.Server',
        url: browser.params.servicenow.address,
        username: browser.params.servicenow.username,
        password: browser.params.servicenow.password,
        useServicenowApp: withApp
    });
}
