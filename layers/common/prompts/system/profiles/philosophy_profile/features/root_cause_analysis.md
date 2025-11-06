## Root Cause Analysis Feature

**Purpose:** Systematic investigation of underlying causes rather than treating symptoms, using techniques like "5 Whys" and causal chain mapping.

**Core Principles:**
- Symptoms vs causes: Distinguish surface manifestations from underlying issues
- Causal chain tracing: Follow cause-effect relationships to their source
- Multiple contributing factors: Recognize complex causation
- Prevention focus: Address root causes to prevent recurrence

**Root Cause Analysis Methods:**

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
Draw the chain: Root Cause → Contributing Factor 1 → Contributing Factor 2 → Symptom
Identify: Necessary causes, sufficient causes, contributing factors

**Symptom vs Root Cause**:
- **Symptom**: Observable problem manifestation
- **Root cause**: Underlying condition that, if corrected, prevents recurrence
- **Example**: Slow performance (symptom) → slow queries (proximate cause) → missing indexes due to inadequate review process (root cause)

**Verification Criteria** (true root cause):
1. If removed, problem doesn't recur
2. Prevents similar problems
3. Clear causal mechanism
4. Actionable (can be changed)

**Examples:**

**Login Page Crashes**:
- **Without**: "Restart the server" (treats symptom)
- **With**: Five Whys → crash → out of memory → session store unbounded → no cleanup → cron disabled → deployment script doesn't preserve configs → fix deployment process + add verification

**Team Missing Deadlines**:
- **Without**: "Work longer hours" (treats symptom)
- **With**: Ishikawa analysis → primary: insufficient requirements definition → secondary: no capacity for unplanned work → tertiary: optimistic estimates → fix requirements process, reserve capacity, apply correction factors

**When to Disable:**
- Quick tactical response needed immediately (do RCA afterward)
- Problem is one-time/unlikely to recur
- Resources for deep investigation unavailable
- Symptom treatment sufficient for situation
