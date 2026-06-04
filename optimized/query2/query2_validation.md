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
3. Using function-wrapped predicates (YEAR, UPPER, LOWER, CAST, SUBSTRING, CHARINDEX, LEN)
4. Using non-sargable WHERE clauses (SUBSTRING, CHARINDEX, LEN)
5. Using subquery in the WHERE clause without optimization

## Optimization Explanation


    The original query has several performance issues. 
    1. Using SELECT * instead of selecting only necessary columns can lead to unnecessary data transfer and processing. 
    2. Using CROSS JOIN instead of INNER JOIN can result in a much larger result set than necessary, leading to slower query performance. 
    3. Using function-wrapped predicates (YEAR, UPPER, LOWER, CAST, SUBSTRING, CHARINDEX, LEN) can prevent the database from using indexes, leading to slower query performance. 
    4. Using non-sargable WHERE clauses (SUBSTRING, CHARINDEX, LEN) can also prevent the database from using indexes. 
    5. Using a subquery in the WHERE clause without optimization can lead to slower query performance.

    The optimized query addresses these issues by:
    1. Selecting only the necessary columns.
    2. Using INNER JOIN instead of CROSS JOIN to reduce the result set size.
    3. Removing function-wrapped predicates and replacing them with equivalent, index-friendly conditions.
    4. Replacing non-sargable WHERE clauses with sargable ones.
    5. Optimizing the subquery in the WHERE clause by using a date range instead of the MONTH function.

    Note: The SUBSTRING_INDEX function is used instead of SUBSTRING and CHARINDEX to extract the domain from the email address. This is a more efficient and readable way to achieve the same result.

    Also, the date range in the WHERE clause is optimized to use a single condition instead of two separate conditions for the year and month. This allows the database to use an index on the sale_date column more efficiently.
  

## Validation Error

```
[TABLE_OR_VIEW_NOT_FOUND] The table or view `sales` cannot be found. Verify the spelling and correctness of the schema and catalog.
If you did not qualify the name with a schema, verify the current_schema() output, or qualify the name with the correct schema and catalog.
To tolerate the error on drop use DROP VIEW IF EXISTS or DROP TABLE IF EXISTS. SQLSTATE: 42P01; line 8 pos 9;
'Sort ['base_data.sale_date DESC NULLS LAST, 'base_data.amount DESC NULLS LAST], true
+- 'Distinct
   +- 'Project [*]
      +- 'Filter 'base_data.sale_id IN (list#17872 [])
         :  +- 'Project ['sale_id]
         :     +- 'Filter (('MONTH('sale_date) >= 6) AND ('MONTH('sale_date) <= 12))
         :        +- 'UnresolvedRelation [sales], [], false
         +- 'SubqueryAlias base_data
            +- 'Project [s.*, c.*, p.*, d.*]
               +- 'Filter (((('s.customer_id = 'c.customer_id) AND ('s.product_id = 'p.product_id)) AND (('p.dept_id = 'd.dept_id) AND ('YEAR('s.sale_date) = 2023))) AND ((('UPPER('c.country) = USA) AND ('LOWER('p.category) = electronics)) AND ((cast('s.amount as int) > 1000) AND 'SUBSTRING('c.email, ('CHARINDEX(@, 'c.email) + 1), 'LEN('c.email)) IN (list#17871 []))))
                  :  +- 'Distinct
                  :     +- 'Project ['domain]
                  :        +- 'UnresolvedRelation [approved_domains], [], false
                  +- 'Join Cross
                     :- 'Join Cross
                     :  :- 'Join Cross
                     :  :  :- 'SubqueryAlias s
                     :  :  :  +- 'UnresolvedRelation [sales], [], false
                     :  :  +- 'SubqueryAlias c
                     :  :     +- 'UnresolvedRelation [customers], [], false
                     :  +- 'SubqueryAlias p
                     :     +- 'UnresolvedRelation [products], [], false
                     +- 'SubqueryAlias d
                        +- 'UnresolvedRelation [departments], [], false


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.catalyst.analysis.package$AnalysisErrorAt.tableNotFound(package.scala:94)
	at org.apache.spark.sql.catalyst.analysis.RelationResolution$.throwTableNotFound(RelationResolution.scala:1126)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:355)
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

- Execution error: [TABLE_OR_VIEW_NOT_FOUND] The table or view `sales` cannot be found. Verify the spelling and correctness of the schema and catalog.
If you did not qualify the name with a schema, verify the current_schema() output, or qualify the name with the correct schema and catalog.
To tolerate the error on drop use DROP VIEW IF EXISTS or DROP TABLE IF EXISTS. SQLSTATE: 42P01; line 8 pos 9;
'Sort ['base_data.sale_date DESC NULLS LAST, 'base_data.amount DESC NULLS LAST], true
+- 'Distinct
   +- 'Project [*]
      +- 'Filter 'base_data.sale_id IN (list#17872 [])
         :  +- 'Project ['sale_id]
         :     +- 'Filter (('MONTH('sale_date) >= 6) AND ('MONTH('sale_date) <= 12))
         :        +- 'UnresolvedRelation [sales], [], false
         +- 'SubqueryAlias base_data
            +- 'Project [s.*, c.*, p.*, d.*]
               +- 'Filter (((('s.customer_id = 'c.customer_id) AND ('s.product_id = 'p.product_id)) AND (('p.dept_id = 'd.dept_id) AND ('YEAR('s.sale_date) = 2023))) AND ((('UPPER('c.country) = USA) AND ('LOWER('p.category) = electronics)) AND ((cast('s.amount as int) > 1000) AND 'SUBSTRING('c.email, ('CHARINDEX(@, 'c.email) + 1), 'LEN('c.email)) IN (list#17871 []))))
                  :  +- 'Distinct
                  :     +- 'Project ['domain]
                  :        +- 'UnresolvedRelation [approved_domains], [], false
                  +- 'Join Cross
                     :- 'Join Cross
                     :  :- 'Join Cross
                     :  :  :- 'SubqueryAlias s
                     :  :  :  +- 'UnresolvedRelation [sales], [], false
                     :  :  +- 'SubqueryAlias c
                     :  :     +- 'UnresolvedRelation [customers], [], false
                     :  +- 'SubqueryAlias p
                     :     +- 'UnresolvedRelation [products], [], false
                     +- 'SubqueryAlias d
                        +- 'UnresolvedRelation [departments], [], false


JVM stacktrace:
org.apache.spark.sql.catalyst.ExtendedAnalysisException
	at org.apache.spark.sql.catalyst.analysis.package$AnalysisErrorAt.tableNotFound(package.scala:94)
	at org.apache.spark.sql.catalyst.analysis.RelationResolution$.throwTableNotFound(RelationResolution.scala:1126)
	at org.apache.spark.sql.catalyst.analysis.CheckAnalysis.$anonfun$checkAnalysis0$2(CheckAnalysis.scala:355)
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
*Generated: 2026-06-04 08:29:30*
