---
name: architecture
description: Split architecture into business, enterprise, and solution layers, then record the expensive choice.
---

# Architecture

Three people, three questions. Do not merge them into one diagram unless the person asked for an overview sheet, and even then label the layers.

## Business

Which capabilities exist, which value stream they serve, and what is outside the system.
No classes. No libraries. Output is a short capability list and the non-goals.

## Enterprise

Which system owns which data and decision, which choice must still be true in years, and where the team boundary is.
No sprint-level class design.

## Solution

The contract other teams build against this sprint: interfaces, data, failures, and what slice counts as done.
Detailed enough to open a story. Not a substitute for the developer.

## Then

An expensive choice becomes an ADR.
Behavior goes to Sysl. Structure goes to CALM.
The chair in agents/architect.md decides which layer speaks. Mixing layers without that call breaks BOUND-2.

Rules: ARCH-1 … ARCH-5.

## Rules
Operate under wiki/Rules.md. If this skill conflicts with a rule id, the rule wins and this skill is wrong.
