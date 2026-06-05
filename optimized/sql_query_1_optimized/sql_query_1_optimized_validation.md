# Validation Report: sql_query_1_optimized

## Summary

| Metric | Value |
|--------|-------|
| **Overall Status** | ❌ FAILED |
| **Row Count** | 0 |
| **Column Count** | 0 |

## Performance Improvement

| Metric | Original | Optimized | Improvement |
|--------|----------|-----------|-------------|
| **Execution Time** | 0.00s | 0.00s | 0.00s saved (0.0% faster) |
| **Speedup Factor** | 1.0x | 0.00x | 0.00x faster |

### Performance Summary

⚠️ **Note:** The optimized query runs slightly slower (0.00x). This is common with small datasets where optimization overhead outweighs benefits. Performance gains would be more significant on larger datasets.

## Validation

- ✅ **Row Count Match**: 0 rows (identical)
- ❌ **Column Names Differ**
- ❌ **Data Checksum Mismatch**: Results differ

## Issues Found & Fixed

1. No indexes on join columns and where clause column
2. Potential full table scan due to lack of indexes

## Optimization Explanation

The original query is well-structured and does not contain any obvious performance issues such as SELECT *, CROSS JOIN, or function-wrapped predicates. However, the lack of indexes on the join columns and the where clause column can lead to full table scans, which can significantly impact performance. By creating indexes on these columns, we can improve the query performance by allowing the database to use index scans instead of full table scans. This optimization does not change the query logic and will return the same results as the original query.

## Validation Error

