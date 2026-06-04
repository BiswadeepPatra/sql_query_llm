# Validation Report: query2

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

1. Using SELECT * instead of selecting only necessary columns
2. Using CROSS JOIN instead of INNER JOIN
3. Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) which can prevent index usage
4. Using non-sargable WHERE clauses (LIKE with a wildcard at the beginning)
5. Using a subquery in the WHERE clause which can be slow for large datasets

## Optimization Explanation


    The original query has several performance issues. 
    1. Using SELECT * instead of selecting only necessary columns can lead to unnecessary data transfer and processing.
    2. Using CROSS JOIN instead of INNER JOIN can result in a much larger result set than necessary, leading to slower performance.
    3. Using function-wrapped predicates (YEAR, MONTH, UPPER, LOWER, CAST) can prevent the database from using indexes, leading to slower performance.
    4. Using non-sargable WHERE clauses (LIKE with a wildcard at the beginning) can prevent the database from using indexes, leading to slower performance.
    5. Using a subquery in the WHERE clause can be slow for large datasets.

    The optimized query addresses these issues by:
    1. Selecting only the necessary columns.
    2. Using INNER JOIN instead of CROSS JOIN to reduce the result set size.
    3. Replacing function-wrapped predicates with equivalent expressions that allow index usage.
    4. Replacing the non-sargable LIKE clause with a sargable one (although this may not be possible if the wildcard must be at the beginning).
    5. Using an INTERSECT operator instead of a subquery in the WHERE clause to improve performance for large datasets.
  

## Validation Error

