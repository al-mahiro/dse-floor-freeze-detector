# Floor-price timeline: sources and verification status

`dse_floor.timeline.FLOOR_PERIODS` was compiled by the thesis authors from BSEC orders and press coverage. This page records what each regime rests on. It is a working audit trail, not a legal reference: **check the primary orders before reusing the timeline in new work.**

Verification notes come from the authors' chronology check (a document in the thesis Drive, "Verify Floor Price Chronology"). Newspaper items are cited by outlet, headline and date only.

| Period (effective sessions) | Regime | Basis | Status |
|---|---|---|---|
| 19 Mar 2020 - 7 Apr 2021 | all securities | BSEC instruction of 19 Mar 2020; floor = average of the previous five sessions. Covered by The Business Standard, New Age, The Daily Star, Dhaka Tribune and Prothom Alo (19 Mar 2020), and independently by the Bangladesh Bank Financial Stability Report | Verified in chronology check |
| 8 Apr 2021 - 5 Jun 2021 | 66 exempted | Decision 7 Apr 2021, effective 8 Apr. The Daily Star (7 Apr 2021), The Financial Express (8 Apr 2021); BSEC order on 66 companies (11 Apr 2021) | Verified |
| 6 Jun 2021 - 17 Jun 2021 | 96 exempted (66 + 30) | Announced 3 Jun 2021, effective the next session. The Business Standard printed the 30-name list, which matches `COMPANIES_30`; New Age confirms 96 withdrawn | Verified, including the 30-name list |
| 18 Jun 2021 - 30 Jul 2022 | no floor | BSEC order of 17 Jun 2021 removed floors from the remaining 240 companies (New Age, The Business Standard, The Daily Star) | Verified |
| 31 Jul 2022 - 21 Dec 2022 | all securities | BSEC Order BSEC/CMRRCD/2001-07/39 of 28 Jul 2022; floor = average close of 28 Jul and the four prior sessions, so the first session trading against it is 31 Jul | Verified; effective-session date derived from the order |
| 22 Dec 2022 - 1 Mar 2023 | 168 exempted | Order of 21 Dec 2022 (bdnews24, BSS, The Financial Express). Press reports say 169; the code uses 168 (see note below) | Revised after the chronology check; re-verify |
| 2 Mar 2023 - 18 Jan 2024 | all securities | BSEC Order BSEC/CMRRCD/2009-193/55 of 1 Mar 2023 re-imposed the floor on the 169-company group. The code treats every other security as still floored under the July 2022 order | Revised after the chronology check; re-verify |
| 21 Jan 2024 - 22 Jan 2024 | 35 securities | Order of 18 Jan 2024 retained the floor for 35 companies; The Daily Star printed the list, which matches `COMPANIES_35` | Verified |
| 23 Jan 2024 - 28 Aug 2024 | 12, then 9, 8, 7, 6 | 12 from 23 Jan 2024; later releases (7 Feb, 3 Mar, 4 Mar, 19 Mar 2024) are in the source comments | Partly verified; later releases to be re-checked |
| 29 Aug 2024 - 8 Jun 2026 | 2 (BEXIMCO, ISLAMIBANK) | Last 4 freed after a 28 Aug 2024 meeting. The 8 Aug 2024 order for the last 6 was cancelled on 11 Aug and never took effect | To be re-checked |
| from 9 Jun 2026 | no floor | Withdrawal of the remaining floors | To be re-checked |

## Open points

- **168 versus 169.** The chronology check found 169 securities exempted in December 2022. The code uses 168: the 169-list minus `ASIAINS` and `FARCHEM`, plus `NLI1STMF`, reflecting differences between the December and March order attachments. The attachments should be compared line by line.
- **Dec 2022 - Mar 2023 effect.** Securities outside the 169 are assumed to keep their July 2022 floor throughout. This matters for every stock outside the list.
- **Announcement versus effective date.** Boundaries use the first session a rule bound. Intraday timing of the 17 Jun 2021 order is not verified.
- **Resets inside a block.** Floors can be re-based within one regime (for example, BEXIMCO's floor moved from 115.60 to 110.10 on 27 Nov 2024 after a stock dividend). The detector estimates one floor per block and does not model this; see its docstring.

Primary documents the authors collected include the BSEC order of 28 Jul 2022 and the BSEC Quarterly Review for October-December 2022.
