/**
 * Copyright (c) 2019. All rights reserved.
 *
 * This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
 */
package com.xebialabs.xlrelease.plugins.servicenow

import akka.http.scaladsl.model.headers.LinkParams.title
import com.github.tomakehurst.wiremock.WireMockServer
import com.github.tomakehurst.wiremock.client.WireMock._
import com.github.tomakehurst.wiremock.core.WireMockConfiguration.options
import com.xebialabs.deployit.plugin.api.reflect.Type
import com.xebialabs.xlrelease.builder.PhaseBuilder.newPhase
import com.xebialabs.xlrelease.builder.ReleaseBuilder.newRelease
import com.xebialabs.xlrelease.builder.TaskBuilder.newCustomScript
import com.xebialabs.xlrelease.domain.CustomScriptTask
import com.xebialabs.xlrelease.domain.configuration.HttpConnection
import com.xebialabs.xlrelease.domain.status.TaskStatus.{IN_PROGRESS, PLANNED}
import com.xebialabs.xlrelease.repository.FacetRepositoryDispatcher
import com.xebialabs.xlrelease.script.ScriptTestService
import com.xebialabs.xlrelease.{TestIds, XLReleaseIntegrationScalaTest}
import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class ItsmTaskIntegrationTest extends XLReleaseIntegrationScalaTest {
  private val wireMockServer = new WireMockServer(options.dynamicPort)
  wireMockServer.start()

  override protected def beforeEach(): Unit = {
    super.beforeEach()
    createStub()
  }

  override protected def afterAll(): Unit = {
    super.afterAll()
    wireMockServer.stop()
  }

  lazy val scriptTestService = springBean[ScriptTestService]
  lazy val facetRepository = springBean[FacetRepositoryDispatcher]

  describe("ItsmTask") {
    it("should invoke facet API when create_task is successful") {
      val task = createTask("servicenow.CreateChangeRequest",
        Map("servicenowServer" -> servicenowServer(),
          "shortDescription" -> "short description from XL Release"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CHG0030696",
        record_url = s"http://localhost:${wireMockServer.port()}/change_request.do?sys_id=439c0e4fdb997300cab6ee82ca96196b",
        title = "short description from XL Release",
        status = "New",
        priority = "3 - Moderate",
        createdBy = "xlr")
    }

    it("should invoke facet API when update_task is successful") {
      val task = createTask("servicenow.UpdateIncident",
        Map("servicenowServer" -> servicenowServer(),
          "shortDescription" -> "update short description from XL Release",
          "sysId" -> "a5ac06cfdb997300cab6ee82ca96191f"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "INC0010340",
        record_url = s"http://localhost:${wireMockServer.port()}/incident.do?sys_id=a5ac06cfdb997300cab6ee82ca96191f",
        title = "update short description from XL Release",
        status = "New",
        priority = "5 - Planning",
        createdBy = "xlr")
    }

    it("should invoke facet API when poll_status is successful") {
      val task = createTask("servicenow.PollingCheckStatus",
        Map("servicenowServer" -> servicenowServer(),
          "statusField" -> "state",
          "sysId" -> "439c0e4fdb997300cab6ee82ca96196b",
          "checkForStatus" -> "New"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CHG0030696",
        record_url = s"http://localhost:${wireMockServer.port()}/change_request.do?sys_id=439c0e4fdb997300cab6ee82ca96196b",
        title = "short description from XL Release",
        status = "New",
        priority = "3 - Moderate",
        createdBy = "xlr")
    }

    it("servicenow.CheckChangeRequest") {
      wireMockServer.stubFor(
        get(urlMatching("/api/now/table/change_request.*"))
          .willReturn(aResponse
            .withHeader("Content-Type", "application/json")
            .withBodyFile("request_approval_approved.json")
          )
      )
      val task = createTask("servicenow.CheckChangeRequest",
        Map("servicenowServer" -> servicenowServer(),
          "number" -> "CHG0030700"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CHG0030700",
        record_url = s"http://localhost:${wireMockServer.port()}/change_request.do?sys_id=1ecc46cfdb997300cab6ee82ca961944",
        title = "provide approval please",
        status = "Closed",
        priority = "4 - Low",
        createdBy = "xlr")

    }

    it("servicenow.CheckStatus") {
      val task = createTask("servicenow.CheckStatus",
        Map("servicenowServer" -> servicenowServer(),
          "statusField" -> "state",
          "tableName" -> "change_task",
          "sysId" -> "34bc0e4bdbd97300b5326ce2ca96190d"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CTASK0010260",
        record_url = s"http://localhost:${wireMockServer.port()}/change_task.do?sys_id=34bc0e4bdbd97300b5326ce2ca96190d",
        title = "New Change Task from XL Release",
        status = "Open",
        priority = "4 - Low",
        createdBy = "xlr")

    }

    it("servicenow.GetChangeRequest") {
      val task = createTask("servicenow.GetChangeRequest",
        Map("servicenowServer" -> servicenowServer(),
          "number" -> "CHG0030696",
          "fieldNames" -> "priority,state"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CHG0030696",
        record_url = s"http://localhost:${wireMockServer.port()}/change_request.do?sys_id=439c0e4fdb997300cab6ee82ca96196b",
        title = "short description from XL Release",
        status = "New",
        priority = "3 - Moderate",
        createdBy = "xlr")

    }

    it("servicenow.RequestApproval") {
      wireMockServer.stubFor(
        post(urlMatching("/api/now/table/change_request.*"))
          .willReturn(aResponse
            .withHeader("Content-Type", "application/json")
            .withBodyFile("request_approval.json")
          )
      )
      wireMockServer.stubFor(
        get(urlMatching("/api/now/table/change_request.*"))
          .willReturn(aResponse
            .withHeader("Content-Type", "application/json")
            .withBodyFile("request_approval_approved.json")
          )
      )

      val task = createTask("servicenow.RequestApproval",
        Map("servicenowServer" -> servicenowServer(),
          "shortDescription" -> "provide approval please",
          "description" -> "need your approval"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CHG0030700",
        record_url = s"http://localhost:${wireMockServer.port()}/change_request.do?sys_id=1ecc46cfdb997300cab6ee82ca961944",
        title = "provide approval please",
        status = "Closed",
        priority = "4 - Low",
        createdBy = "xlr")

    }

    it("servicenow.FindChangeTaskByParent") {
      val task = createTask("servicenow.FindChangeTaskByParent",
        Map("servicenowServer" -> servicenowServer(),
          "parent" -> "439c0e4fdb997300cab6ee82ca96196b"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CTASK0010260",
        record_url = s"http://localhost:${wireMockServer.port()}/change_task.do?sys_id=34bc0e4bdbd97300b5326ce2ca96190d",
        title = "New Change Task from XL Release",
        status = "Open",
        priority = "4 - Low",
        createdBy = "xlr")

    }

    it("servicenow.FindRecordByQuery") {
      val task = createTask("servicenow.FindRecordByQuery",
        Map("servicenowServer" -> servicenowServer(),
          "query" -> "number=INC0010340"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "INC0010340",
        record_url = s"http://localhost:${wireMockServer.port()}/incident.do?sys_id=a5ac06cfdb997300cab6ee82ca96191f",
        title = "update short description from XL Release",
        status = "New",
        priority = "5 - Planning",
        createdBy = "xlr")
    }

    it("servicenow.FindRecordByTicket") {
      val task = createTask("servicenow.FindRecordByTicket",
        Map("servicenowServer" -> servicenowServer(),
          "ticket" -> "CHG0030696"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "CHG0030696",
        record_url = s"http://localhost:${wireMockServer.port()}/task.do?sys_id=439c0e4fdb997300cab6ee82ca96196b",
        title = "short description from XL Release",
        status = "New",
        priority = "3 - Moderate",
        createdBy = "xlr")

    }

    it("servicenow.PublishArticle") {
      val task = createTask("servicenow.PublishArticle",
        Map("servicenowServer" -> servicenowServer(),
          "knowledgeBase" -> "Knowledge",
          "articleCategory" -> "Release Notes",
          "shortDescription" -> "Test Article from XL Release",
          "articleText" -> "New <i>article</i> from <strong>xlr-servicenow-plugin"))

      executeAndVerifyFacet(task = task,
        serverUrl = s"http://localhost:${wireMockServer.port()}",
        serverUser = "xlr",
        record = "KB0010134",
        record_url = s"http://localhost:${wireMockServer.port()}/kb_view.do?sys_kb_id=f583cfd3db95b300cab6ee82ca96193b",
        title = "Test Article from XL Release",
        status = null,
        priority = null,
        createdBy = "xlr")

    }
  }

  private def executeAndVerifyFacet(task: CustomScriptTask,
                                    serverUrl: String,
                                    serverUser: String,
                                    record: String,
                                    record_url: String,
                                    title: String,
                                    status: String,
                                    priority: String,
                                    createdBy: String): Unit = {
    scriptTestService.executeCustomScriptTask(task)
    val facets = facetRepository.findAllFacetsByTask(task)
    facets should have size (1)

    val facet = facets.apply(0)
    facet.getType should equal(Type.valueOf("udm.ItsmFacet"))
    facet.getProperty[String]("serverUrl") shouldBe serverUrl
    facet.getProperty[String]("serverUser") shouldBe serverUser
    facet.getProperty[String]("record") shouldBe record
    facet.getProperty[String]("record_url") shouldBe record_url
    facet.getProperty[String]("title") shouldBe title
    facet.getProperty[String]("status") shouldBe status
    facet.getProperty[String]("priority") shouldBe priority
    facet.getProperty[String]("createdBy") shouldBe createdBy
  }

  private def createTask(taskType: String, propertyMap: Map[String, _]): CustomScriptTask = {
    val task = newCustomScript(taskType).withIdAndTitle(TestIds.TASK111).withStatus(PLANNED).build
    val script = task.getPythonScript
    propertyMap.foreach(x => script.setProperty(x._1, x._2))
    val phase = newPhase.withIdAndTitle(TestIds.PHASE11).withTasks(task).build
    val release = newRelease.withId(TestIds.RELEASE1).withPhases(phase).withScriptUsername("admin").withScriptUserPassword("admin").build
    storeRelease(release)
    releaseActorLifecycleUtils.activateReleaseActorAndAwait(release.getId)
    task.setStatus(IN_PROGRESS)
    task
  }

  private def servicenowServer(): HttpConnection = {
    val server: HttpConnection = Type.valueOf("servicenow.Server").getDescriptor.newInstance(TestIds.CONFIGURATION1)
    server.setProperty("url", s"http://localhost:${wireMockServer.port}")
    server.setUsername("xlr")
    server.setPassword("xlr")
    configurationRepository.create(server)
    markForDeletion(server)
    server
  }

  private def createStub(): Unit = {
    wireMockServer.stubFor(
      post(urlMatching("/api/now/table/change_request.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("change_request.json")
        )
    )
    wireMockServer.stubFor(
      get(urlMatching("/api/now/table/change_request.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("get_change_request.json")
        )
    )
    wireMockServer.stubFor(
      get(urlMatching("/api/now/table/task.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("get_change_request.json")
        )
    )
    wireMockServer.stubFor(
      put(urlMatching("/api/now/table/incident.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("incident.json")
        )
    )
    wireMockServer.stubFor(
      get(urlMatching("/api/now/table/incident.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("get_incident.json")
        )
    )
    wireMockServer.stubFor(
      get(urlMatching("/api/now/table/change_task.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("get_change_task.json")
        )
    )
    wireMockServer.stubFor(
      post(urlMatching("/api/now/table/kb_knowledge.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("kb_knowledge.json")
        )
    )
    wireMockServer.stubFor(
      get(urlMatching("/api/now/table/kb_knowledge.*"))
        .willReturn(aResponse
          .withHeader("Content-Type", "application/json")
          .withBodyFile("get_kb_knowledge.json")
        )
    )
  }
}
