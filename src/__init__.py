"""
SQL Optimizer - LLM-powered SQL query optimization for Databricks

This package provides intelligent SQL optimization using Databricks Foundation Models.
"""

__version__ = "1.0.0"

from .optimizer import detect_complex_query, optimize_sql, compare_query_results
from .git_utils import clone_or_pull_repo, find_sql_files, commit_and_push
from .report_generator import create_validation_report, save_optimization_results

__all__ = [
    'detect_complex_query',
    'optimize_sql',
    'compare_query_results',
    'clone_or_pull_repo',
    'find_sql_files',
    'commit_and_push',
    'create_validation_report',
    'save_optimization_results',
]
