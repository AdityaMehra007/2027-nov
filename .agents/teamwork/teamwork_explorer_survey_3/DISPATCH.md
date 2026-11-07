# Dispatch Task — Platform CLI & Test Explorer

## Working Directory
`e:\2027 nov\.agents\teamwork\teamwork_explorer_survey_3\`

## Original Request Record
`e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`

## Objectives
1. Read `e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md`.
2. Inspect the codebase for platform CLI command implementations (`world-clients`, `audit-client`, `build-for-client`, `run-world-swarm`, `world-stats`). Document their syntax, parameters, entrypoints, and runtime behaviors.
3. Inspect the automated test suite(s): framework (jest, pytest, mocha, etc.), test locations, how to execute them, coverage, and any current failures or configuration nuances.
4. Inspect the database engine, migrations/schema, configuration files (.env, configs), and external network access requirements/endpoints.
5. Author a detailed `survey_report.md` and complete a structured `handoff.md` in your working directory.


## 2026-11-07T08:40:56Z
[Message] sender=975620c1-1b3c-413b-8522-63ef75a9fd83 priority=MESSAGE_PRIORITY_HIGH
You are dispatched as a teamwork_explorer to survey the CASHFLOW INFINITY: OMNIVERSE platform codebase.

Working Directory: e:\2027 nov\.agents\teamwork\teamwork_explorer_survey_3\
Original Request Authority: e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md
Your Dispatch Task: e:\2027 nov\.agents\teamwork\teamwork_explorer_survey_3\DISPATCH.md

CRITICAL INSTRUCTIONS:
1. You MUST read e:\2027 nov\.agents\teamwork\ORIGINAL_REQUEST.md first.
2. Read your DISPATCH.md file.
3. Investigate the codebase and configuration:
   - Identify how platform CLI commands are defined, registered, and executed:
     `world-clients`, `audit-client`, `build-for-client`, `run-world-swarm`, `world-stats`.
     Document their exact command syntax, executable entrypoints (e.g. npm run ..., python -m ..., or bin script), accepted flags/parameters, and sample outputs.
   - Investigate the automated test suite(s): test framework, directory location of tests, command lines used to run unit and integration tests, and current test suite status.
   - Investigate database setup, migrations, connection configurations (SQLite, PostgreSQL, etc.), seed scripts, and state files.
   - Investigate external network access needs and operational telemetry sinks.
4. Create your BRIEFING.md and progress.md in your working directory.
5. Write a comprehensive survey_report.md in your working directory with all command strings, configuration details, test definitions, and code references.
6. Write handoff.md in your working directory and notify the parent orchestrator via send_message when finished.
