"""
SQL Optimizer - Core optimization functions using Databricks Llama 3.3 70B
"""

import json
import time
import hashlib
from typing import Dict, Any

# Import prompt loader
try:
    from .prompt_loader import load_prompts, format_system_prompt, format_user_prompt, get_llm_config
    PROMPTS_CONFIG = load_prompts()
except (ImportError, FileNotFoundError):
    # Fallback: prompts hardcoded (for backwards compatibility)
    PROMPTS_CONFIG = None


def detect_complex_query(query: str) -> Dict[str, Any]:
    """
    Detect if query has complex patterns that make CTE collapse risky.
    Returns detection results with recommendations.
    """
    query_upper = query.upper()
    
    # Count CTEs
    cte_count = query_upper.count('WITH ') + query_upper.count('WITH\n')
    
    # Count window functions
    window_functions = ['RANK(', 'ROW_NUMBER(', 'DENSE_RANK(', 'LAG(', 'LEAD(', 
                        'FIRST_VALUE(', 'LAST_VALUE(', 'NTH_VALUE(', 'NTILE(',
                        'AVG(', 'SUM(', 'COUNT(', 'MIN(', 'MAX(']
    window_count = sum(1 for wf in window_functions if wf in query_upper and 'OVER' in query_upper)
    
    # Detect GROUP BY
    has_group_by = 'GROUP BY' in query_upper
    
    is_complex = (cte_count >= 3 and window_count >= 2) or (cte_count >= 4)
    
    return {
        'is_complex': is_complex,
        'cte_count': cte_count,
        'window_count': window_count,
        'has_group_by': has_group_by,
        'recommendation': 'conservative' if is_complex else 'aggressive'
    }