```

[INVALID_STATEMENT_OR_CLAUSE] The statement or clause: CREATE INDEX is not valid. SQLSTATE: 42601
== SQL (line 3, position 5) ==
    CREATE INDEX idx_employees_dept_id ON workspace.sql_optimizer_tests.employees(dept_id);
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_employees_emp_id ON workspace.sql_optimizer_tests.employees(emp_id);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_departments_dept_id ON workspace.sql_optimizer_tests.departments(dept_id);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_sales_emp_id ON workspace.sql_optimizer_tests.sales(emp_id);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_employees_salary ON workspace.sql_optimizer_tests.employees(salary);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    SELECT e.emp_name, d.dept_name, s.product
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FROM workspace.sql_optimizer_tests.employees e
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    INNER JOIN workspace.sql_optimizer_tests.departments d
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ON e.dept_id = d.dept_id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    INNER JOIN workspace.sql_optimizer_tests.sales s
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ON e.emp_id = s.emp_id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    WHERE e.salary > 80000;
^^^^^^^^^^^^^^^^^^^^^^^^^^


JVM stacktrace:
org.apache.spark.sql.catalyst.parser.ParseException
	at org.apache.spark.sql.errors.QueryParsingErrors$.invalidStatementError(QueryParsingErrors.scala:509)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.invalidStatement(ParserUtils.scala:47)
	at org.apache.spark.sql.execution.SparkSqlAstBuilder.$anonfun$visitFailNativeCommand$1(SparkSqlParser.scala:1406)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.execution.SparkSqlAstBuilder.visitFailNativeCommand(SparkSqlParser.scala:1402)
	at org.apache.spark.sql.execution.SparkSqlAstBuilder.visitFailNativeCommand(SparkSqlParser.scala:334)
	at org.apache.spark.sql.catalyst.parser.SqlBaseParser$FailNativeCommandContext.accept(SqlBaseParser.java:14150)
	at org.antlr.v4.runtime.tree.AbstractParseTreeVisitor.visit(AbstractParseTreeVisitor.java:18)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitSingleStatement$3(AstBuilder.scala:1207)
	at scala.Option.map(Option.scala:242)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitSingleStatement$1(AstBuilder.scala:1207)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.visitSingleStatement(AstBuilder.scala:1208)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitCompoundOrSingleStatement$3(AstBuilder.scala:211)
	at scala.Option.getOrElse(Option.scala:201)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitCompoundOrSingleStatement$1(AstBuilder.scala:211)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.visitCompoundOrSingleStatement(AstBuilder.scala:210)
	at org.apache.spark.sql.execution.SparkSqlParser.$anonfun$parsePlanWithParameters$2(SparkSqlParser.scala:214)
	at org.apache.spark.sql.catalyst.parser.AbstractSqlParser.$anonfun$withErrorHandling$1(AbstractSqlParser.scala:166)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.catalyst.parser.AbstractSqlParser.withErrorHandling(AbstractSqlParser.scala:165)
	at org.apache.spark.sql.execution.SparkSqlParser.$anonfun$parsePlanWithParameters$1(SparkSqlParser.scala:214)
	at org.apache.spark.sql.catalyst.parser.AbstractParser$.executeWithTwoStageStrategy(parsers.scala:312)
	at org.apache.spark.sql.catalyst.parser.AbstractParser.parse(parsers.scala:89)
	at org.apache.spark.sql.execution.SparkSqlParser.super$parse(SparkSqlParser.scala:312)
	at org.apache.spark.sql.execution.SparkSqlParser.$anonfun$parseInternal$1(SparkSqlParser.scala:312)
	at org.apache.spark.sql.catalyst.trees.CurrentOrigin$.withOrigin(origin.scala:142)
	at org.apache.spark.sql.execution.SparkSqlParser.parseInternal(SparkSqlParser.scala:312)
	at org.apache.spark.sql.execution.SparkSqlParser.parseWithParameters(SparkSqlParser.scala:182)
	at org.apache.spark.sql.execution.SparkSqlParser.parsePlanWithParameters(SparkSqlParser.scala:196)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$9(SparkSession.scala:994)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:266)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$8(SparkSession.scala:994)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:918)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$6(SparkSession.scala:990)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.classic.SparkSession.sql(SparkSession.scala:980)
	at org.apache.spark.sql.connect.planner.SparkConnectPlanner.executeSQL(SparkConnectPlanner.scala:4264)
	at org.apache.spark.sql.connect.planner.SparkConnectPlanner.handleSqlCommand(SparkConnectPlanner.scala:4057)
	at org.apache.spark.sql.connect.planner.SparkConnectPlanner.process(SparkConnectPlanner.scala:3756)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.handleCommand(ExecuteThreadRunner.scala:517)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.$anonfun$executeInternal$1(ExecuteThreadRunner.scala:405)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.$anonfun$executeInternal$1$adapted(ExecuteThreadRunner.scala:331)
	at org.apache.spark.sql.connect.service.SessionHolder.$anonfun$withSession$2(SessionHolder.scala:745)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.connect.service.SessionHolder.$anonfun$withSession$1(SessionHolder.scala:745)
	at org.apache.spark.JobArtifactSet$.withActiveJobArtifactState(JobArtifactSet.scala:97)
	at org.apache.spark.sql.artifact.ArtifactManager.$anonfun$withResources$1(ArtifactManager.scala:124)
	at org.apache.spark.sql.artifact.ArtifactManager.withClassLoaderIfNeeded(ArtifactManager.scala:118)
	at org.apache.spark.sql.artifact.ArtifactManager.withResources(ArtifactManager.scala:123)
	at org.apache.spark.sql.connect.service.SessionHolder.withSession(SessionHolder.scala:744)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.executeInternal(ExecuteThreadRunner.scala:331)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.$anonfun$execute$1(ExecuteThreadRunner.scala:196)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.connect.service.UtilizationMetrics.recordActiveQueries(UtilizationMetrics.scala:72)
	at com.databricks.spark.connect.service.UtilizationMetrics.recordActiveQueries$(UtilizationMetrics.scala:69)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.recordActiveQueries(ExecuteThreadRunner.scala:57)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.org$apache$spark$sql$connect$execution$ExecuteThreadRunner$$execute(ExecuteThreadRunner.scala:188)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner$ExecutionThread.$anonfun$run$3(ExecuteThreadRunner.scala:722)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.DBRTracing$.withSpanFromParent(DBRTracing.scala:70)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner$ExecutionThread.$anonfun$run$2(ExecuteThreadRunner.scala:722)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.unity.UCSEphemeralState$Handle.runWith(UCSEphemeralState.scala:51)
	at com.databricks.unity.HandleImpl.runWith(UCSHandle.scala:128)
	at com.databricks.unity.HandleImpl.$anonfun$runWithAndClose$1(UCSHandle.scala:133)
	at scala.util.Using$.resource(Using.scala:296)
	at com.databricks.unity.HandleImpl.runWithAndClose(UCSHandle.scala:132)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner$ExecutionThread.run(ExecuteThreadRunner.scala:721)
```

