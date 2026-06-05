# Validation Report: query3

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

1. Redundant CTEs (employee_totals, dept_averages, employee_ranks, dept_info) can be combined
2. Unnecessary CAST() operations
3. Unnecessary CONCAT() operations in join conditions
4. YEAR() function in WHERE clause can be replaced with date range filter
5. Multiple aggregations scanning the same table can be combined

## Optimization Explanation

The original query had multiple redundant CTEs and aggregations that could be combined into a single efficient query. The CONCAT() operations in join conditions were unnecessary and have been removed. The YEAR() function in the WHERE clause has been replaced with a date range filter. The CAST() operations were also unnecessary and have been removed. The query now uses a single CTE to calculate all necessary values, and then joins this CTE with the departments table to get the department information. The WHERE and ORDER BY clauses remain the same to ensure the query logic is identical and returns the exact same results.

## Validation Error

```
[MISSING_AGGREGATION] The non-aggregating expression "amount" is based on columns which are not participating in the GROUP BY clause.
Add the columns or the expression to the GROUP BY, aggregate the expression, or use "any_value(amount)" if you do not care which of the values within a group is returned. SQLSTATE: 42803;
Sort [dept_rank#13078 ASC NULLS FIRST, total_sales#13074 DESC NULLS LAST], true
+- Distinct
   +- Project [emp_name#13072, total_sales#13074, num_sales#13075L, dept_rank#13078, dept_name#13070, location#13110, avg_dept_sale#13076, dept_sale_count#13077L, CASE WHEN (cast(total_sales#13074 as decimal(25,7)) > cast((avg_dept_sale#13076 * 1.5) as decimal(25,7))) THEN Top Performer WHEN (cast(total_sales#13074 as decimal(24,6)) > cast(avg_dept_sale#13076 as decimal(24,6))) THEN Above Average ELSE Below Average END AS performance_tier#13071]
      +- Filter (((upper(country#13073) = USA) AND lower(dept_name#13070) LIKE %engineering%) AND (total_sales#13074 > cast(cast(1000 as decimal(4,0)) as decimal(20,2))))
         +- Join Inner, (dept_id#13100 = dept_id#13108)
            :- SubqueryAlias ea
            :  +- SubqueryAlias employee_analysis
            :     +- SubqueryAlias employee_analysis
            :        +- Window [emp_id#13098, upper(emp_name#13099) AS emp_name#13072, dept_id#13100, upper(country#13103) AS country#13073, total_sales#13074, num_sales#13075L, avg(amount#13088) windowspecdefinition(dept_id#13100, specifiedwindowframe(RowFrame, unboundedpreceding$(), unboundedfollowing$())) AS avg_dept_sale#13076, count(1) windowspecdefinition(dept_id#13100, specifiedwindowframe(RowFrame, unboundedpreceding$(), unboundedfollowing$())) AS dept_sale_count#13077L, dept_rank#13078], [dept_id#13100]
            :           +- Window [emp_id#13098, emp_name#13099, dept_id#13100, country#13103, total_sales#13074, num_sales#13075L, amount#13088, _w7#13127, rank(_w7#13127) windowspecdefinition(dept_id#13100, _w7#13127 DESC NULLS LAST, specifiedwindowframe(RowFrame, unboundedpreceding$(), currentrow$())) AS dept_rank#13078], [dept_id#13100], [_w7#13127 DESC NULLS LAST]
            :              +- Aggregate [emp_id#13098, emp_name#13099, dept_id#13100, country#13103], [emp_id#13098, emp_name#13099, dept_id#13100, country#13103, sum(amount#13088) AS total_sales#13074, count(1) AS num_sales#13075L, amount#13088, sum(amount#13088) AS _w7#13127]
            :                 +- Filter ((sale_date#13089 >= cast(2024-01-01 as date)) AND (sale_date#13089 < cast(2025-01-01 as date)))
            :                    +- Join Inner, (emp_id#13086 = emp_id#13098)
            :                       :- SubqueryAlias s
            :                       :  +- SubqueryAlias workspace.sql_optimizer_tests.sales
            :                       :     +- Relation workspace.sql_optimizer_tests.sales[sale_id#13085,emp_id#13086,product#13087,amount#13088,sale_date#13089,region#13090] parquet
            :                       +- SubqueryAlias e
            :                          +- SubqueryAlias workspace.sql_optimizer_tests.employees
            :                             +- Relation workspace.sql_optimizer_tests.employees[emp_id#13098,emp_name#13099,dept_id#13100,salary#13101,hire_date#13102,country#13103,city#13104] parquet
            +- SubqueryAlias di
               +- Project [dept_id#13108, lower(dept_name#13109) AS dept_name#13070, location#13110]
                  +- SubqueryAlias workspace.sql_optimizer_tests.departments
                     +- Relation workspace.sql_optimizer_tests.departments[dept_id#13108,dept_name#13109,location#13110] parquet


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.errors.QueryCompilationErrors$.columnNotInGroupByClauseError(QueryCompilationErrors.scala:5682)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.checkExpr$1(ExprUtils.scala:310)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.$anonfun$assertValidAggregation$10(ExprUtils.scala:341)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.$anonfun$assertValidAggregation$10$adapted(ExprUtils.scala:341)
	at scala.collection.immutable.List.foreach(List.scala:334)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.assertValidAggregation(ExprUtils.scala:341)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:779)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2$adapted(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:377)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
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

- Execution error: [MISSING_AGGREGATION] The non-aggregating expression "amount" is based on columns which are not participating in the GROUP BY clause.
Add the columns or the expression to the GROUP BY, aggregate the expression, or use "any_value(amount)" if you do not care which of the values within a group is returned. SQLSTATE: 42803;
Sort [dept_rank#13078 ASC NULLS FIRST, total_sales#13074 DESC NULLS LAST], true
+- Distinct
   +- Project [emp_name#13072, total_sales#13074, num_sales#13075L, dept_rank#13078, dept_name#13070, location#13110, avg_dept_sale#13076, dept_sale_count#13077L, CASE WHEN (cast(total_sales#13074 as decimal(25,7)) > cast((avg_dept_sale#13076 * 1.5) as decimal(25,7))) THEN Top Performer WHEN (cast(total_sales#13074 as decimal(24,6)) > cast(avg_dept_sale#13076 as decimal(24,6))) THEN Above Average ELSE Below Average END AS performance_tier#13071]
      +- Filter (((upper(country#13073) = USA) AND lower(dept_name#13070) LIKE %engineering%) AND (total_sales#13074 > cast(cast(1000 as decimal(4,0)) as decimal(20,2))))
         +- Join Inner, (dept_id#13100 = dept_id#13108)
            :- SubqueryAlias ea
            :  +- SubqueryAlias employee_analysis
            :     +- SubqueryAlias employee_analysis
            :        +- Window [emp_id#13098, upper(emp_name#13099) AS emp_name#13072, dept_id#13100, upper(country#13103) AS country#13073, total_sales#13074, num_sales#13075L, avg(amount#13088) windowspecdefinition(dept_id#13100, specifiedwindowframe(RowFrame, unboundedpreceding$(), unboundedfollowing$())) AS avg_dept_sale#13076, count(1) windowspecdefinition(dept_id#13100, specifiedwindowframe(RowFrame, unboundedpreceding$(), unboundedfollowing$())) AS dept_sale_count#13077L, dept_rank#13078], [dept_id#13100]
            :           +- Window [emp_id#13098, emp_name#13099, dept_id#13100, country#13103, total_sales#13074, num_sales#13075L, amount#13088, _w7#13127, rank(_w7#13127) windowspecdefinition(dept_id#13100, _w7#13127 DESC NULLS LAST, specifiedwindowframe(RowFrame, unboundedpreceding$(), currentrow$())) AS dept_rank#13078], [dept_id#13100], [_w7#13127 DESC NULLS LAST]
            :              +- Aggregate [emp_id#13098, emp_name#13099, dept_id#13100, country#13103], [emp_id#13098, emp_name#13099, dept_id#13100, country#13103, sum(amount#13088) AS total_sales#13074, count(1) AS num_sales#13075L, amount#13088, sum(amount#13088) AS _w7#13127]
            :                 +- Filter ((sale_date#13089 >= cast(2024-01-01 as date)) AND (sale_date#13089 < cast(2025-01-01 as date)))
            :                    +- Join Inner, (emp_id#13086 = emp_id#13098)
            :                       :- SubqueryAlias s
            :                       :  +- SubqueryAlias workspace.sql_optimizer_tests.sales
            :                       :     +- Relation workspace.sql_optimizer_tests.sales[sale_id#13085,emp_id#13086,product#13087,amount#13088,sale_date#13089,region#13090] parquet
            :                       +- SubqueryAlias e
            :                          +- SubqueryAlias workspace.sql_optimizer_tests.employees
            :                             +- Relation workspace.sql_optimizer_tests.employees[emp_id#13098,emp_name#13099,dept_id#13100,salary#13101,hire_date#13102,country#13103,city#13104] parquet
            +- SubqueryAlias di
               +- Project [dept_id#13108, lower(dept_name#13109) AS dept_name#13070, location#13110]
                  +- SubqueryAlias workspace.sql_optimizer_tests.departments
                     +- Relation workspace.sql_optimizer_tests.departments[dept_id#13108,dept_name#13109,location#13110] parquet


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.errors.QueryCompilationErrors$.columnNotInGroupByClauseError(QueryCompilationErrors.scala:5682)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.checkExpr$1(ExprUtils.scala:310)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.$anonfun$assertValidAggregation$10(ExprUtils.scala:341)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.$anonfun$assertValidAggregation$10$adapted(ExprUtils.scala:341)
	at scala.collection.immutable.List.foreach(List.scala:334)
	at org.apache.spark.sql.catalyst.expressions.ExprUtils$.assertValidAggregation(ExprUtils.scala:341)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:779)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2$adapted(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:377)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
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
*Generated: 2026-06-05 10:33:45*
