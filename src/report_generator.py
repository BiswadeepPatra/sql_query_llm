"""
Report Generation - Create markdown validation reports
"""

import os
from typing import Dict
from datetime import datetime


def create_validation_report(sql_name: str, optimization_result: Dict, validation_result: Dict) -> str:
    """
    Create a markdown validation report for a single SQL file.
    """
    
    # Calculate performance metrics
    original_time = validation_result.get('execution_times', {}).get('original', 0)
    optimized_time = validation_result.get('execution_times', {}).get('optimized', 0)
    speedup = validation_result.get('execution_times', {}).get('speedup', 0)
    time_saved = original_time - optimized_time
    time_saved_pct = (time_saved / original_time * 100) if original_time > 0 else 0
    
    # Get optimization mode if available
    opt_mode = optimization_result.get('optimization_mode', 'N/A')
    complexity = optimization_result.get('complexity_details', 'N/A')
    
    md = f"""# Validation Report: {sql_name}

## Summary

 Metric | Value |
--------|-------|
 **Overall Status** | {'✅ PASSED' if validation_result.get('match') else '❌ FAILED'} |
 **Optimization Mode** | {opt_mode} |
 **Complexity** | {complexity} |
 **Row Count** | {validation_result.get('original_count', 'N/A')} |
 **Column Count** | {validation_result.get('original_columns', 'N/A')} |

## Performance Improvement

 Metric | Original | Optimized | Improvement |
--------|----------|-----------|-------------|
 **Execution Time** | {original_time:.2f}s | {optimized_time:.2f}s | {time_saved:.2f}s saved ({time_saved_pct:.1f}% faster) |
 **Speedup Factor** | 1.0x | {speedup:.2f}x | {speedup:.2f}x faster |

## Validation

- {'✅' if validation_result.get('original_count') == validation_result.get('optimized_count') else '❌'} **Row Count**: {validation_result.get('original_count')} rows
- {'✅' if validation_result.get('column_names_match') else '❌'} **Column Names**: {validation_result.get('original_columns')} columns
- {'✅' if validation_result.get('data_checksum_match') else '❌'} **Data Checksum**: {'Match' if validation_result.get('data_checksum_match') else 'Differ'}

## Issues Found & Fixed

"""
    
    if optimization_result.get('issues_found'):
        for idx, issue in enumerate(optimization_result['issues_found'], 1):
            md += f"{idx}. {issue}\n"
    else:
        md += "No major issues found. Query is already well-optimized.\n"
    
    md += f"\n## Optimization Explanation\n\n{optimization_result.get('explanation', 'No explanation provided')}\n"
    
    if validation_result.get('error'):
        md += f"\n## Validation Error\n\n```\n{validation_result['error']}\n```\n"
    
    md += f"\n---\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return md


def save_optimization_results(sql_file: Dict, optimization_result: Dict, validation_result: Dict, output_base: str) -> Dict[str, str]:
    """
    Save optimized SQL and validation report to organized folder structure.
    """
    
    # Create folder for this SQL file
    sql_folder = os.path.join(output_base, sql_file['name'])
    os.makedirs(sql_folder, exist_ok=True)
    
    paths = {}
    
    # Save original SQL
    original_sql_path = os.path.join(sql_folder, f"{sql_file['name']}_original.sql")
    with open(original_sql_path, 'w', encoding='utf-8') as f:
        f.write(sql_file['content'])
    paths['original_sql'] = original_sql_path
    
    # Save optimized SQL
    optimized_sql_path = os.path.join(sql_folder, f"{sql_file['name']}_optimized.sql")
    with open(optimized_sql_path, 'w', encoding='utf-8') as f:
        f.write(optimization_result['optimized_sql'])
    paths['optimized_sql'] = optimized_sql_path
    
    # Save validation report
    validation_md_path = os.path.join(sql_folder, f"{sql_file['name']}_validation.md")
    report_content = create_validation_report(sql_file['name'], optimization_result, validation_result)
    with open(validation_md_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    paths['validation_md'] = validation_md_path
    
    return paths
