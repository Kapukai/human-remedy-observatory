#!/usr/bin/env python3
"""Illustrative planning only: two proportions, equal allocation, no inference.

Normal approximation without continuity correction. Baseline/effect/ICC are
assumptions, not estimates from the historical atlas. Standard library only.
"""

import json
from math import ceil, sqrt
from statistics import NormalDist


def main():
    p0, alpha, power, attrition = .20, .05, .80, .15
    observed_per_office, icc = 20, .05
    deff = 1 + (observed_per_office - 1) * icc
    enroll_per_office = ceil(observed_per_office / (1 - attrition))
    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_power = NormalDist().inv_cdf(power)
    rows = []
    for p1 in [.25, .30, .35]:
        pbar = (p0 + p1) / 2
        n = ceil((z_alpha * sqrt(2 * pbar * (1 - pbar))
                  + z_power * sqrt(p0 * (1 - p0) + p1 * (1 - p1))) ** 2
                 / (p1 - p0) ** 2)
        offices_per_arm = ceil(n * deff / observed_per_office)
        rows.append({
            "baseline": p0,
            "intervention_probability_assumed": p1,
            "difference_percentage_points": round(100 * (p1 - p0), 2),
            "evaluable_per_arm": n,
            "evaluable_total": 2 * n,
            "independent_enrollment_total": 2 * ceil(n / (1 - attrition)),
            "illustrative_cluster_offices_per_arm": offices_per_arm,
            "illustrative_cluster_enrollment_total": 2 * offices_per_arm * enroll_per_office,
        })
    print(json.dumps({
        "status": "planning assumptions; not atlas results or tested hypotheses",
        "alpha_two_sided": alpha,
        "power": power,
        "attrition_assumed": attrition,
        "icc_assumed": icc,
        "observed_cases_per_office_assumed": observed_per_office,
        "enrollment_per_office": enroll_per_office,
        "design_effect": deff,
        "scenarios": rows,
    }, indent=2))


if __name__ == "__main__":
    main()
