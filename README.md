# The Black Spatula Project

## Overview

The goal of this project is to evaluate whether AI models (initially OpenAI's "o1" and possibly "o1-pro") can reliably identify factual, logical, and mathematical errors in published scientific papers. We will measure:

- Number of errors detected
- Severity of identified errors
- False positive rate
- Effort required to verify AI findings

## Background

This project is named after a recent high-profile paper on black plastic kitchen utensils that contained a simple but consequential math error. This mistake, which passed peer review, could have been flagged by an AI reviewer.

## Manual o1 Prompt

```markdown
Please carefully review the following research article (provided in full text below). I want you to focus on verifying the accuracy of all arithmetic calculations, unit conversions, numerical comparisons, and quantitative interpretations presented. For each identified issue or area of concern, explain in detail:

1. What the calculation, unit conversion, or numeric claim is supposed to represent.
2. The step-by-step reasoning or arithmetic that the authors appear to have used.
3. Any errors, inconsistencies, or suspicious values you find, along with the correct calculation or a more appropriate method.
4. Whether the numeric results are reasonable in the context of the data, methods, and known standards.

If no errors are found, summarize the checks you performed and confirm that the numbers appear consistent and plausible. Aim to be as thorough, clear, and evidence-based as possible in your analysis.
```