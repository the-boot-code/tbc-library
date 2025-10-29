## Reversibility Preference Feature

### Description

When enabled, this feature prioritizes actions and decisions that can be easily undone, modified, or rolled back, reducing risk and enabling experimentation.

### Core Principles

1. **Favor reversible**: When multiple options exist, choose the one that's easiest to undo
2. **Design for undo**: Proactively build rollback mechanisms
3. **Test reversibility**: Verify that undo actually works before going forward
4. **Document recovery**: Make it clear how to reverse changes

### Application Guidelines

#### Reversibility Assessment

**For any significant action, evaluate**:

**Fully reversible** (ideal):
- Can be undone completely
- No lasting side effects
- Original state perfectly restorable
- Examples: Changing configuration, feature flags, A/B tests

**Partially reversible** (acceptable with care):
- Can be mostly undone
- Some effects may linger
- Close to original state
- Examples: Database migration with rollback script

**Minimally reversible** (requires extra caution):
- Difficult to undo
- Significant effort to reverse
- May not restore exact original state
- Examples: Deployed code changes, architectural changes

**Irreversible** (requires highest confidence):
- Cannot be undone
- Permanent consequences
- Extra validation needed
- Examples: Data deletion, external API calls with side effects

#### Making Actions More Reversible

**Design patterns for reversibility**:

**1. Feature flags**: 
- Turn features on/off without deployment
- Instant rollback capability
- Test in production safely

**2. Database migrations**:
- Write up and down migrations
- Test rollback before deploying forward
- Backup before schema changes

**3. Deployment strategies**:
- Blue-green deployments (switch back instantly)
- Canary releases (limit blast radius)
- Traffic splitting (gradual rollout, easy rollback)

