/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
import {createServiceNowCI} from '../dsl/servicenow-ci';

const publishArticleRelease = (releaseId) => {
    fixtures().release({
        id: releaseId,
        title: 'Publish Article',
        status: 'planned',
        scheduledStartDate: moment().subtract(3, 'days'),
        dueDate: moment().add(8, 'days'),
        phases: [{
            title: 'Prod',
            status: 'planned',
            tasks: [{
                title: 'Publish Article',
                type: 'xlrelease.CustomScriptTask',
                status: 'planned',
                owner: 'admin',
                pythonScript: {
                    type: 'servicenow.PublishArticle',
                    servicenowServer: 'Configuration/Custom/ConfigurationServiceNow',
                    knowledgeBase: 'Knowledge',
                    articleCategory: 'Release Notes',
                    shortDescription: 'Test Article from XL Release',
                    articleText: 'New <i>article</i> from <strong>xlr-servicenow-plugin</strong>'
                }
            }]
        }]
    });
};

const testSteps = (releaseId) => {
    let release = Page.openRelease(releaseId);
    return release.start().waitForCompletion();
};

describe('Publish Article (without XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(false);
        publishArticleRelease('ReleasePublishArticle');
        return LoginPage.login('admin', 'admin');
    });

    it('should publish article ', async () => {
        await testSteps('ReleasePublishArticle');
    });
});

describe('Publish Article (with XL Release App)', () => {
    globalForEach();

    beforeEach(() => {
        createServiceNowCI(true);
        publishArticleRelease('ReleasePublishArticleWithApp');
        return LoginPage.login('admin', 'admin');
    });

    it('should publish article ', async () => {
        await testSteps('ReleasePublishArticleWithApp');
    });
});