## Differences Detected

- Execution error: 
[INVALID_STATEMENT_OR_CLAUSE] The statement or clause: CREATE INDEX is not valid. SQLSTATE: 42601
== SQL (line 3, position 5) ==
    CREATE INDEX idx_employees_dept_id ON workspace.sql_optimizer_tests.employees(dept_id);
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_employees_emp_id ON workspace.sql_optimizer_tests.employees(emp_id);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_departments_dept_id ON workspace.sql_optimizer_tests.departments(dept_id);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_sales_emp_id ON workspace.sql_optimizer_tests.sales(emp_id);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    CREATE INDEX idx_employees_salary ON workspace.sql_optimizer_tests.employees(salary);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    SELECT e.emp_name, d.dept_name, s.product
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FROM workspace.sql_optimizer_tests.employees e
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    INNER JOIN workspace.sql_optimizer_tests.departments d
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ON e.dept_id = d.dept_id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    INNER JOIN workspace.sql_optimizer_tests.sales s
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ON e.emp_id = s.emp_id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    WHERE e.salary > 80000;
^^^^^^^^^^^^^^^^^^^^^^^^^^


JVM stacktrace:
org.apache.spark.sql.catalyst.parser.ParseException
	at org.apache.spark.sql.errors.QueryParsingErrors$.invalidStatementError(QueryParsingErrors.scala:509)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.invalidStatement(ParserUtils.scala:47)
	at org.apache.spark.sql.execution.SparkSqlAstBuilder.$anonfun$visitFailNativeCommand$1(SparkSqlParser.scala:1406)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.execution.SparkSqlAstBuilder.visitFailNativeCommand(SparkSqlParser.scala:1402)
	at org.apache.spark.sql.execution.SparkSqlAstBuilder.visitFailNativeCommand(SparkSqlParser.scala:334)
	at org.apache.spark.sql.catalyst.parser.SqlBaseParser$FailNativeCommandContext.accept(SqlBaseParser.java:14150)
	at org.antlr.v4.runtime.tree.AbstractParseTreeVisitor.visit(AbstractParseTreeVisitor.java:18)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitSingleStatement$3(AstBuilder.scala:1207)
	at scala.Option.map(Option.scala:242)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitSingleStatement$1(AstBuilder.scala:1207)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.visitSingleStatement(AstBuilder.scala:1208)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitCompoundOrSingleStatement$3(AstBuilder.scala:211)
	at scala.Option.getOrElse(Option.scala:201)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.$anonfun$visitCompoundOrSingleStatement$1(AstBuilder.scala:211)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.catalyst.parser.AstBuilder.visitCompoundOrSingleStatement(AstBuilder.scala:210)
	at org.apache.spark.sql.execution.SparkSqlParser.$anonfun$parsePlanWithParameters$2(SparkSqlParser.scala:214)
	at org.apache.spark.sql.catalyst.parser.AbstractSqlParser.$anonfun$withErrorHandling$1(AbstractSqlParser.scala:166)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin(SparkParserUtils.scala:213)
	at org.apache.spark.sql.catalyst.util.SparkParserUtils.withOrigin$(SparkParserUtils.scala:196)
	at org.apache.spark.sql.catalyst.parser.ParserUtils$.withOrigin(ParserUtils.scala:41)
	at org.apache.spark.sql.catalyst.parser.AbstractSqlParser.withErrorHandling(AbstractSqlParser.scala:165)
	at org.apache.spark.sql.execution.SparkSqlParser.$anonfun$parsePlanWithParameters$1(SparkSqlParser.scala:214)
	at org.apache.spark.sql.catalyst.parser.AbstractParser$.executeWithTwoStageStrategy(parsers.scala:312)
	at org.apache.spark.sql.catalyst.parser.AbstractParser.parse(parsers.scala:89)
	at org.apache.spark.sql.execution.SparkSqlParser.super$parse(SparkSqlParser.scala:312)
	at org.apache.spark.sql.execution.SparkSqlParser.$anonfun$parseInternal$1(SparkSqlParser.scala:312)
	at org.apache.spark.sql.catalyst.trees.CurrentOrigin$.withOrigin(origin.scala:142)
	at org.apache.spark.sql.execution.SparkSqlParser.parseInternal(SparkSqlParser.scala:312)
	at org.apache.spark.sql.execution.SparkSqlParser.parseWithParameters(SparkSqlParser.scala:182)
	at org.apache.spark.sql.execution.SparkSqlParser.parsePlanWithParameters(SparkSqlParser.scala:196)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$9(SparkSession.scala:994)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:266)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$8(SparkSession.scala:994)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:918)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$6(SparkSession.scala:990)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.classic.SparkSession.sql(SparkSession.scala:980)
	at org.apache.spark.sql.connect.planner.SparkConnectPlanner.executeSQL(SparkConnectPlanner.scala:4264)
	at org.apache.spark.sql.connect.planner.SparkConnectPlanner.handleSqlCommand(SparkConnectPlanner.scala:4057)
	at org.apache.spark.sql.connect.planner.SparkConnectPlanner.process(SparkConnectPlanner.scala:3756)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.handleCommand(ExecuteThreadRunner.scala:517)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.$anonfun$executeInternal$1(ExecuteThreadRunner.scala:405)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.$anonfun$executeInternal$1$adapted(ExecuteThreadRunner.scala:331)
	at org.apache.spark.sql.connect.service.SessionHolder.$anonfun$withSession$2(SessionHolder.scala:745)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.connect.service.SessionHolder.$anonfun$withSession$1(SessionHolder.scala:745)
	at org.apache.spark.JobArtifactSet$.withActiveJobArtifactState(JobArtifactSet.scala:97)
	at org.apache.spark.sql.artifact.ArtifactManager.$anonfun$withResources$1(ArtifactManager.scala:124)
	at org.apache.spark.sql.artifact.ArtifactManager.withClassLoaderIfNeeded(ArtifactManager.scala:118)
	at org.apache.spark.sql.artifact.ArtifactManager.withResources(ArtifactManager.scala:123)
	at org.apache.spark.sql.connect.service.SessionHolder.withSession(SessionHolder.scala:744)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.executeInternal(ExecuteThreadRunner.scala:331)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.$anonfun$execute$1(ExecuteThreadRunner.scala:196)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.connect.service.UtilizationMetrics.recordActiveQueries(UtilizationMetrics.scala:72)
	at com.databricks.spark.connect.service.UtilizationMetrics.recordActiveQueries$(UtilizationMetrics.scala:69)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.recordActiveQueries(ExecuteThreadRunner.scala:57)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner.org$apache$spark$sql$connect$execution$ExecuteThreadRunner$$execute(ExecuteThreadRunner.scala:188)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner$ExecutionThread.$anonfun$run$3(ExecuteThreadRunner.scala:722)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.DBRTracing$.withSpanFromParent(DBRTracing.scala:70)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner$ExecutionThread.$anonfun$run$2(ExecuteThreadRunner.scala:722)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.unity.UCSEphemeralState$Handle.runWith(UCSEphemeralState.scala:51)
	at com.databricks.unity.HandleImpl.runWith(UCSHandle.scala:128)
	at com.databricks.unity.HandleImpl.$anonfun$runWithAndClose$1(UCSHandle.scala:133)
	at scala.util.Using$.resource(Using.scala:296)
	at com.databricks.unity.HandleImpl.runWithAndClose(UCSHandle.scala:132)
	at org.apache.spark.sql.connect.execution.ExecuteThreadRunner$ExecutionThread.run(ExecuteThreadRunner.scala:721)

---
*Generated: 2026-06-05 05:55:30*
