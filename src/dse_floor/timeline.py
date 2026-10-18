"""BSEC floor-price regulatory timeline for the Dhaka Stock Exchange (DSE).

The Bangladesh Securities and Exchange Commission (BSEC) imposed a lower
price limit ("floor price") on DSE-listed securities in two phases:

* Phase 1 (COVID-19): 19 Mar 2020 - 17 Jun 2021, relaxed in steps.
* Phase 2: from 28 Jul 2022 until the floor was withdrawn on 9 Jun 2026,
  again relaxed in steps until only two securities remained on a floor.

Each entry of :data:`FLOOR_PERIODS` is a tuple
``(start, end, regime, company_set)`` with inclusive ISO dates, where
``regime`` is one of:

``"ALL"``
    every security was subject to the floor (no company set).
``"EXEMPTED"``
    the listed securities were exempt; every other security kept its floor.
``"WITH_FLOOR"``
    only the listed securities were subject to the floor.

Dates outside every interval are floor-free. Dates are *effective trading
sessions* (the first session a rule bound), not announcement dates; the
comments record how each boundary was derived. DSE trades Sunday-Thursday.

The company lists below were transcribed from BSEC orders by the thesis
authors. Treat the timeline as data that should be re-verified against the
primary orders before reuse in new work.
"""

from __future__ import annotations

from typing import FrozenSet, Optional, Tuple

FloorPeriod = Tuple[str, str, str, Optional[FrozenSet[str]]]

# 66 securities exempted: decided 7 Apr 2021, effective 8 Apr 2021.
COMPANIES_66: FrozenSet[str] = frozenset({
    "PLFSL", "RNSPIN", "BDSERVICE", "IFILISLMF1", "ZAHEENSPIN",
    "RINGSHINE", "OAL", "DBH1STMF", "PF1STMF", "NURANI",
    "REGENTTEX", "SEMLFBSLGF", "ETL", "PDL", "METROSPIN",
    "KTL", "FARCHEM", "DESHBANDHU", "YPL", "SAFKOSPINN",
    "WMSHIPYARD", "CENTRALPHL", "BEACHHATCH", "SIMTEX", "SHEPHERD",
    "HFL", "PRIMETEX", "SAIHAMCOT", "BBS", "GHAIL",
    "AFCAGRO", "BENGALWTL", "KPPL", "SILVAPHL", "IBP",
    "ARGONDENIM", "COPPERTECH", "SHASHADNIM", "SHURWID", "ESQUIRENIT",
    "VFSTDL", "IPDC", "PHOENIXFIN", "ADVENT", "RSRMSTEEL",
    "QUEENSOUTH", "MTB", "OIMEX", "RUPALIBANK", "SAIHAMTEX",
    "SONARGAON", "AIL", "GHCL", "NAVANACNG", "DESCO",
    "UNIQUEHRL", "STANDARINS", "FAREASTLIF", "UTTARAFIN", "USMANIAGL",
    "KPCL", "NAHEEACP", "DULAMIACOT", "SINOBANGLA", "PTL",
    "MLDYEING",
})

# 30 further securities exempted: announced 3 Jun 2021, effective 6 Jun 2021.
COMPANIES_30: FrozenSet[str] = frozenset({
    "RENWICKJA", "MONNOAGML", "BATASHOE", "KOHINOOR", "NORTHERN",
    "STANCERAM", "WATACHEM", "SONALIPAPR", "APEXFOOT", "KAY&QUE",
    "BDAUTOCA", "STYLECRAFT", "GEMINISEA", "ECABLES", "APEXSPINN",
    "MONNOCERA", "BANGAS", "CVOPRL", "ATLASBANG", "APEXTANRY",
    "SAMATALETH", "NTLTUBES", "AZIZPIPES", "SEAPEARL", "HAKKANIPUL",
    "ORIONINFU", "LEGACYFOOT", "SKTRIMS", "NPOLYMAR", "DAFODILCOM",
})

# Cumulative exempted list from 6 Jun 2021.
COMPANIES_96: FrozenSet[str] = COMPANIES_66 | COMPANIES_30

