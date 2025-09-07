# XAI Methods Comparison Report

**Generated:** 2025-09-07 05:36:49
**Methods Compared:** LIME, SHAP, SRTA
**Sample Size:** 50

## Executive Summary

This report compares three explanation evaluation approaches:
- **LIME**: Local Interpretable Model-agnostic Explanations
- **SHAP**: SHapley Additive exPlanations  
- **SRTA**: Self-Anchored Rationale & Teleology Architecture

## Method Performance Statistics


### LIME Results
- **Status:** Failed to compute (constant values or errors)

### SHAP Results
- **Status:** Failed to compute (constant values or errors)

### SRTA Results
- **Mean Score:** 34.42 Å} 0.07
- **Correlation with Task Performance:**
  - Spearman Éœ = -0.396 (p = 0.004)
  - Pearson r = -0.641 (p = 0.000)


## Cross-Method Correlations

How well do the different methods agree with each other?


## Key Findings

### Task Performance Correlations

**Strongest correlation with task performance:** SRTA (Éœ = -0.396)

**Method Ranking by Correlation Strength:**
1. SRTA: Éœ = -0.396


## Implications for SRTA Evaluation

Based on this comparison:

- **SRTA shows negative correlation**, consistent with previous findings


## Limitations

- **Synthetic data:** Analysis used simplified test cases, not real-world explanations
- **Dummy classifier:** LIME/SHAP applied to basic classifier, not production model
- **Small sample size:** 50 samples may be insufficient for robust conclusions
- **Simplified task performance:** Synthetic performance metric may not reflect real utility

## Recommendations

1. **If SRTA correlations are weaker than LIME/SHAP:** Focus on improving SRTA methodology
2. **If all methods show similar patterns:** Reconsider task performance metric validity
3. **If SRTA performs comparably:** Consider SRTA as viable alternative approach
4. **For production validation:** Test all methods on real models with human evaluation

---

**Data Files:**
- Raw results: `xai_comparison_results.json`
- Statistical analysis: `xai_correlation_analysis.json`
- Tabular data: `xai_comparison_results.csv`
