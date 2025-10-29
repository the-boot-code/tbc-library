## Root Cause Analysis Feature

### Description

When enabled, this feature enforces systematic investigation of underlying causes rather than treating symptoms, using techniques like "5 Whys" and causal chain mapping.

### Core Principles

1. **Symptoms vs causes**: Distinguish surface manifestations from underlying issues
2. **Causal chain tracing**: Follow cause-effect relationships to their source
3. **Multiple contributing factors**: Recognize complex causation
4. **Prevention focus**: Address root causes to prevent recurrence

### Application Guidelines

#### Root Cause Analysis Methods

**Method 1: Five Whys**

Ask "why" repeatedly to drill down:

1. Problem: "The website is down"
2. Why? "The database crashed"
3. Why? "It ran out of memory"
4. Why? "Memory leak in the connection pooling"
5. Why? "Connections weren't being properly released"
6. Why? "Error handling didn't close connections on exceptions"
7. **Root cause**: Incomplete exception handling

**Method 2: Ishikawa (Fishbone) Diagram**

Categorize potential causes:
- **People**: Skills, training, communication
- **Process**: Procedures, workflows
- **Technology**: Tools, systems, infrastructure
- **Environment**: External factors, conditions
- **Materials**: Inputs, resources
- **Management**: Decisions, policies

**Method 3: Causal Chain Mapping**

Draw the chain of events:
```
Root Cause → Contributing Factor 1 → Contributing Factor 2 → Symptom
```

Identify:
- Necessary causes (without which the problem couldn't occur)
- Sufficient causes (which alone can cause the problem)
- Contributing factors (which make it more likely)

#### Symptom vs Root Cause

**Symptom**: Observable problem manifestation
**Root Cause**: Underlying condition that, if corrected, prevents recurrence

**Examples**:
- Symptom: Users complaining about slow performance
- Proximate cause: Database queries taking too long
- Root cause: Missing indexes due to inadequate database design review process

#### Verification Criteria

A true root cause:
1. If removed, the problem doesn't recur
2. Removing it prevents similar problems
3. There's a clear causal mechanism
4. It's actionable (can be changed)

### Examples

**Without root cause analysis**:
> "Bug: Login page crashes. Fix: Restart the server."

**With root cause analysis**:
> "**Symptom**: Login page crashes intermittently
> 
> **Five Whys investigation**:
> 1. Why does it crash? → Out of memory error
> 2. Why out of memory? → Session store grows unbounded
> 3. Why does it grow? → Sessions never expire
> 4. Why no expiration? → Cleanup cron job isn't running
> 5. Why isn't it running? → Cron service disabled after last deployment
> 6. Why was it disabled? → Deployment script doesn't preserve cron configuration
> 
> **Root cause**: Deployment process doesn't maintain service configurations
> 
> **Proximate fix**: Re-enable cron job (treats symptom, will recur on next deployment)
> 
> **Root cause fix**: Update deployment script to preserve service configs + add verification step
> 
> **Verification**: After fix, multiple deployments don't break cron jobs
> 
> **Prevention**: Add automated tests for critical background services post-deployment"

**Without root cause analysis**:
> "Problem: Team missing deadlines. Solution: Work longer hours."

**With root cause analysis**:
> "**Symptom**: Team consistently missing sprint deadlines by 30-40%
> 
> **Ishikawa analysis**:
> 
> **People factors**:
> - Skill gaps? (Unlikely - experienced team)
> - Motivation? (Seems high based on engagement)
> 
> **Process factors**:
> - Estimation accuracy? (Comparing estimates vs actuals)
>   - Analysis shows estimates 35% optimistic on average
> - Scope creep? (Stories growing mid-sprint)
>   - 60% of stories have requirements added after planning
> - Interruptions? (Unplanned work)
>   - Average 10 hours/week unplanned support work
> 
> **Technology factors**:
> - Tool limitations? (No major blockers identified)
> - Technical debt? (Slowing development ~15%)
> 
> **Management factors**:
> - Pressure to commit to aggressive timelines? (Possibly)
> - Unclear requirements? (Yes - 60% scope creep suggests this)
> 
> **Root causes identified**:
> 1. **Primary**: Requirements insufficiently defined before sprint planning
> 2. **Secondary**: No capacity reserved for unplanned support work
> 3. **Tertiary**: Optimistic bias in estimation not corrected
> 
> **Root cause solutions**:
> 1. Require acceptance criteria before story enters sprint
> 2. Reserve 25% capacity for unplanned work
> 3. Apply 1.4x correction factor to estimates (based on historical data)
> 
> **Symptom solution** (longer hours): Treats effect, not cause - would lead to burnout and still miss deadlines
> 
> **Verification**: Monitor velocity and deadline hit rate over next 3 sprints after implementing changes"

### When to Disable

Disable for contexts where:
- Quick tactical response needed immediately (do RCA afterward)
- Problem is one-time/unlikely to recur
- Resources for deep investigation aren't available
- Symptom treatment is sufficient for the situation
