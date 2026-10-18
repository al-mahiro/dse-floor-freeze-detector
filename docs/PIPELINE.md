# Thesis pipeline and project status

**Thesis:** *Mitigating Regulatory Price Freeze Bias in Regime-Aware Portfolio Optimization: A Hybrid Framework for the Dhaka Stock Exchange (DSE).*
Authors: Abdullah Al Mahi, Saptaporna Dey. Supervisor: Dr. Nafisa Mahbub. BUET, Department of Industrial and Production Engineering.

## Research question

When a regulator floors prices for long periods, recorded closes stop reflecting market equilibrium. Does correcting that bias before regime detection and portfolio construction improve out-of-sample decisions? The design runs **raw** and **corrected** data through the *same* downstream pipeline and compares the results with significance tests.

## Pipeline

| Step | Component | Purpose | Main output | Status |
|---|---|---|---|---|
| 1 | Data collection and cleaning | Clean OHLCV data, trading-day returns | cleaned panel | **In this repo** |
| 2 | BSEC floor-period classification | When did a floor apply to each stock | `Floor_Period_Flag` | **In this repo** |
| 3 | Rule-based floor detector | Which closes were frozen, estimated floor level | `Floor_Locked_Flag`, `Floor_Price` | **In this repo**; run on two pilot stocks |
| 4 | Censored stochastic volatility (CSV) | Recover latent returns under a one-sided floor | corrected series plus posterior uncertainty | Implemented; being re-estimated on the revised timeline. Not released |
| 5 | 3-state HMM | Bull, bear and transitional regimes from corrected returns | regime label | Planned |
| 6A | Heterogeneous-agent model (HAM) with genetic-algorithm calibration | Strategy signals from interacting trader types | HAM signal | Planned |
| 6B | XGBoost | Next-period return forecast | return forecast | Planned (exploratory runs only) |
| 7 | Regime-aware CVaR optimisation | Portfolio under return, risk, allocation and turnover constraints (Rockafellar-Uryasev linear program) | portfolio weights | Planned |
| 8 | Walk-forward backtest and significance tests | Raw versus corrected out-of-sample comparison | performance tables | Planned |

Planned milestones: HAM parameters converged by early February 2027, pipeline integrated by mid-March 2027, significance tests complete by late April 2027, submission 7 May 2027.

## Tooling planned for later steps

The 3-state HMM is planned with `hmmlearn`; the CVaR step is a linear program.

## Design notes for Step 4 (not in this repo)

- The CSV model follows Hsieh and Yang (2009, *Journal of Empirical Finance* 16, 337-351), specialised to a **one-sided lower bound**: the BSEC rule is a floor only, so the upper-limit branch of the original two-sided circuit-breaker model is dropped.
- Posterior convergence is judged with the Gelman-Rubin statistic across parallel chains.
- Open modelling questions include how to treat release days under the daily circuit breaker, and what volatility ordering between "discard locked days", "ignore the floor" and "CSV" should be expected under a floor (as opposed to the daily-limit setting of the original paper).

## References

- Hsieh, S.-F. and Yang, T.-L. (2009). *Journal of Empirical Finance*, 16, 337-351. (censored stochastic volatility under daily price limits)
- Rockafellar, R. T. and Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk*, 2, 21-42.