# 169 securities: exempted 21 Dec 2022 - 28 Feb 2023 in the original reading
# of the order; re-floored on 1 Mar 2023.
COMPANIES_169: FrozenSet[str] = frozenset({
    "1STPRIMFMF", "SAVAREFR", "ICBAMCL2ND", "SEMLLECMF", "MEGHNAPET",
    "SHYAMPSUG", "CAPMBDBLMF", "BDSERVICE", "ICBEPMF1S1", "DULAMIACOT",
    "JUTESPINN", "NORTHERN", "AZIZPIPES", "ISNLTD", "ATCSLGF",
    "MITHUNKNIT", "SEMLFBSLGF", "TUNGHAI", "PF1STMF", "IFILISLMF1",
    "ICB3RDNRB", "KPPL", "FIRSTFIN", "RELIANCE1", "MBL1STMF",
    "ANLIMAYARN", "MEGCONMILK", "BDAUTOCA", "FARCHEM", "SAMATALETH",
    "ASIAINS", "AIBL1STIMF", "ZAHINTEX", "NCCBLMF1", "VAMLBDMF1",
    "LEGACYFOOT", "PRIME1ICBA", "ICBSONALI1", "FASFIN", "ICICL",
    "FINEFOODS", "DBH1STMF", "EXIM1STMF", "SAFKOSPINN", "SEMLIBBLSF",
    "PLFSL", "NURANI", "ICBAGRANI1", "PREMIERLEA", "TALLUSPIN",
    "IFIC1STMF", "CAPMIBBLMF", "INTECH", "GQBALLPEN", "BIFC",
    "FAREASTFIN", "IMAMBUTTON", "BANGAS", "GLDNJMF", "STANCERAM",
    "GREENDELMF", "ZEALBANGLA", "ARAMITCEM", "SHURWID", "EBL1STMF",
    "APEXSPINN", "DESHBANDHU", "DSHGARME", "HAKKANIPUL", "VAMLRBBF",
    "MIRACLEIND", "BDWELDING", "AGRANINS", "SINOBANGLA", "ILFSL",
    "ABB1STMF", "DGIC", "REGENTTEX", "OIMEX", "KARNAPHULI",
    "PROGRESLIF", "USMANIAGL", "SONALIANSH", "SONARGAON", "CONTININS",
    "GLOBALINS", "LIBRAINFU", "AMBEEPHA", "UNIONCAP", "KBPPWBIL",
    "ALLTEX", "SIMTEX", "SAMORITA", "JANATAINS", "MERCINS",
    "YPL", "DELTASPINN", "KAY&QUE", "ZAHEENSPIN", "EBLNRBMF",
    "PHPMF1", "CENTRALPHL", "POPULAR1MF", "PURABIGEN", "STYLECRAFT",
    "NFML", "DACCADYE", "PRIMETEX", "PHENIXINS", "AGNISYSL",
    "TOSRIFA", "CRYSTALINS", "PRIMELIFE", "ISLAMIINS", "TRUSTB1MF",
    "RANFOUNDRY", "ETL", "RSRMSTEEL", "NITOLINS", "BEACHHATCH",
    "FAMILYTEX", "PEOPLESINS", "UNIONINS", "NORTHRNINS", "1JANATAMF",
    "MEGHNAINS", "PADMALIFE", "CITYGENINS", "APEXFOODS", "REPUBLIC",
    "ARAMIT", "NAVANACNG", "FEDERALINS", "EIL", "ASIAPACINS",
    "OAL", "MEGHNACEM", "PARAMOUNT", "MIDASFIN", "RENWICKJA",
    "APEXTANRY", "IBP", "CENTRALINS", "SONARBAINS", "LRGLOBMF1",
    "DHAKAINS", "EASTRNLUB", "GBBPOWER", "TAKAFULINS", "HFL",
    "RAHIMTEXT", "UNITEDINS", "SKTRIMS", "BDCOM", "RUPALIINS",
    "PDL", "SUNLIFEINS", "STANDARINS", "EASTLAND", "BDTHAI",
    "EMERALDOIL", "AMCL(PRAN)", "SKICL", "SAIHAMTEX", "EASTERNINS",
    "PAPERPROC", "DOMINAGE", "MONNOAGML", "CLICL",
})

# The December 2022 order covered 168 securities: the 169 above, minus
# ASIAINS and FARCHEM, plus NLI1STMF (probably a mutual fund delisted before
# the March 2023 list was drawn up -- verify against the primary order).
COMPANIES_168_DEC2022: FrozenSet[str] = (
    (COMPANIES_169 - {"ASIAINS", "FARCHEM"}) | {"NLI1STMF"}
)

# 35 securities kept on the floor from 18 Jan 2024.
COMPANIES_35: FrozenSet[str] = frozenset({
    "ANWARGALV", "BARKAPOWER", "BATBC", "BEXIMCO", "BSCCL",
    "BSRMLTD", "BSRMSTEEL", "CONFIDCEM", "DBH", "DOREENPWR",
    "ENVOYTEX", "GP", "HRTEX", "IDLC", "INDEXAGRO",
    "ISLAMIBANK", "KDSALTD", "KPCL", "KTL", "MALEKSPIN",
    "MPETROLEUM", "NHFIL", "NPOLYMER", "ORIONPHARM", "PADMAOIL",
    "RENATA", "ROBI", "SAIHAMCOT", "SHASHADNIM", "SONALIPAPR",
    "SONARBAINS", "SPCERAMICS", "SPCL", "SUMITPOWER", "UPGDCL",
})