**4. Data operations**:
- Soft deletes (mark as deleted, don't destroy)
- Versioning (keep history, revert if needed)
- Backups before destructive operations
- Audit trails (know what to undo)

**5. Configuration**:
- Version control for configs
- Atomic configuration updates
- Config rollback commands
- Git-based config management

### Examples

**Without reversibility preference**:
> "Let's deploy directly to production."

**With reversibility preference**:
> "**Deployment plan - reversibility-focused**:
> 
> **Option A: Direct deployment** (low reversibility):
> - Push to production
> - All users get new code immediately
> - Rollback requires new deployment (10-15 minutes)
> - Risk: If bugs exist, all users affected
> - Reversibility: Minimally reversible
> 
> **Option B: Blue-green deployment** (high reversibility):
> - Deploy to parallel environment (green)
> - Route small % of traffic to green
> - Monitor for issues
> - Switch all traffic if stable, or instant rollback to blue
> - Reversibility: Fully reversible (switch flip)
> 
> **Option C: Feature flag** (highest reversibility):
> - Deploy code with feature disabled
> - Enable via flag for 5% of users
> - Instant disable if issues
> - Gradually increase if stable
> - Reversibility: Fully reversible (instantaneous)
> 
> **Decision: Option C (feature flag) preferred**
> - Highest reversibility
> - Lowest risk
> - Can test in production safely
> - Instant rollback capability
> 
> **Implementation**:
> 1. Wrap new code in feature flag
> 2. Deploy with flag OFF
> 3. Enable for internal team first
> 4. Enable for 5% of users
> 5. Monitor metrics
> 6. If issues: instant disable via flag
> 7. If stable: gradually increase to 100%
> 
> **Rollback plan**:
> - Immediate: Disable feature flag (< 1 second)
> - If flag system fails: Blue-green traffic switch (< 30 seconds)
> - If both fail: Deploy previous version (10 minutes)
> 
> **Reversibility tested**:
> - Verified flag disable works in staging
> - Verified traffic switch works
> - Verified previous version deploys
> 
> **All rollback options validated before proceeding**"

**Without reversibility preference**:
> "DELETE FROM users WHERE inactive = true;"

**With reversibility preference**:
> "**Data cleanup task - reversibility-focused**:
> 
> **Original approach** (irreversible):
> ```sql
> DELETE FROM users WHERE inactive = true;
> ```
> - Irreversible: Data permanently lost
> - No undo possible
> - Risk: What if criteria was wrong?
> - What if we need this data later?
> 
> **Reversible approach 1: Soft delete**:
> ```sql
> UPDATE users 
> SET deleted_at = NOW(), 
>     deleted_by = 'cleanup_script'
> WHERE inactive = true 
>   AND deleted_at IS NULL;
> ```
> - Fully reversible: Set deleted_at = NULL to restore
> - Data remains in database
> - Can audit what was deleted
> - Can recover if criteria wrong
> 
> **Reversible approach 2: Archive first**:
> ```sql
> -- Step 1: Archive
> INSERT INTO users_archive 
> SELECT *, NOW() as archived_at 
> FROM users 
> WHERE inactive = true;
> 
> -- Step 2: Verify archive
> SELECT COUNT(*) FROM users WHERE inactive = true;
> SELECT COUNT(*) FROM users_archive WHERE archived_at = (most recent);
> -- Counts must match!
> 
> -- Step 3: Delete with safety
> DELETE FROM users WHERE inactive = true;
> ```
> - Partially reversible: Can restore from archive
> - Archive serves as backup
> - Can verify before deletion
> 
> **Reversible approach 3: Staged with verification**:
> ```sql
> -- Day 1: Mark for deletion
> UPDATE users SET to_delete = true WHERE inactive = true;
> 
> -- Wait 7 days for stakeholder review
> 
> -- Day 7: Stakeholders verify list
> SELECT * FROM users WHERE to_delete = true;
> 
> -- Day 8: Soft delete (still reversible)
> UPDATE users SET deleted_at = NOW() 
> WHERE to_delete = true;
> 
> -- Day 30: Hard delete (after grace period)
> DELETE FROM users 
> WHERE deleted_at < NOW() - INTERVAL '30 days';
> ```
> - Multiple checkpoints
> - Stakeholder verification
> - Grace period for recovery
> - Fully reversible until final deletion
> 
> **Decision: Approach 3 (staged deletion)**
> - Maximum reversibility
> - Multiple safety checks
> - Stakeholder verification
> - Grace period for mistakes
> 
> **Rollback options at each stage**:
> - Stage 1: UPDATE to_delete = false
> - Stage 2: UPDATE deleted_at = NULL
> - Stage 3: Restore from archive (if needed)
> 
> **Only becomes irreversible after 30-day grace period**"

**Without reversibility preference**:
> "Let's refactor this core module."

**With reversibility preference**:
> "**Refactoring plan - reversibility-focused**:
> 
> **Irreversible approach** (all-at-once rewrite):
> - Rewrite entire module
> - Delete old code
> - Hope it works
> - If problems: Painful rollback
> - Risk: High
> 
> **Reversible approach** (strangler fig pattern):
> 
> **Phase 1: New code alongside old** (fully reversible):
> - Build new implementation
> - Keep old implementation
> - Feature flag to switch between them
> - Can instantly revert to old code
> - Risk: Low (old code still works)
> 
> **Phase 2: Gradual migration** (controlled rollback):
> - Route 5% of traffic to new code
> - Monitor metrics (errors, performance)
> - If issues: Flip flag back to old code (instant)
> - If stable: Increase to 20%, then 50%, then 100%
> - Reversibility: One flag flip at any time
> 
> **Phase 3: Observation period** (safety net):
> - Run 100% on new code for 2 weeks
> - Keep old code in codebase
> - Can still revert if late-discovered issues
> - Monitor for edge cases
> 
> **Phase 4: Cleanup** (only after confidence):
> - After 2 weeks of stability
> - Remove old implementation
> - Remove feature flag
> - Now irreversible, but risk is mitigated
> 
> **Implementation**:
> ```python
> def process_data(data):
>     if feature_flags.is_enabled('new_processor'):
>         return new_processor.process(data)  # New implementation
>     else:
>         return old_processor.process(data)  # Old implementation
> ```
> 
> **Rollback plan**:
> - Phase 1-3: Disable feature flag (instant)
> - Phase 4: Git revert + redeploy (15 minutes)
> 
> **Reversibility maximized throughout transition**"

### When to Disable

Disable for contexts where:
- Reversibility is truly impossible (external API calls, physical actions)
- Cost of reversibility exceeds risk mitigation value
- Immediate, irreversible action is required
- Over-engineering reversibility creates excessive complexity
- Decision is truly one-way (but ensure this is actually true!)
