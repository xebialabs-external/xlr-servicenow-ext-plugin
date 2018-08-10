from java.util import Date
from java.text import ParseException
from java.text import SimpleDateFormat
from sets import Set
from java.util import TimeZone
import traceback, sys

formatter = SimpleDateFormat(snFormat)
xlrFormat = SimpleDateFormat(xlFormat)
formatter.setTimeZone(TimeZone.getTimeZone(snTimeZone))

startDate = snData[startField]
print "------"
try:
    print "Schedule Task=> date = %s" % (startDate)
    date = formatter.parse(startDate)
    print "Schedule Task=> date = %s" % (date)
    release = getCurrentRelease()
    releaseID = release.id
    phaseTitle = targetPhase
    taskTitle = targetTask
    print "Schedule Task=> Phase / Task = %s / %s" % (phaseTitle, taskTitle)
    phase = phaseApi.searchPhasesByTitle(phaseTitle, releaseID)
    print "Schedule Task=> phase = %s" % (phase)
    phaseID = phase[0].id
    task = taskApi.searchTasksByTitle(taskTitle, phaseTitle, releaseID)
    print "Schedule Task=> task = %s" % (task)
    taskID = task[0].id
    myTask = taskApi.getTask(taskID)
    myTask.waitForScheduledStartDate = True
    myTask.scheduledStartDate = xlrFormat.format(date)
    print "Schedule Task=> Task = %s" % (myTask)
    print "Schedule Task=> Task.scheduledStartDate = %s" % (myTask.scheduledStartDate)
    taskApi.updateTask(myTask)
except ParseException, e:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    print e
print "------"
