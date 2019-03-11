/*
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
const initReleaseDefaults = (function () {
    const RELEASE_TYPE = 'xlrelease.Release';
    const PHASE_TYPE = 'xlrelease.Phase';
    const TEAM_TYPE = 'xlrelease.Team';
    const TASK_TYPE = 'xlrelease.Task';
    const COMMENT_TYPE = 'xlrelease.Comment';
    const CONDITION_TYPE = 'xlrelease.GateCondition';
    const DEPENDENCY_TYPE = 'xlrelease.Dependency';
    const LINK_TYPE = 'xlrelease.Link';
    const ATTACHMENT_TYPE = 'xlrelease.Attachment';
    const DASHBOARD_TYPE = 'xlrelease.Dashboard';
    const TRIGGER_TYPE = 'xlrelease.ReleaseTrigger';
    const DEFAULT_TASK_OWNER = 'Itchy';

    const processTasks = function (task, container, index) {
        if (_.isUndefined(task.type))
            task.type = TASK_TYPE;
        task.id = task.id ? task.id : container.id + '/Task' + index;
        if (_.isUndefined(task.owner))
            task.owner = DEFAULT_TASK_OWNER;
        if (task.owner === null)
            delete task.owner;

        _.each(task.conditions, function (condition, index) {
            condition.type = CONDITION_TYPE;
            condition.id = task.id + '/GateCondition' + index;
        });
        _.each(task.dependencies, function (dependency, index) {
            dependency.type = DEPENDENCY_TYPE;
            dependency.id = task.id + '/Dependency' + index;
        });
        _.each(task.links, function (link, index) {
            link.type = LINK_TYPE;
            link.id = task.id + '/Link' + index;
        });
        _.each(task.comments, function (comment, index) {
            comment.type = COMMENT_TYPE;
            comment.id = task.id + '/Comment' + index;
        });
        _.each(task.tasks, function (subTask, index) {
            processTasks(subTask, task, index);
        });
        _.each(task.templateVariables, function (variable, index) {
            _.defaults(variable, getVariableEntity(variable.value, variable.key, task.id, index));
        });
        _.each(task.attachments, function (attachment, index) {
            attachment.type = ATTACHMENT_TYPE;
            attachment.id = task.id + '/Attachment' + index;
        });
        if ('pythonScript' in task) {
            const pythonScript = task.pythonScript;
            pythonScript.id = task.id + '/PythonScript';
            pythonScript.customScriptTask = task.id;
        }
    };

    const processPhases = function (phase, release, index) {
        phase.type = PHASE_TYPE;
        phase.id = release.id + '/Phase' + index;

        _.forEach(phase.tasks, function (task, index) {
            processTasks(task, phase, index);
        });
    };

    const getVariableEntity = function (value, key, containerId, index, password) {
        const rv = {};
        const keyNoSyntax = key.replace('${', '').replace('}', '');
        rv.id = containerId + '/Variable' + index;
        rv.key = keyNoSyntax;
        rv.requiresValue = true;
        rv.showOnReleaseStart = true;
        rv.type = password ? 'xlrelease.PasswordStringVariable' : 'xlrelease.StringVariable';
        if (value) {
            rv.value = value;
        }
        return rv;
    };

    const getValueProviderConfigurationEntity = function (containerId) {
        return {
            id: containerId + '/valueProvider',
            variable: containerId
        };
    };

    function getDashboardExtension(dashboard, releaseId) {
        const dashboardExtension = {
            id: releaseId + '/summary',
            type: DASHBOARD_TYPE,
            tiles: []
        };
        if (dashboard.tiles) {
            _.forEach(dashboard.tiles, function (tile, index) {
                dashboardExtension.tiles.push(getTileEntity(tile, releaseId + '/summary', index));
            });
        }
        return dashboardExtension;
    }

    function getTileEntity(tile, containerId, index) {
        tile.id = tile.id || containerId + '/Tile' + index;
        return tile;
    }

    return function (release) {
        release.type = RELEASE_TYPE;
        if (release.id.indexOf('Applications/') === -1) {
            release.id = 'Applications/' + release.id;
        }
        if (release.startDate) {
            release.queryableStartDate = release.startDate;
        } else if (release.scheduledStartDate) {
            release.queryableStartDate = release.scheduledStartDate;
        }
        if (release.endDate) {
            release.queryableEndDate = release.endDate;
        } else if (release.dueDate) {
            release.queryableEndDate = release.dueDate;
        }
        if (_.isUndefined(release.owner)) {
            release.owner = 'Itchy'; // default release manager
        }

        if (_.isUndefined(release.scriptUsername)) {
            release.scriptUsername = 'admin' //default script user
        }
        if (_.isUndefined(release.scriptUserPassword)) {
            release.scriptUserPassword = 'admin'
        }

        _.forEach(release.phases, function (phase, index) {
            processPhases(phase, release, index);
        });
        _.forEach(release.teams, function (team, index) {
            team.type = TEAM_TYPE;
            team.id = release.id + '/Team' + index;
        });
        _.forEach(release.releaseTriggers, function (trigger, index) {
            trigger.type = TRIGGER_TYPE;
            trigger.id = release.id + '/Trigger' + index;
        });
        _.forEach(release.attachments, function (attachment, index) {
            attachment.type = ATTACHMENT_TYPE;
            attachment.id = release.id + '/Attachment' + index;
        });
        _.forEach(release.variables, function (variable, index) {
            _.defaults(variable, getVariableEntity(variable.value, variable.key, release.id, index));
            if (variable.valueProvider) {
                _.defaults(variable.valueProvider, getValueProviderConfigurationEntity(variable.id));
            }
        });
        _.forEach(_.toPairs(release.variableValues), function (keyValue, index) {
            if (!release.variables)
                release.variables = [];
            release.variables.push(getVariableEntity(keyValue[1], keyValue[0], release.id, 1000 + index));
            release.variableValues = undefined;
        });
        _.forEach(_.toPairs(release.passwordVariableValues), function (keyValue, index) {
            if (!release.variables)
                release.variables = [];
            release.variables.push(getVariableEntity(keyValue[1], keyValue[0], release.id, 1500 + index, true));
            release.passwordVariableValues = undefined;
        });

        if (release.summary) {
            release.extensions = [ getDashboardExtension(release.summary, release.id) ];
            release.summary = undefined;
        }
    };
})();

const getFolderEntities = (function () {
    const FOLDER_TYPE = 'xlrelease.Folder';
    const TEAM_TYPE = 'xlrelease.Team';

    function forEachRecursive(items, getterFn, callbackFn) {
        if (!items) {
            return;
        }
        _.forEach(items, function (item) {
            const children = getterFn(item);
            callbackFn(item);
            forEachRecursive(children, getterFn, callbackFn);
        });
    }

    return function (folder) {
        const entities = [];

        forEachRecursive([folder],
            function (f) {
                return f.children;
            },
            function (f) {
                if (f.teams) {
                    _.forEach(f.teams, function (team) {
                        team.type = TEAM_TYPE;
                        entities.push(team);
                    });
                    delete f.teams;
                }
            });

        forEachRecursive([folder],
            function (f) {
                return f.children;
            },
            function (f) {
                f.type = FOLDER_TYPE;
                delete f.children;
                entities.push(f);
            });

        return entities;
    };
})();


// No global object in Angular-Scenario
try {
    global.initReleaseDefaults = initReleaseDefaults;
    global.getFolderEntities = getFolderEntities;
} catch (error) {
}
