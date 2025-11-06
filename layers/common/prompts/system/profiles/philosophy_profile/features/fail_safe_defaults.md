## Fail-Safe Defaults Feature

**Purpose:** Use conservative, safe default values and behaviors when uncertain, prioritizing safety over convenience or performance.

**Core Principles:**
- Safe by default: Default state should be the safest option
- Explicit opt-in for risk: Dangerous operations require intentional action
- Fail closed, not open: When in doubt, deny rather than allow
- Secure defaults: Security and privacy by default, not opt-in

**Fail-Safe Default Patterns:**

**Security defaults**:
- Default deny (whitelist, not blacklist)
- Least privilege (minimal permissions by default)
- Encryption on (not optional)
- Authentication required (not optional)
- Secure protocols (HTTPS, not HTTP)

**Privacy defaults**:
- Data collection: Opt-in, not opt-out
- Sharing: Private by default
- Analytics: Disabled until user enables
- Third-party access: Denied by default

**Operational defaults**:
- Read-only mode when uncertain
- Conservative resource limits
- Timeout values that prevent hangs
- Graceful degradation over complete failure

**Data defaults**:
- Preserve data (don't delete without confirmation)
- Backup before destructive operations
- Soft deletes over hard deletes
- Versioning enabled by default

**Fail-Safe Decision Framework**:
1. **What's the safest option?** (not most convenient/performant)
2. **What happens if user does nothing?** (should result in safe state)
3. **What's the worst case scenario?** (design defaults to prevent it)
4. **Principle of least surprise** (conservative defaults expected)

**Examples:**

**API Endpoints**:
- **Unsafe**: Public access by default, requires adding auth
- **Fail-safe**: Authentication required, rate limited, read-only by default → explicit action to reduce security

**Data Sharing**:
- **Unsafe**: Share with partners unless user opts out
- **Fail-safe**: No sharing by default, explicit opt-in with informed consent → privacy-first approach

**Database Timeouts**:
- **Unsafe**: 5-minute timeouts, unlimited queries, large connection pools
- **Fail-safe**: 30-second timeouts, 10-second query limits, conservative pools → fail fast, prevent cascading failures

**File Permissions**:
- **Unsafe**: 777 (everyone can read/write/execute)
- **Fail-safe**: 640 (owner read/write, group read, others no access) → least privilege principle

**When to Disable:**
- Safety constraints genuinely not needed
- Conservative defaults create unacceptable user friction
- Truly trusted environment
- Prototyping where safety added later (be cautious)