# 12 securities after 23 Jan 2024, then freed one by one.
COMPANIES_12: FrozenSet[str] = frozenset({
    "ANWARGALV", "BATBC", "BEXIMCO", "BSRMLTD", "GP", "ISLAMIBANK",
    "KPCL", "MPETROLEUM", "ORIONPHARM", "RENATA", "ROBI", "SPCL",
})
COMPANIES_9: FrozenSet[str] = COMPANIES_12 - {"ANWARGALV", "ORIONPHARM", "RENATA"}  # eff. 7 Feb 2024
COMPANIES_8: FrozenSet[str] = COMPANIES_9 - {"GP"}      # GP freed 3 Mar 2024
COMPANIES_7: FrozenSet[str] = COMPANIES_8 - {"BATBC"}   # BATBC freed 4 Mar 2024
COMPANIES_6: FrozenSet[str] = COMPANIES_7 - {"ROBI"}    # ROBI freed 19 Mar 2024
COMPANIES_2: FrozenSet[str] = frozenset({"BEXIMCO", "ISLAMIBANK"})  # after 28 Aug 2024


FLOOR_PERIODS: Tuple[FloorPeriod, ...] = (
    # Phase 1 - COVID-19. Imposed 19 Mar 2020 (markets shut 26 Mar-30 May 2020).
    ("2020-03-19", "2021-04-07", "ALL", None),
    # 66 exempted: decided 7 Apr, effective 8 Apr 2021.
    ("2021-04-08", "2021-06-05", "EXEMPTED", COMPANIES_66),
    # +30 exempted: announced Thu 3 Jun, effective Sun 6 Jun 2021.
    ("2021-06-06", "2021-06-17", "EXEMPTED", COMPANIES_96),
    # 17 Jun 2021 order removed all floors -> first floor-free session is
    # Sun 20 Jun 2021 (17 Jun itself: order issued that day, intraday timing
    # unverified). Gap: 20 Jun 2021 - 30 Jul 2022, no floor.

    # Phase 2. Order of 28 Jul 2022; floor = average close of 28 Jul and the
    # 4 prior sessions, so the first session trading against it is Sun 31 Jul.
    ("2022-07-31", "2022-12-21", "ALL", None),
    # 168 exempted: order after close Wed 21 Dec -> effective Thu 22 Dec 2022.
    ("2022-12-22", "2023-03-01", "EXEMPTED", COMPANIES_168_DEC2022),
    # 1 Mar 2023: floor re-imposed on the 169 (average close 26 Feb-1 Mar) ->
    # effective 2 Mar. All other securities never lost their July-2022 floor,
    # so every security is floored again.
    ("2023-03-02", "2024-01-18", "ALL", None),
    # Order evening of Thu 18 Jan 2024 -> first session Sun 21 Jan 2024.
    ("2024-01-21", "2024-01-22", "WITH_FLOOR", COMPANIES_35),
    ("2024-01-23", "2024-02-06", "WITH_FLOOR", COMPANIES_12),
    ("2024-02-07", "2024-03-02", "WITH_FLOOR", COMPANIES_9),
    ("2024-03-03", "2024-03-03", "WITH_FLOOR", COMPANIES_8),
    ("2024-03-04", "2024-03-18", "WITH_FLOOR", COMPANIES_7),
    # The 8 Aug 2024 order for the last 6 was cancelled on 11 Aug: never took
    # effect. 28 Aug 2024 urgent meeting (after close) -> 4 freed from 29 Aug.
    ("2024-03-19", "2024-08-28", "WITH_FLOOR", COMPANIES_6),
    # Beximco floor adjusted 115.60 -> 110.10 on 27 Nov 2024 (stock dividend).
    ("2024-08-29", "2026-06-08", "WITH_FLOOR", COMPANIES_2),
    # 9 Jun 2026 onward: no floor.
)

__all__ = [
    "FLOOR_PERIODS",
    "FloorPeriod",
    "COMPANIES_66", "COMPANIES_30", "COMPANIES_96", "COMPANIES_169",
    "COMPANIES_168_DEC2022", "COMPANIES_35", "COMPANIES_12", "COMPANIES_9",
    "COMPANIES_8", "COMPANIES_7", "COMPANIES_6", "COMPANIES_2",
]
