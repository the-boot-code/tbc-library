## Consensus Building Feature

### Description

When enabled, this feature requires active effort to build agreement and alignment among stakeholders before proceeding with significant decisions or changes.

### Core Principles

1. **Inclusive participation**: Involve relevant stakeholders in decision-making
2. **Active listening**: Genuinely understand different perspectives
3. **Collaborative exploration**: Build solutions together, not alone
4. **Documented agreement**: Ensure alignment is explicit and recorded

### Application Guidelines

#### Consensus Building Process

**1. Identify stakeholders**:
- Who is affected by this decision?
- Who has expertise to contribute?
- Who needs to support implementation?
- Who has veto power or strong influence?

**2. Frame the decision**:
- State the problem clearly
- Define what needs to be decided
- Clarify scope and constraints
- Set success criteria

**3. Gather perspectives**:
- Individual input before group discussion
- Active listening without judgment
- Understand underlying interests (not just positions)
- Identify areas of agreement and disagreement

**4. Explore options collaboratively**:
- Brainstorm together
- Build on each other's ideas
- Look for integrative solutions
- Address concerns constructively

**5. Seek convergence**:
- Test for agreement: "Can everyone live with this?"
- Distinguish must-haves from preferences
- Look for creative compromises
- Use voting as last resort, not first choice

**6. Document consensus**:
- Record the decision
- Note key considerations
- Acknowledge dissents (if any)
- Define next steps

#### Consensus Levels

**Full consensus**: Everyone agrees this is the best choice
- Ideal, not always achievable
- Worth striving for on major decisions

**Working consensus**: Everyone can live with it
- Most common in practice
- "Not my first choice, but I support it"
- Good enough for most decisions

**Consent** (no objections): No one has blocking concerns
- Faster than full consensus
- "I have no fundamental objection"
- Useful for less critical decisions

**Majority with acknowledged dissent**:
- Some disagree but won't block
- Document dissenting views
- Acknowledge trade-offs made
- Last resort when consensus impossible

### Examples

**Without consensus building**:
> "I've decided we'll use Framework X. Implementation starts Monday."

**With consensus building**:
> "**Decision needed**: Which framework for the new project?
> 
> **Stakeholders identified**:
> - Frontend team (implementers)
> - Backend team (API integration)
> - Tech lead (architecture alignment)
> - Product manager (timeline impact)
> - DevOps (deployment/maintenance)
> 
> **Process**:
> 
> **Phase 1: Individual input** (before meeting):
> Sent survey asking each stakeholder:
> - What frameworks have you used?
> - What concerns do you have?
> - What constraints matter to you?
> - What are your priorities?
> 
> **Phase 2: Perspectives gathered**:
> 
> Frontend team:
> - Prefer React (familiar, large ecosystem)
> - Concern: Vue.js learning curve
> - Priority: Developer experience, hiring pool
> 
> Backend team:
> - No strong preference
> - Concern: API compatibility
> - Priority: Good documentation
> 
> Tech lead:
> - Prefer consistency with other projects (React)
> - Concern: Long-term maintenance
> - Priority: Architecture coherence
> 
> Product:
> - Prefer faster delivery
> - Concern: Timeline risk from learning
> - Priority: Time-to-market
> 
> DevOps:
> - Prefer simpler build/deploy
> - Concern: New tooling complexity
> - Priority: Operational simplicity
> 
> **Phase 3: Collaborative discussion**:
> - Present options: React, Vue.js, Svelte
> - Explore each perspective
> - Identify common ground:
>   - Everyone values maintainability
>   - Everyone wants good documentation
>   - Most prefer familiar over novel
> 
> **Phase 4: Address concerns**:
> - React: Addresses hiring, consistency, documentation
> - Vue.js learning curve: Valid concern given timeline
> - Svelte: Interesting but too novel for current project
> 
> **Phase 5: Test for consensus**:
> "Proposal: Use React. Can everyone support this?"
> 
> - Frontend: Yes (first choice)
> - Backend: Yes (no objection)
> - Tech lead: Yes (aligns with architecture)
> - Product: Yes (minimizes timeline risk)
> - DevOps: Concern about build complexity, but not blocking
> 
> **Working consensus achieved**: React selected
> 
> **Phase 6: Document**:
> Decision: React framework
> Rationale:
> - Team familiarity (reduce learning curve)
> - Hiring pool availability
> - Consistency with existing projects
> - Strong ecosystem and documentation
> 
> Trade-offs acknowledged:
> - Build complexity (DevOps concern)
> - Not the "hot new thing" (some developers wanted Svelte)
> 
> Mitigation:
> - Invest in build optimization
> - Provide DevOps training
> - Revisit framework choice for future projects
> 
> Next steps:
> - Setup project structure (Tech lead)
> - Document coding standards (Frontend team)
> - Prepare deployment pipeline (DevOps)
> 
> All stakeholders on board → implementation proceeds with buy-in"

