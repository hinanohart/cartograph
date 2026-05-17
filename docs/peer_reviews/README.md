# Peer review logs

Each minor release (`v0.X.0`) ships with a peer review log in this directory
recording the external reviewers, their domain, and outstanding construct-
validity concerns. The `verify_release.py` script (gate #6) fails any release
whose log is missing.

## Reviewer slate (target)

- 1 philosopher familiar with *Cartographies* (Pasquinelli / Hui / Sha Xin
  Wei orbit)
- 1 mechanistic interpretability researcher (TransformerLens / Anthropic /
  Neel Nanda orbit)
- 1 applied TDA researcher (giotto-tda / Carriere orbit)
- (optional, for v0.2.0+): 1 political philosophy reviewer from the Italian
  *Operaismo* line (Lazzarato / Berardi / Stalder orbit) for the U-functor
  value-domain selection

Outreach happens within month 1 of Phase 1a per ADR-0001 residual issue #7.
