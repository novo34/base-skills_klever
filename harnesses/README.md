# JEV harness capability contracts

These profiles are conservative Foundation contracts, not claims that every installation exposes every feature.

JEV core owns policy, authorization, risk, audit, verification and human-approval gates. A harness is a replaceable execution surface. Platform adapters must intersect these declared capabilities with capabilities actually available at runtime and must return a typed unsupported/blocking result when a required capability is absent.

No harness prompt may weaken or replace JEV core safety controls.