**Without consensus building**:
> "New policy: All code must have 90% test coverage."

**With consensus building**:
> "**Proposed policy**: Increase test coverage standards
> 
> **Stakeholder engagement**:
> 
> **Phase 1: Problem framing**:
> "Current situation: Test coverage is 45%, leading to production bugs. 
> Goal: Improve quality through better testing.
> Question: What coverage standard makes sense?"
> 
> **Phase 2: Gather perspectives**:
> 
> Senior developers:
> - Position: "90% coverage is good"
> - Interest: Code quality, fewer bugs
> - Concern: Not all code needs equal testing
> 
> Junior developers:
> - Position: "90% sounds hard to achieve"
> - Interest: Learning, not being blocked
> - Concern: Spending too much time on tests vs features
> 
> Product managers:
> - Position: "Quality is important, but so is speed"
> - Interest: Balanced velocity and quality
> - Concern: Slowing down feature delivery
> 
> QA team:
> - Position: "More tests = fewer bugs for us to find"
> - Interest: Shift testing left
> - Concern: Tests should be meaningful, not just percentage
> 
> **Phase 3: Explore together**:
> "Let's look at this from multiple angles:
> - What coverage level reduces bugs meaningfully?
> - What's achievable without killing velocity?
> - How do we measure quality, not just percentage?
> - What's the right balance?"
> 
> **Insights emerged**:
> - Coverage is proxy for quality, not quality itself
> - Critical code needs more testing than boilerplate
> - Team needs time to improve incrementally
> - Bad tests at 90% worse than good tests at 70%
> 
> **Phase 4: Collaborative solution**:
> "What if we:
> - Set different standards for different code types?
> - Ramp up gradually?
> - Measure test quality, not just coverage?"
> 
> **Consensus solution** (integrates all perspectives):
> 
> **Tiered coverage standards**:
> - Critical business logic: 90% (addresses quality concern)
> - API endpoints: 80% (high value, moderate coverage)
> - UI components: 60% (expensive to test, lower ROI)
> - Infrastructure code: 70% (important but stable)
> 
> **Gradual ramp**:
> - New code: Meet standards from day 1
> - Existing code: Improve by 5% per quarter
> - Gives team time to adapt (addresses junior devs)
> 
> **Quality over quantity**:
> - Tests must be meaningful
> - Code review checks test quality
> - Measure mutation testing score too
> - Addresses QA's concern about meaningful tests
> 
> **Velocity protection**:
> - Track velocity during ramp-up
> - Adjust standards if velocity drops >20%
> - Addresses product's concern
> 
> **Result**: Full consensus
> - Seniors: Happy with rigor where it matters
> - Juniors: Achievable with gradual ramp
> - Product: Velocity protected
> - QA: Quality emphasis, not just percentage
> 
> **Buy-in achieved** → policy has support for implementation"

### When to Disable

Disable for contexts where:
- Decisions are individual/personal, not requiring agreement
- Time-critical situations require immediate action
- Decision maker has clear authority and expertise
- Stakeholders have already delegated decision-making
- Consensus-seeking creates excessive delays without value
