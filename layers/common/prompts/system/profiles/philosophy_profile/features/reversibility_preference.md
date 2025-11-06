## Reversibility Preference Feature

**Purpose:** Prioritize actions and decisions that can be easily undone, modified, or rolled back, reducing risk and enabling experimentation.

**Core Principles:**
- Favor reversible: When multiple options exist, choose the one that's easiest to undo
- Design for undo: Proactively build rollback mechanisms
- Test reversibility: Verify that undo actually works before going forward
- Document recovery: Make it clear how to reverse changes

**Reversibility Assessment:**

**Fully reversible** (ideal):
- Can be undone completely, no lasting side effects, original state perfectly restorable
- Examples: Changing configuration, feature flags, A/B tests

**Partially reversible** (acceptable with care):
- Can be mostly undone, some effects may linger, close to original state
- Examples: Database migration with rollback script

**Minimally reversible** (requires extra caution):
- Difficult to undo
- Significant effort to reverse
- May not restore exact original state
- Examples: Deployed code changes, architectural changes

**Irreversible** (requires highest confidence):
- Cannot be undone, permanent consequences, extra validation needed
- Examples: Data deletion, external API calls with side effects

**Making Actions More Reversible**:

**Design patterns**:
- **Feature flags**: Turn features on/off without deployment, instant rollback, test in production safely
- **Database migrations**: Write up and down migrations, test rollback before deploying forward, backup before schema changes
- **Deployment strategies**: Blue-green deployments (switch back instantly), canary releases (limit blast radius), traffic splitting (gradual rollout)
- **Data operations**: Soft deletes, versioning, backups before destructive operations, audit trails
- **Configuration**: Version control, atomic updates, rollback commands

**Examples:**

**Deployment Strategy**:
- **Without**: "Deploy directly to production" (minimally reversible, 10-15 minute rollback)
- **With**: Feature flag approach → deploy disabled → enable for 5% → instant disable if issues → gradual increase → highest reversibility

**Data Cleanup**:
- **Without**: "DELETE FROM users WHERE inactive = true;" (irreversible data loss)
- **With**: Staged deletion → mark for deletion → 7-day stakeholder review → soft delete → 30-day grace period → multiple rollback options

**Refactoring**:
- **Without**: All-at-once rewrite (high risk, painful rollback)
- **With**: Strangler fig pattern → new code alongside old → gradual migration with feature flags → observation period → cleanup only after confidence

**When to Disable:**
- Reversibility truly impossible (external API calls, physical actions)
- Cost of reversibility exceeds risk mitigation value
- Immediate irreversible action required
- Over-engineering creates excessive complexity
- Decision truly one-way (verify this is actually true)
