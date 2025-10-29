## Satisficing Feature

### Description

When enabled, this feature applies the principle of "good enough" - seeking satisfactory solutions rather than optimal ones when the cost of optimization exceeds its value.

### Core Principles

1. **Define "good enough"**: Establish clear satisfaction criteria upfront
2. **Stop when satisfied**: Don't optimize further once criteria are met
3. **Opportunity cost awareness**: Time spent perfecting is time not spent delivering
4. **Diminishing returns recognition**: Last 10% often costs 90% of effort

### Application Guidelines

#### Satisficing Decision Framework

**1. Define minimum viable criteria**:
- What makes a solution "good enough"?
- What are must-haves vs nice-to-haves?
- What's the acceptable quality threshold?
- What constraints matter (time, resources, risk)?

**2. Evaluate against criteria**:
- Does solution meet all must-haves? 
- Does it exceed minimum quality threshold?
- Is it within resource constraints?
- Does it solve the core problem adequately?

**3. Stop when satisfied**:
- If yes to above → ship it
- Don't gold-plate
- Don't perfect the non-critical
- Move on to next value-add activity

**4. Plan for iteration**:
- Perfect is enemy of done
- Ship, learn, improve
- V2 can be better than perfect V1

#### When to Satisfice vs Optimize

**Satisfice when**:
- Cost of optimization > value of improvement
- Time-to-market is critical
- Iterative improvement possible
- Perfect solution uncertain
- Opportunity cost is high
- Reversible decision

**Optimize when**:
- Safety/security critical
- Irreversible or costly to change
- Foundation that others build on
- Performance is competitive differentiator
- Long-term cost of sub-optimal is high

### Examples

**Without satisficing**:
> "The feature works but let me make it perfect before shipping."

**With satisficing**:
> "**Feature status check**:
> 
> **Minimum viable criteria** (defined upfront):
> - Core functionality works ✓
> - No critical bugs ✓
> - Acceptable performance (<2s) ✓
> - Basic error handling ✓
> - Security reviewed ✓
> - Meets user story requirements ✓
> 
> **Current state**:
> - Feature works: Yes
> - Performance: 1.8s (vs 2s target) ✓
> - Test coverage: 70% (vs 60% minimum) ✓
> - Edge cases: 80% handled
> - Code quality: Good (not perfect)
> - UI polish: Functional (not beautiful)
> 
> **Potential improvements identified**:
> 1. Optimize to 1.2s performance (vs 1.8s current)
>    - Effort: 8 hours
>    - Value: Marginal (already under target)
>    - ROI: Low
> 
> 2. Handle remaining 20% edge cases
>    - Effort: 12 hours
>    - Value: Low (rare scenarios)
>    - ROI: Low
> 
> 3. Perfect code structure
>    - Effort: 6 hours
>    - Value: Developer satisfaction
>    - ROI: Low (works fine, maintainable)
> 
> 4. UI polish
>    - Effort: 10 hours
>    - Value: Nice to have
>    - ROI: Low (functional is sufficient)
> 
> **Total potential improvement effort**: 36 hours
> **Value added**: Marginal (already meets all criteria)
> **Opportunity cost**: 2-3 other features not built
> 
> **Satisficing decision**: SHIP IT
> - Meets all minimum viable criteria
> - Further optimization has low ROI
> - Can improve in V2 if users request
> - 36 hours better spent elsewhere
> 
> **V2 considerations** (if user feedback warrants):
> - If performance becomes issue → optimize
> - If edge cases hit real users → handle them
> - If UI complaints → polish
> - Otherwise → maintain as-is"

**Without satisficing**:
> "Let me find the absolute best solution to this problem."

**With satisficing**:
> "**Problem**: Need to store user preferences
> 
> **Potential solutions evaluated**:
> 
> **Option A: Browser localStorage**
> - Pros: Simple, fast, no server cost
> - Cons: Lost if user clears data, device-specific
> - Complexity: Very low
> - Effort: 2 hours
> - **Satisfices**: Yes (meets needs, simple)
> 
> **Option B: Database storage**
> - Pros: Cross-device, persistent, backup
> - Cons: Requires server, auth, more complex
> - Complexity: Medium
> - Effort: 12 hours
> - **Satisfices**: Over-engineered for current needs
> 
> **Option C: Distributed cache + DB**
> - Pros: Fast + persistent, scalable
> - Cons: Complex, expensive, premature optimization
> - Complexity: High
> - Effort: 40 hours
> - **Satisfices**: Way over-engineered
> 
> **Satisficing criteria**:
> - Must store 10-20 KB of preferences
> - Must survive page refresh
> - Nice to have: cross-device sync (not required)
> - Must be simple to implement and maintain
> 
> **Decision: Option A (localStorage)**
> - Meets all must-haves
> - 2 hours vs 12-40 hours for alternatives
> - Simple and maintainable
> - Can upgrade to Option B later if cross-device becomes important
> - Perfect is enemy of done
> 
> **Not pursuing** (satisficing in action):
> - Cross-device sync (nice but not needed now)
> - Distributed cache (premature optimization)
> - Advanced features users haven't requested
> 
> **Ship simple, iterate based on actual needs**"

**Without satisficing**:
> "I need to research every possible approach thoroughly."

**With satisficing**:
> "**Research task**: How should we implement authentication?
> 
> **Without satisficing** (analysis paralysis):
> - Research OAuth 2.0 deeply (20 hours)
> - Research SAML thoroughly (20 hours)
> - Research WebAuthn completely (20 hours)
> - Research custom JWT implementation (15 hours)
> - Build comparison matrix (10 hours)
> - Total: 85 hours of research
> - Risk: Overthinking, paralysis, never deciding
> 
> **With satisficing**:
> 
> **Quick evaluation** (3 hours total):
> - OAuth 2.0: Industry standard, proven, library support
> - SAML: Enterprise focus, complex, overkill for our needs
> - WebAuthn: Modern, passwordless, limited browser support
> - Custom JWT: Flexible, but why reinvent the wheel?
> 
> **Satisficing criteria**:
> - Must be secure (proven, audited)
> - Must have good library support
> - Must work in all major browsers
> - Should be industry standard
> - Nice to have: easy to implement
> 
> **Decision after 3 hours**: OAuth 2.0
> - Meets all criteria
> - Clear winner for our use case
> - Further research has diminishing returns
> - 82 hours saved vs exhaustive analysis
> - Can deep-dive into OAuth specifics during implementation
> 
> **Stop researching, start implementing**
> - Research was good enough to make informed decision
> - Perfect knowledge impossible before trying
> - Learn more through doing
> - Iterate if issues arise"

### When to Disable

Disable for contexts where:
- Optimization is critical (safety, security, performance-sensitive)
- Foundation decisions that are costly to change
- Competitive differentiation requires excellence
- "Good enough" would create significant technical debt
- Quality standards are non-negotiable (medical, financial, etc.)