```
[NUM_COLUMNS_MISMATCH] INTERSECT can only be performed on inputs with the same number of columns, but the first input has 9 columns and the second input has 1 columns. SQLSTATE: 42826; line 2 pos 4;
'Sort ['s.sale_date DESC NULLS LAST, 's.amount DESC NULLS LAST], true
+- 'Intersect false
   :- Distinct
   :  +- Project [sale_id#20623, emp_id#20624, sale_date#20627, amount#20626, emp_id#20629, dept_id#20631, country#20634, dept_id#20636, dept_name#20637]
   :     +- Filter ((((sale_date#20627 >= cast(2020-01-01 as date)) AND (sale_date#20627 < cast(2020-07-01 as date))) AND (country#20634 = USA)) AND ((amount#20626 > cast(5000.00 as decimal(10,2))) AND dept_name#20637 LIKE %engineering%))
   :        +- Join Inner, (dept_id#20631 = dept_id#20636)
   :           :- Join Inner, (emp_id#20624 = emp_id#20629)
   :           :  :- SubqueryAlias s
   :           :  :  +- SubqueryAlias workspace.sql_optimizer_tests.sales
   :           :  :     +- Relation workspace.sql_optimizer_tests.sales[sale_id#20623,emp_id#20624,product#20625,amount#20626,sale_date#20627,region#20628] parquet
   :           :  +- SubqueryAlias e
   :           :     +- SubqueryAlias workspace.sql_optimizer_tests.employees
   :           :        +- Relation workspace.sql_optimizer_tests.employees[emp_id#20629,emp_name#20630,dept_id#20631,salary#20632,hire_date#20633,country#20634,city#20635] parquet
   :           +- SubqueryAlias d
   :              +- SubqueryAlias workspace.sql_optimizer_tests.departments
   :                 +- Relation workspace.sql_optimizer_tests.departments[dept_id#20636,dept_name#20637,location#20638] parquet
   +- Project [sale_id#20639]
      +- Filter ((sale_date#20643 >= cast(2024-01-01 as date)) AND (sale_date#20643 < cast(2025-01-01 as date)))
         +- SubqueryAlias s
            +- SubqueryAlias workspace.sql_optimizer_tests.sales
               +- Relation workspace.sql_optimizer_tests.sales[sale_id#20639,emp_id#20640,product#20641,amount#20642,sale_date#20643,region#20644] parquet


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.errors.QueryCompilationErrors$.numColumnsMismatch(QueryCompilationErrors.scala:6918)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$41(CheckAnalysis.scala:838)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$41$adapted(CheckAnalysis.scala:830)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:830)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2$adapted(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:377)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0$(CheckAnalysis.scala:295)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis0(Analyzer.scala:554)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis$1(CheckAnalysis.scala:280)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis(CheckAnalysis.scala:267)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis$(CheckAnalysis.scala:263)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis(Analyzer.scala:554)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$resolveInFixedPoint$1(HybridAnalyzer.scala:414)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:266)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.resolveInFixedPoint(HybridAnalyzer.scala:414)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$apply$1(HybridAnalyzer.scala:97)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.withTrackedAnalyzerBridgeState(HybridAnalyzer.scala:134)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.apply(HybridAnalyzer.scala:90)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$2(Analyzer.scala:620)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.markInAnalyzer(AnalysisHelper.scala:425)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$1(Analyzer.scala:620)
	at com.databricks.sql.unity.SAMSnapshotHelper$.visitPlansDuringAnalysis(SAMSnapshotHelper.scala:43)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.executeAndCheck(Analyzer.scala:609)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$3(QueryExecution.scala:580)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:918)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$8(QueryExecution.scala:1028)
	at org.apache.spark.sql.execution.SQLExecution$.$anonfun$withExecutionPhase$1(SQLExecution.scala:318)
	at com.databricks.util.TracingSpanUtils$.withTracing(TracingSpanUtils.scala:250)
	at com.databricks.spark.util.DatabricksTracingHelper.withSpan(DatabricksSparkTracingHelper.scala:154)
	at com.databricks.spark.util.DBRTracing$.withSpan(DBRTracing.scala:87)
	at org.apache.spark.sql.execution.SQLExecution$.withExecutionPhase(SQLExecution.scala:299)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$7(QueryExecution.scala:1028)
	at org.apache.spark.sql.execution.QueryExecution$.withInternalError(QueryExecution.scala:1736)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$5(QueryExecution.scala:1021)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$4(QueryExecution.scala:1018)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$3(QueryExecution.scala:1018)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$2(QueryExecution.scala:1017)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.localBlock$1(QueryExecution.scala:998)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$4(QueryExecution.scala:1008)
	at com.databricks.unity.UCSManager$.withTemporaryScope(UCSManager.scala:168)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$3(QueryExecution.scala:1007)
	at org.apache.spark.sql.execution.QueryExecution$.$anonfun$runWithWrappers$2(QueryExecution.scala:1990)
	at org.apache.spark.sql.execution.QueryExecution$.org$apache$spark$sql$execution$QueryExecution$$runWithWrappers(QueryExecution.scala:1989)
	at org.apache.spark.sql.execution.QueryExecution.withQueryExecutionId(QueryExecution.scala:1008)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$1(QueryExecution.scala:1016)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.execution.QueryExecution.executePhase(QueryExecution.scala:1015)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$2(QueryExecution.scala:571)
	at com.databricks.sql.util.MemoryTrackerHelper.withMemoryTracking(MemoryTrackerHelper.scala:111)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$1(QueryExecution.scala:570)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.analyzed(QueryExecution.scala:634)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyCommandExecuted$1(QueryExecution.scala:639)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.commandExecuted(QueryExecution.scala:644)
	at org.apache.spark.sql.execution.QueryExecution.assertCommandExecuted(QueryExecution.scala:777)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyOptimizedPlan$1(QueryExecution.scala:809)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.optimizedPlan(QueryExecution.scala:863)
	at org.apache.spark.sql.execution.QueryExecution.assertOptimized(QueryExecution.scala:865)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyExecutedPlan$1(QueryExecution.scala:887)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.executedPlan(QueryExecution.scala:922)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$16(SqlGatewayHistorySparkListener.scala:919)
	at scala.util.Try$.apply(Try.scala:217)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$15(SqlGatewayHistorySparkListener.scala:919)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$15$adapted(SqlGatewayHistorySparkListener.scala:918)
	at scala.Option.foreach(Option.scala:437)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$1(SqlGatewayHistorySparkListener.scala:918)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.com$databricks$spark$sqlgateway$history$SqlGatewayHistorySparkListener$$onSqlStart(SqlGatewayHistorySparkListener.scala:821)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener$$anonfun$onOtherEventDefault$1.applyOrElse(SqlGatewayHistorySparkListener.scala:239)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener$$anonfun$onOtherEventDefault$1.applyOrElse(SqlGatewayHistorySparkListener.scala:227)
	at scala.runtime.AbstractPartialFunction.apply(AbstractPartialFunction.scala:35)
	at com.databricks.spark.sqlgateway.history.utils.ScriptStatementHelper$$anonfun$onOtherEvent$1.applyOrElse(ScriptStatementHelper.scala:28)
	at com.databricks.spark.sqlgateway.history.utils.ScriptStatementHelper$$anonfun$onOtherEvent$1.applyOrElse(ScriptStatementHelper.scala:28)
	at scala.PartialFunction$OrElse.applyOrElse(PartialFunction.scala:270)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onOtherEvent$1(SqlGatewayHistorySparkListener.scala:205)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.onOtherEvent(SqlGatewayHistorySparkListener.scala:205)
	at org.apache.spark.scheduler.SparkListenerBus.doPostEvent(SparkListenerBus.scala:108)
	at org.apache.spark.scheduler.SparkListenerBus.doPostEvent$(SparkListenerBus.scala:28)
	at org.apache.spark.scheduler.AsyncEventQueue.doPostEvent(AsyncEventQueue.scala:46)
	at org.apache.spark.scheduler.AsyncEventQueue.doPostEvent(AsyncEventQueue.scala:46)
	at org.apache.spark.util.ListenerBus.postToAll(ListenerBus.scala:216)
	at org.apache.spark.util.ListenerBus.postToAll$(ListenerBus.scala:180)
	at org.apache.spark.scheduler.AsyncEventQueue.super$postToAll(AsyncEventQueue.scala:177)
	at org.apache.spark.scheduler.AsyncEventQueue.$anonfun$dispatch$1(AsyncEventQueue.scala:177)
	at scala.runtime.java8.JFunction0$mcJ$sp.apply(JFunction0$mcJ$sp.scala:17)
	at scala.util.DynamicVariable.withValue(DynamicVariable.scala:59)
	at org.apache.spark.scheduler.AsyncEventQueue.org$apache$spark$scheduler$AsyncEventQueue$$dispatch(AsyncEventQueue.scala:119)
	at org.apache.spark.scheduler.AsyncEventQueue$$anon$2.$anonfun$run$1(AsyncEventQueue.scala:115)
	at org.apache.spark.util.Utils$.tryOrStopSparkContext(Utils.scala:1638)
	at org.apache.spark.scheduler.AsyncEventQueue$$anon$2.run(AsyncEventQueue.scala:115)
```

