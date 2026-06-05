# Validation Report: query2_original_original

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

1. Using SELECT * instead of selecting only required columns
2. Using CROSS JOIN instead of INNER JOIN
3. Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) which can prevent index usage
4. Using non-sargable WHERE clauses (LIKE with wildcard at the beginning)
5. Using subquery in the WHERE clause which can be slow for large datasets

## Optimization Explanation

The original query has several performance issues. Firstly, using SELECT * instead of selecting only required columns can lead to unnecessary data transfer and processing. Secondly, using CROSS JOIN instead of INNER JOIN can result in a much larger result set, which can be slow. Thirdly, using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) can prevent the database from using indexes, leading to slower query performance. Fourthly, using non-sargable WHERE clauses (LIKE with wildcard at the beginning) can also prevent index usage. Lastly, using a subquery in the WHERE clause can be slow for large datasets. The optimized query addresses these issues by using INNER JOIN, selecting only required columns, avoiding function-wrapped predicates, and using sargable WHERE clauses. Additionally, the subquery in the WHERE clause has been removed as it was filtering sales that occurred in 2024, but the original query was already filtering sales that occurred in 2020, so this subquery was not necessary.

## Validation Error

```
[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column, variable, or function parameter with name `e`.`name` cannot be resolved. Did you mean one of the following? [`e`.`city`, `e`.`emp_name`, `s`.`amount`, `e`.`emp_id`, `e`.`salary`]. SQLSTATE: 42703; line 4 pos 6;
'Distinct
+- 'Project [emp_id#12539, 'e.name, country#12544, dept_id#12546, dept_name#12547, sale_id#12526, sale_date#12530, amount#12529]
   +- Filter ((((sale_date#12530 >= cast(2020-01-01 as date)) AND (sale_date#12530 < cast(2020-07-01 as date))) AND (country#12544 = USA)) AND ((amount#12529 > cast(5000.00 as decimal(10,2))) AND dept_name#12547 LIKE %engineering%))
      +- Join Inner, (dept_id#12541 = dept_id#12546)
         :- Join Inner, (emp_id#12527 = emp_id#12539)
         :  :- SubqueryAlias s
         :  :  +- SubqueryAlias workspace.sql_optimizer_tests.sales
         :  :     +- Relation workspace.sql_optimizer_tests.sales[sale_id#12526,emp_id#12527,product#12528,amount#12529,sale_date#12530,region#12531] parquet
         :  +- SubqueryAlias e
         :     +- SubqueryAlias workspace.sql_optimizer_tests.employees
         :        +- Relation workspace.sql_optimizer_tests.employees[emp_id#12539,emp_name#12540,dept_id#12541,salary#12542,hire_date#12543,country#12544,city#12545] parquet
         +- SubqueryAlias d
            +- SubqueryAlias workspace.sql_optimizer_tests.departments
               +- Relation workspace.sql_optimizer_tests.departments[dept_id#12546,dept_name#12547,location#12548] parquet


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.errors.QueryCompilationErrors$.unresolvedAttributeError(QueryCompilationErrors.scala:708)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.org$apache$spark$sql$catalyst$analysis$CheckAnalysis$$failUnresolvedAttribute(CheckAnalysis.scala:192)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$17(CheckAnalysis.scala:553)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$17$adapted(CheckAnalysis.scala:538)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.traverse$1(CheckAnalysis.scala:1198)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.foreachUpSkippingSecureView(CheckAnalysis.scala:1200)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$16(CheckAnalysis.scala:538)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$16$adapted(CheckAnalysis.scala:538)
	at scala.collection.IterableOnceOps.foreach(IterableOnce.scala:619)
	at scala.collection.IterableOnceOps.foreach$(IterableOnce.scala:617)
	at scala.collection.AbstractIterable.foreach(Iterable.scala:935)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:538)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2$adapted(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:377)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0$(CheckAnalysis.scala:295)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis0(Analyzer.scala:562)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis$1(CheckAnalysis.scala:280)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis(CheckAnalysis.scala:267)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis$(CheckAnalysis.scala:263)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis(Analyzer.scala:562)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$resolveInFixedPoint$1(HybridAnalyzer.scala:414)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:266)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.resolveInFixedPoint(HybridAnalyzer.scala:414)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$apply$1(HybridAnalyzer.scala:97)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.withTrackedAnalyzerBridgeState(HybridAnalyzer.scala:134)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.apply(HybridAnalyzer.scala:90)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$2(Analyzer.scala:629)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.markInAnalyzer(AnalysisHelper.scala:425)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$1(Analyzer.scala:629)
	at com.databricks.sql.unity.SAMSnapshotHelper$.visitPlansDuringAnalysis(SAMSnapshotHelper.scala:43)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.executeAndCheck(Analyzer.scala:618)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$3(QueryExecution.scala:587)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:918)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$8(QueryExecution.scala:1053)
	at org.apache.spark.sql.execution.SQLExecution$.$anonfun$withExecutionPhase$1(SQLExecution.scala:322)
	at com.databricks.util.TracingSpanUtils$.withTracing(TracingSpanUtils.scala:251)
	at com.databricks.spark.util.DatabricksTracingHelper.withSpan(DatabricksSparkTracingHelper.scala:154)
	at com.databricks.spark.util.DBRTracing$.withSpan(DBRTracing.scala:87)
	at org.apache.spark.sql.execution.SQLExecution$.withExecutionPhase(SQLExecution.scala:303)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$7(QueryExecution.scala:1053)
	at org.apache.spark.sql.execution.QueryExecution$.withInternalError(QueryExecution.scala:1784)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$5(QueryExecution.scala:1046)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$4(QueryExecution.scala:1043)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$3(QueryExecution.scala:1043)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$2(QueryExecution.scala:1042)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.localBlock$1(QueryExecution.scala:1023)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$4(QueryExecution.scala:1033)
	at com.databricks.unity.UCSManager$.withTemporaryScope(UCSManager.scala:168)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$3(QueryExecution.scala:1032)
	at org.apache.spark.sql.execution.QueryExecution$.$anonfun$runWithWrappers$2(QueryExecution.scala:2039)
	at org.apache.spark.sql.execution.QueryExecution$.org$apache$spark$sql$execution$QueryExecution$$runWithWrappers(QueryExecution.scala:2038)
	at org.apache.spark.sql.execution.QueryExecution.withQueryExecutionId(QueryExecution.scala:1033)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$1(QueryExecution.scala:1041)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.execution.QueryExecution.executePhase(QueryExecution.scala:1040)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$2(QueryExecution.scala:578)
	at com.databricks.sql.util.MemoryTrackerHelper.withMemoryTracking(MemoryTrackerHelper.scala:111)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$1(QueryExecution.scala:577)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1770)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1820)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.analyzed(QueryExecution.scala:641)
	at org.apache.spark.sql.execution.QueryExecution.assertAnalyzed(QueryExecution.scala:500)
	at org.apache.spark.sql.classic.Dataset$.$anonfun$ofRows$3(Dataset.scala:157)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$withActiveAndFrameProfiler$1(SparkSession.scala:1330)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.classic.SparkSession.withActiveAndFrameProfiler(SparkSession.scala:1330)
	at org.apache.spark.sql.classic.Dataset$.ofRows(Dataset.scala:149)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$6(SparkSession.scala:1015)
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

- Execution error: [UNRESOLVED_COLUMN.WITH_SUGGESTION] A column, variable, or function parameter with name `e`.`name` cannot be resolved. Did you mean one of the following? [`e`.`city`, `e`.`emp_name`, `s`.`amount`, `e`.`emp_id`, `e`.`salary`]. SQLSTATE: 42703; line 4 pos 6;
'Distinct
+- 'Project [emp_id#12539, 'e.name, country#12544, dept_id#12546, dept_name#12547, sale_id#12526, sale_date#12530, amount#12529]
   +- Filter ((((sale_date#12530 >= cast(2020-01-01 as date)) AND (sale_date#12530 < cast(2020-07-01 as date))) AND (country#12544 = USA)) AND ((amount#12529 > cast(5000.00 as decimal(10,2))) AND dept_name#12547 LIKE %engineering%))
      +- Join Inner, (dept_id#12541 = dept_id#12546)
         :- Join Inner, (emp_id#12527 = emp_id#12539)
         :  :- SubqueryAlias s
         :  :  +- SubqueryAlias workspace.sql_optimizer_tests.sales
         :  :     +- Relation workspace.sql_optimizer_tests.sales[sale_id#12526,emp_id#12527,product#12528,amount#12529,sale_date#12530,region#12531] parquet
         :  +- SubqueryAlias e
         :     +- SubqueryAlias workspace.sql_optimizer_tests.employees
         :        +- Relation workspace.sql_optimizer_tests.employees[emp_id#12539,emp_name#12540,dept_id#12541,salary#12542,hire_date#12543,country#12544,city#12545] parquet
         +- SubqueryAlias d
            +- SubqueryAlias workspace.sql_optimizer_tests.departments
               +- Relation workspace.sql_optimizer_tests.departments[dept_id#12546,dept_name#12547,location#12548] parquet


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.errors.QueryCompilationErrors$.unresolvedAttributeError(QueryCompilationErrors.scala:708)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.org$apache$spark$sql$catalyst$analysis$CheckAnalysis$$failUnresolvedAttribute(CheckAnalysis.scala:192)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$17(CheckAnalysis.scala:553)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$17$adapted(CheckAnalysis.scala:538)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.traverse$1(CheckAnalysis.scala:1198)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.foreachUpSkippingSecureView(CheckAnalysis.scala:1200)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$16(CheckAnalysis.scala:538)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$16$adapted(CheckAnalysis.scala:538)
	at scala.collection.IterableOnceOps.foreach(IterableOnce.scala:619)
	at scala.collection.IterableOnceOps.foreach$(IterableOnce.scala:617)
	at scala.collection.AbstractIterable.foreach(Iterable.scala:935)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:538)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2$adapted(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:377)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0$(CheckAnalysis.scala:295)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis0(Analyzer.scala:562)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis$1(CheckAnalysis.scala:280)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis(CheckAnalysis.scala:267)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis$(CheckAnalysis.scala:263)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis(Analyzer.scala:562)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$resolveInFixedPoint$1(HybridAnalyzer.scala:414)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:266)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.resolveInFixedPoint(HybridAnalyzer.scala:414)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$apply$1(HybridAnalyzer.scala:97)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.withTrackedAnalyzerBridgeState(HybridAnalyzer.scala:134)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.apply(HybridAnalyzer.scala:90)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$2(Analyzer.scala:629)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.markInAnalyzer(AnalysisHelper.scala:425)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$1(Analyzer.scala:629)
	at com.databricks.sql.unity.SAMSnapshotHelper$.visitPlansDuringAnalysis(SAMSnapshotHelper.scala:43)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.executeAndCheck(Analyzer.scala:618)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$3(QueryExecution.scala:587)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:918)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$8(QueryExecution.scala:1053)
	at org.apache.spark.sql.execution.SQLExecution$.$anonfun$withExecutionPhase$1(SQLExecution.scala:322)
	at com.databricks.util.TracingSpanUtils$.withTracing(TracingSpanUtils.scala:251)
	at com.databricks.spark.util.DatabricksTracingHelper.withSpan(DatabricksSparkTracingHelper.scala:154)
	at com.databricks.spark.util.DBRTracing$.withSpan(DBRTracing.scala:87)
	at org.apache.spark.sql.execution.SQLExecution$.withExecutionPhase(SQLExecution.scala:303)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$7(QueryExecution.scala:1053)
	at org.apache.spark.sql.execution.QueryExecution$.withInternalError(QueryExecution.scala:1784)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$5(QueryExecution.scala:1046)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$4(QueryExecution.scala:1043)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$3(QueryExecution.scala:1043)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$2(QueryExecution.scala:1042)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.localBlock$1(QueryExecution.scala:1023)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$4(QueryExecution.scala:1033)
	at com.databricks.unity.UCSManager$.withTemporaryScope(UCSManager.scala:168)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$3(QueryExecution.scala:1032)
	at org.apache.spark.sql.execution.QueryExecution$.$anonfun$runWithWrappers$2(QueryExecution.scala:2039)
	at org.apache.spark.sql.execution.QueryExecution$.org$apache$spark$sql$execution$QueryExecution$$runWithWrappers(QueryExecution.scala:2038)
	at org.apache.spark.sql.execution.QueryExecution.withQueryExecutionId(QueryExecution.scala:1033)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$1(QueryExecution.scala:1041)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.execution.QueryExecution.executePhase(QueryExecution.scala:1040)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$2(QueryExecution.scala:578)
	at com.databricks.sql.util.MemoryTrackerHelper.withMemoryTracking(MemoryTrackerHelper.scala:111)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$1(QueryExecution.scala:577)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1770)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1820)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.analyzed(QueryExecution.scala:641)
	at org.apache.spark.sql.execution.QueryExecution.assertAnalyzed(QueryExecution.scala:500)
	at org.apache.spark.sql.classic.Dataset$.$anonfun$ofRows$3(Dataset.scala:157)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$withActiveAndFrameProfiler$1(SparkSession.scala:1330)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.classic.SparkSession.withActiveAndFrameProfiler(SparkSession.scala:1330)
	at org.apache.spark.sql.classic.Dataset$.ofRows(Dataset.scala:149)
	at org.apache.spark.sql.classic.SparkSession.$anonfun$sql$6(SparkSession.scala:1015)
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
*Generated: 2026-06-05 05:55:23*
