---
name: xquik-source-research-expert
description: Design and review source-grounded X research with Xquik REST, MCP, the x-developer SDK, evidence logs, and reproducible sampling.
---

# Xquik source research expert

## Overview

Use this skill when a task needs repeatable X research with traceable source data,
structured collection notes, and clear limits. It helps agents plan searches,
collect evidence, normalize records, and report findings without treating a
single feed snapshot as a complete truth set.

## When to use

- Build a source-review packet for an X account, keyword, competitor, launch, or incident.
- Compare claims against public posts, profiles, replies, follower evidence, or search results.
- Design a small X data collection workflow before writing code or running an API client.
- Add provenance fields to a report, CSV export, dashboard note, or issue summary.
- Translate an analyst question into Xquik REST calls, MCP calls, or pinned `x-developer` SDK usage.

## Inputs to request

- Research question and decision the evidence should support.
- Accounts, keywords, post URLs, or user IDs to inspect.
- Time window, sample size, locale, and any exclusion rules.
- Output format: notes, CSV, JSON, issue comment, table, or code example.
- Credential boundary: confirm whether an API key is already available in the environment.

## Workflow

1. Select the research route.
   - Read [references/task_selection.md](references/task_selection.md) to match
     the question to the smallest useful collection method.
   - Use [references/topic_index.md](references/topic_index.md) to choose the
     evidence artifact and validation oracle.

2. Verify source truth.
   - Read the current [Xquik API overview](https://docs.xquik.com/api-reference/overview)
     before naming endpoints.
   - Use the [X API comparison](https://docs.xquik.com/alternatives/x-api) only for
     public positioning context, not for endpoint contracts.
   - Before writing an SDK example, resolve the current stable version with
     `npm view x-developer version`, pin that exact version, and record it in the evidence log.
   - Do not infer nonpublic implementation details or plan limits from examples.

3. Define the collection plan.
   - Convert the question into exact accounts, keywords, URLs, or IDs.
   - Set a time window and sample cap before collecting data.
   - Decide which fields are required for the decision, then ignore unrelated fields.
   - Record the query, source URL or post ID, collection time, and tool used.

4. Collect evidence.
   - Prefer Xquik REST, MCP, or the pinned SDK when the task needs live X data.
   - Keep credentials in the runtime environment. Never print tokens, cookies, auth headers,
     or screenshots that contain secrets.
   - Retry transient failures only enough to confirm whether the route is unavailable.
   - Stop and report a blocker if the task needs private account access, missing credentials,
     deleted content, or a legal review.

5. Normalize records.
   - Store stable identifiers separately from display names.
   - Keep `collected_at`, `query`, `source_url`, and `sample_limit` with every result set.
   - Preserve raw post IDs or profile URLs so reviewers can recheck the evidence.
   - Mark derived fields, such as topic labels or sentiment, as analysis rather than source data.

6. Report with limits.
   - Lead with the decision-relevant findings.
   - Include the sample size, window, and collection time.
   - Separate observed facts from interpretation.
   - Add a caveat when rate limits, deleted posts, protected accounts, or small
     samples affect coverage.

7. Validate the evidence packet.
   - Follow [references/project_workflow.md](references/project_workflow.md) for
     existing and greenfield research projects.
   - Run the checks in
     [references/testing_and_oracles.md](references/testing_and_oracles.md).

## Quality bar

- Every factual claim traces to a query, source URL, post ID, or exported row.
- Every report states the time window and collection time.
- Code examples pin the verified SDK version or link to current public docs.
- Public output avoids credentials, private implementation details, unsupported coverage claims,
  and broad statements such as "all posts" unless the collection actually proved that scope.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.

## When not to use

- Full social listening strategy without a specific X evidence task.
- Private or credentialed account access that has not been authorized.
- Legal, safety, or policy decisions that require professional review.
- Generic marketing copy where no source collection or provenance is needed.