## Differences Detected

- Execution error: [NUM_COLUMNS_MISMATCH] INTERSECT can only be performed on inputs with the same number of columns, but the first input has 9 columns and the second input has 1 columns. SQLSTATE: 42826; line 2 pos 4;
'Sort ['s.sale_date DESC NULLS LAST, 's.amount DESC NULLS LAST], true
+- 'Intersect false
   :- Distinct
   :  +- Project [sale_id#20623, emp_id#20624, sale_date#20627, amount#20626, emp_id#20629, dept_id#20631, country#20634, dept_id#20636, dept_name#20637]
   :     +- Filter ((((sale_date#20627 >= cast(2020-01-01 as date)) AND (sale_date#20627 < cast(2020-07-01 as date))) AND (country#20634 = USA)) AND ((amount#20626 > cast(5000.00 as decimal(10,2))) AND dept_name#20637 LIKE %engineering%))
   :        +- Join Inner, (dept_id#20631 = dept_id#20636)
   :           :- Join Inner, (emp_id#20624 = emp_id#20629)
   :           :  :- SubqueryAlias s
   :           :  :  +- SubqueryAlias workspace.sql_optimizer_tests.sales
   :           :  :     +- Relation workspace.sql_optimizer_tests.sales[sale_id#20623,emp_id#20624,product#20625,amount#20626,sale_date#20627,region#20628] parquet
   :           :  +- SubqueryAlias e
   :           :     +- SubqueryAlias workspace.sql_optimizer_tests.employees
   :           :        +- Relation workspace.sql_optimizer_tests.employees[emp_id#20629,emp_name#20630,dept_id#20631,salary#20632,hire_date#20633,country#20634,city#20635] parquet
   :           +- SubqueryAlias d
   :              +- SubqueryAlias workspace.sql_optimizer_tests.departments
   :                 +- Relation workspace.sql_optimizer_tests.departments[dept_id#20636,dept_name#20637,location#20638] parquet
   +- Project [sale_id#20639]
      +- Filter ((sale_date#20643 >= cast(2024-01-01 as date)) AND (sale_date#20643 < cast(2025-01-01 as date)))
         +- SubqueryAlias s
            +- SubqueryAlias workspace.sql_optimizer_tests.sales
               +- Relation workspace.sql_optimizer_tests.sales[sale_id#20639,emp_id#20640,product#20641,amount#20642,sale_date#20643,region#20644] parquet


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.errors.QueryCompilationErrors$.numColumnsMismatch(QueryCompilationErrors.scala:6918)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$41(CheckAnalysis.scala:838)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$41$adapted(CheckAnalysis.scala:830)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:830)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2$adapted(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:377)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.trees.TreeNode.$anonfun$foreachUp$1$adapted(TreeNode.scala:376)
	at scala.collection.immutable.Vector.foreach(Vector.scala:2125)
	at org.apache.spark.sql.catalyst.trees.TreeNode.foreachUp(TreeNode.scala:376)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0(CheckAnalysis.scala:324)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis0$(CheckAnalysis.scala:295)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis0(Analyzer.scala:554)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis$1(CheckAnalysis.scala:280)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis(CheckAnalysis.scala:267)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.checkAnalysis$(CheckAnalysis.scala:263)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.checkAnalysis(Analyzer.scala:554)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$resolveInFixedPoint$1(HybridAnalyzer.scala:414)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker$.withTracker(QueryPlanningTracker.scala:266)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.resolveInFixedPoint(HybridAnalyzer.scala:414)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.$anonfun$apply$1(HybridAnalyzer.scala:97)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.withTrackedAnalyzerBridgeState(HybridAnalyzer.scala:134)
	at org.apache.spark.sql.catalyst.analysis.resolver.HybridAnalyzer.apply(HybridAnalyzer.scala:90)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$2(Analyzer.scala:620)
	at org.apache.spark.sql.catalyst.plans.logical.AnalysisHelper$.markInAnalyzer(AnalysisHelper.scala:425)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.$anonfun$executeAndCheck$1(Analyzer.scala:620)
	at com.databricks.sql.unity.SAMSnapshotHelper$.visitPlansDuringAnalysis(SAMSnapshotHelper.scala:43)
	at org.apache.spark.sql.catalyst.analysis.Analyzer.executeAndCheck(Analyzer.scala:609)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$3(QueryExecution.scala:580)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at org.apache.spark.sql.catalyst.QueryPlanningTracker.measurePhase(QueryPlanningTracker.scala:918)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$8(QueryExecution.scala:1028)
	at org.apache.spark.sql.execution.SQLExecution$.$anonfun$withExecutionPhase$1(SQLExecution.scala:318)
	at com.databricks.util.TracingSpanUtils$.withTracing(TracingSpanUtils.scala:250)
	at com.databricks.spark.util.DatabricksTracingHelper.withSpan(DatabricksSparkTracingHelper.scala:154)
	at com.databricks.spark.util.DBRTracing$.withSpan(DBRTracing.scala:87)
	at org.apache.spark.sql.execution.SQLExecution$.withExecutionPhase(SQLExecution.scala:299)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$7(QueryExecution.scala:1028)
	at org.apache.spark.sql.execution.QueryExecution$.withInternalError(QueryExecution.scala:1736)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$5(QueryExecution.scala:1021)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$4(QueryExecution.scala:1018)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$3(QueryExecution.scala:1018)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$2(QueryExecution.scala:1017)
	at com.databricks.util.LexicalThreadLocal$Handle.runWith(LexicalThreadLocal.scala:63)
	at org.apache.spark.sql.execution.QueryExecution.localBlock$1(QueryExecution.scala:998)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$4(QueryExecution.scala:1008)
	at com.databricks.unity.UCSManager$.withTemporaryScope(UCSManager.scala:168)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$withQueryExecutionId$3(QueryExecution.scala:1007)
	at org.apache.spark.sql.execution.QueryExecution$.$anonfun$runWithWrappers$2(QueryExecution.scala:1990)
	at org.apache.spark.sql.execution.QueryExecution$.org$apache$spark$sql$execution$QueryExecution$$runWithWrappers(QueryExecution.scala:1989)
	at org.apache.spark.sql.execution.QueryExecution.withQueryExecutionId(QueryExecution.scala:1008)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$executePhase$1(QueryExecution.scala:1016)
	at org.apache.spark.sql.SparkSession.withActive(SparkSession.scala:866)
	at org.apache.spark.sql.execution.QueryExecution.executePhase(QueryExecution.scala:1015)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$2(QueryExecution.scala:571)
	at com.databricks.sql.util.MemoryTrackerHelper.withMemoryTracking(MemoryTrackerHelper.scala:111)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyAnalyzed$1(QueryExecution.scala:570)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.analyzed(QueryExecution.scala:634)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyCommandExecuted$1(QueryExecution.scala:639)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.commandExecuted(QueryExecution.scala:644)
	at org.apache.spark.sql.execution.QueryExecution.assertCommandExecuted(QueryExecution.scala:777)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyOptimizedPlan$1(QueryExecution.scala:809)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.optimizedPlan(QueryExecution.scala:863)
	at org.apache.spark.sql.execution.QueryExecution.assertOptimized(QueryExecution.scala:865)
	at org.apache.spark.sql.execution.QueryExecution.$anonfun$lazyExecutedPlan$1(QueryExecution.scala:887)
	at scala.util.Try$.apply(Try.scala:217)
	at org.apache.spark.util.Utils$.doTryWithCallerStacktrace(Utils.scala:1765)
	at org.apache.spark.util.Utils$.getTryWithCallerStacktrace(Utils.scala:1815)
	at org.apache.spark.util.LazyTry.get(LazyTry.scala:78)
	at org.apache.spark.sql.execution.QueryExecution.executedPlan(QueryExecution.scala:922)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$16(SqlGatewayHistorySparkListener.scala:919)
	at scala.util.Try$.apply(Try.scala:217)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$15(SqlGatewayHistorySparkListener.scala:919)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$15$adapted(SqlGatewayHistorySparkListener.scala:918)
	at scala.Option.foreach(Option.scala:437)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onSqlStart$1(SqlGatewayHistorySparkListener.scala:918)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.com$databricks$spark$sqlgateway$history$SqlGatewayHistorySparkListener$$onSqlStart(SqlGatewayHistorySparkListener.scala:821)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener$$anonfun$onOtherEventDefault$1.applyOrElse(SqlGatewayHistorySparkListener.scala:239)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener$$anonfun$onOtherEventDefault$1.applyOrElse(SqlGatewayHistorySparkListener.scala:227)
	at scala.runtime.AbstractPartialFunction.apply(AbstractPartialFunction.scala:35)
	at com.databricks.spark.sqlgateway.history.utils.ScriptStatementHelper$$anonfun$onOtherEvent$1.applyOrElse(ScriptStatementHelper.scala:28)
	at com.databricks.spark.sqlgateway.history.utils.ScriptStatementHelper$$anonfun$onOtherEvent$1.applyOrElse(ScriptStatementHelper.scala:28)
	at scala.PartialFunction$OrElse.applyOrElse(PartialFunction.scala:270)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.$anonfun$onOtherEvent$1(SqlGatewayHistorySparkListener.scala:205)
	at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.scala:18)
	at com.databricks.spark.util.FrameProfiler$.$anonfun$record$1(FrameProfiler.scala:114)
	at com.databricks.spark.util.FrameProfilerExporter$.maybeExportFrameProfiler(FrameProfilerExporter.scala:201)
	at com.databricks.spark.util.FrameProfiler$.record(FrameProfiler.scala:105)
	at com.databricks.spark.sqlgateway.history.SqlGatewayHistorySparkListener.onOtherEvent(SqlGatewayHistorySparkListener.scala:205)
	at org.apache.spark.scheduler.SparkListenerBus.doPostEvent(SparkListenerBus.scala:108)
	at org.apache.spark.scheduler.SparkListenerBus.doPostEvent$(SparkListenerBus.scala:28)
	at org.apache.spark.scheduler.AsyncEventQueue.doPostEvent(AsyncEventQueue.scala:46)
	at org.apache.spark.scheduler.AsyncEventQueue.doPostEvent(AsyncEventQueue.scala:46)
	at org.apache.spark.util.ListenerBus.postToAll(ListenerBus.scala:216)
	at org.apache.spark.util.ListenerBus.postToAll$(ListenerBus.scala:180)
	at org.apache.spark.scheduler.AsyncEventQueue.super$postToAll(AsyncEventQueue.scala:177)
	at org.apache.spark.scheduler.AsyncEventQueue.$anonfun$dispatch$1(AsyncEventQueue.scala:177)
	at scala.runtime.java8.JFunction0$mcJ$sp.apply(JFunction0$mcJ$sp.scala:17)
	at scala.util.DynamicVariable.withValue(DynamicVariable.scala:59)
	at org.apache.spark.scheduler.AsyncEventQueue.org$apache$spark$scheduler$AsyncEventQueue$$dispatch(AsyncEventQueue.scala:119)
	at org.apache.spark.scheduler.AsyncEventQueue$$anon$2.$anonfun$run$1(AsyncEventQueue.scala:115)
	at org.apache.spark.util.Utils$.tryOrStopSparkContext(Utils.scala:1638)
	at org.apache.spark.scheduler.AsyncEventQueue$$anon$2.run(AsyncEventQueue.scala:115)

---
*Generated: 2026-06-04 08:43:59*