def optimize_sql(query: str, llm_client, llm_provider: str = "databricks-meta-llama-3-3-70b-instruct", 
                 prompts_config: Dict = None) -> Dict[str, Any]:
    """
    Optimize SQL query using Databricks Llama 3.3 70B model.
    
    Args:
        query: SQL query to optimize
        llm_client: MLflow deployment client
        llm_provider: LLM endpoint name
        prompts_config: Optional external prompts configuration (overrides default)
    
    Returns:
        Dictionary with optimization results
    """
    
    if not llm_client or not llm_provider:
        return {
            "success": False,
            "error": "No LLM client available.",
            "original_sql": query,
            "optimized_sql": query
        }
    
    # Use provided config or load from file
    config = prompts_config or PROMPTS_CONFIG
    
    # Detect query complexity
    complexity = detect_complex_query(query)
    
    # Build prompts from configuration if available
    if config:
        try:
            system_prompt = format_system_prompt(config, complexity['recommendation'], complexity)
            user_prompt = format_user_prompt(config, query)
            llm_config = get_llm_config(config)
            
            llm_provider = llm_config.get('endpoint', llm_provider)
            temperature = llm_config.get('temperature', 0.1)
            max_tokens = llm_config.get('max_tokens', 2000)
            
            print(f"✅ Using prompts from config/prompts.yaml ({complexity['recommendation'].upper()} mode)")
        except Exception as e:
            print(f"⚠️ Error loading prompts config: {e}. Using hardcoded prompts.")
            config = None
    
    # Fallback to hardcoded prompts if no config
    if not config:
        temperature = 0.1
        max_tokens = 2000
        
        if complexity['recommendation'] == 'conservative':
            optimization_strategy = f"""⚠️ CONSERVATIVE OPTIMIZATION MODE

This query has {complexity['cte_count']} CTEs and {complexity['window_count']} window functions - high complexity detected.

🚫 DO NOT ATTEMPT TO:
- Collapse or combine CTEs (keep them separate)
- Restructure window functions
- Change aggregation logic

✅ SAFE OPTIMIZATIONS ONLY:
- Replace YEAR(date) with date range filters (e.g., date >= '2024-01-01' AND date < '2025-01-01')
- Replace MONTH(date) with date range filters
- Remove CONCAT() from join conditions when not needed
- Remove unnecessary CAST() operations
- Replace CROSS JOIN with INNER JOIN where appropriate
- Keep ALL CTEs intact - DO NOT collapse them
"""
        else:
            optimization_strategy = """✅ FULL OPTIMIZATION MODE

You MAY optimize:
- Replace CROSS JOIN with INNER JOIN
- Replace YEAR/MONTH functions with date range filters (>= and <)
- Remove CAST() when not needed
- Remove CONCAT() from join conditions
- Collapse multiple CTEs into a single efficient query when they can be combined
- Remove redundant joins (e.g. joining to same CTE twice)
- Push down WHERE filters into CTEs when possible
- Combine aggregations that scan the same table
"""
        
        system_prompt = f"""You are an expert SQL optimization assistant for Databricks/Spark SQL.

{optimization_strategy}

YOUR TASK:
1. Identify performance issues (SELECT *, CROSS JOIN, function-wrapped predicates, non-sargable WHERE clauses, etc.)
2. Provide an optimized version following the strategy above
3. Explain what you found and why optimizations improve performance

CRITICAL RULES - MUST FOLLOW:
1. Keep query logic IDENTICAL - must return EXACT same results
2. Use ONLY column names from the original query - DO NOT invent or change column names
3. NEVER EVER remove UPPER() or LOWER() functions - they change results!
4. Preserve all LIKE patterns exactly as written
5. If SELECT creates column aliases, use those ALIASES in ORDER BY, not original column names
6. If original has SELECT *, keep SELECT * (don't expand it)

Return ONLY valid JSON format (no markdown, no code blocks):
{{
  "issues_found": ["issue 1", "issue 2"],
  "optimized_sql": "optimized SQL here",
  "explanation": "detailed explanation"
}}"""
        
        user_prompt = f"""Analyze and optimize this SQL query:

```sql
{query}
```

Provide optimized SQL and explanation in JSON format."""
    
    try:
        response = llm_client.predict(
            endpoint=llm_provider,
            inputs={
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        result_text = response['choices'][0]['message']['content']
        
        # Parse JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = json.loads(result_text, strict=False)
        
        output = {
            "success": True,
            "original_sql": query,
            "optimized_sql": result.get("optimized_sql", query),
            "issues_found": result.get("issues_found", []),
            "explanation": result.get("explanation", "No explanation provided"),
            "llm_provider": llm_provider,
            "optimization_mode": complexity['recommendation'].upper(),
            "complexity_details": f"CTEs: {complexity['cte_count']}, Windows: {complexity['window_count']}",
            "prompts_source": "config/prompts.yaml" if config else "hardcoded"
        }
        
        return output
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "original_sql": query,
            "optimized_sql": query
        }


def compare_query_results(original_sql: str, optimized_sql: str, spark_session) -> Dict[str, Any]:
    """
    Execute both queries and compare results to ensure they're identical.
    
    Args:
        original_sql: Original SQL query
        optimized_sql: Optimized SQL query
        spark_session: Spark session to execute queries
    
    Returns:
        Dictionary with validation results
    """
    
    report = {
        "match": False,
        "original_count": 0,
        "optimized_count": 0,
        "original_columns": 0,
        "optimized_columns": 0,
        "column_names_match": False,
        "data_checksum_match": False,
        "differences": [],
        "execution_times": {},
        "error": None
    }
    
    # First, validate optimized SQL syntax by attempting EXPLAIN
    try:
        spark_session.sql(f"EXPLAIN {optimized_sql}")
    except Exception as e:
        error_msg = str(e)
        report["error"] = f"SQL Syntax Error: {error_msg}"
        report["differences"].append(f"Invalid SQL: {error_msg[:200]}")
        return report
    
    try:
        # Execute original
        start = time.time()
        df_original = spark_session.sql(original_sql)
        original_count = df_original.count()
        original_time = time.time() - start
        
        # Execute optimized
        start = time.time()
        df_optimized = spark_session.sql(optimized_sql)
        optimized_count = df_optimized.count()
        optimized_time = time.time() - start
        
        report["original_count"] = original_count
        report["optimized_count"] = optimized_count
        report["execution_times"] = {
            "original": original_time,
            "optimized": optimized_time,
            "speedup": original_time / optimized_time if optimized_time > 0 else 0
        }
        
        # Compare counts
        if original_count != optimized_count:
            report["differences"].append(f"Row count mismatch: {original_count} vs {optimized_count}")
        
        # Compare columns
        original_cols = df_original.columns
        optimized_cols = df_optimized.columns
        report["original_columns"] = len(original_cols)
        report["optimized_columns"] = len(optimized_cols)
        
        if len(original_cols) != len(optimized_cols):
            report["differences"].append(f"Column count mismatch")
        
        report["column_names_match"] = set(original_cols) == set(optimized_cols)
        if not report["column_names_match"]:
            report["differences"].append(f"Column names differ")
        
        # Compare data if counts match
        if original_count == optimized_count and len(original_cols) == len(optimized_cols):
            cols_sorted = sorted(original_cols)
            df_original_sorted = df_original.select(cols_sorted).orderBy(cols_sorted)
            df_optimized_sorted = df_optimized.select(cols_sorted).orderBy(cols_sorted)
            
            if original_count <= 10000:
                original_hash = hashlib.md5(str(df_original_sorted.collect()).encode()).hexdigest()
                optimized_hash = hashlib.md5(str(df_optimized_sorted.collect()).encode()).hexdigest()
                
                report["data_checksum_match"] = (original_hash == optimized_hash)
                if not report["data_checksum_match"]:
                    report["differences"].append("Data checksums don't match")
        
        report["match"] = len(report["differences"]) == 0
        return report
        
    except Exception as e:
        report["error"] = str(e)
        report["differences"].append(f"Execution error: {e}")
        return report
