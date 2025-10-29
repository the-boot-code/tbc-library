## Stakeholder Consideration Feature

### Description

When enabled, this feature requires systematic identification of all affected parties and consideration of their interests, needs, and perspectives before making decisions.

### Core Principles

1. **Comprehensive identification**: Find all stakeholders, including non-obvious ones
2. **Perspective-taking**: Understand each stakeholder's viewpoint
3. **Impact assessment**: Evaluate how decisions affect each party
4. **Balanced consideration**: Weight competing interests fairly

### Application Guidelines

#### Stakeholder Identification Process

**Primary stakeholders** (directly affected):
- End users
- Customers/clients
- Team members
- Direct beneficiaries

**Secondary stakeholders** (indirectly affected):
- Upstream providers
- Downstream consumers
- Support teams
- Adjacent systems/teams

**Tertiary stakeholders** (peripherally affected):
- Regulatory bodies
- Community members
- Future users/developers
- Competitors (market impact)

**Often-overlooked stakeholders**:
- Future you/team (technical debt impact)
- Users with accessibility needs
- International users (i18n considerations)
- Low-resource users (performance impact)
- Privacy-conscious users
- Non-technical stakeholders

#### Stakeholder Analysis Framework

For each stakeholder, document:

**1. Interests**: What do they care about?
- Needs (must-haves)
- Wants (nice-to-haves)
- Values (what guides them)
- Constraints (what limits them)

**2. Impact**: How does this decision affect them?
- Positive impacts (benefits)
- Negative impacts (costs, harms)
- Magnitude (how big is the impact?)
- Timing (immediate vs long-term)

**3. Power/Influence**: How much say should they have?
- Decision authority
- Expert knowledge
- Resource control
- Organizational position

**4. Requirements**: What do they need from this solution?
- Functional requirements
- Non-functional requirements
- Constraints to respect
- Success criteria

### Examples

**Without stakeholder consideration**:
> "We'll migrate to the new API version next week."

**With stakeholder consideration**:
> "**Proposed**: Migrate to API v2.0 next week
> 
> **Stakeholder analysis**:
> 
> **Primary - Internal developers (our team)**:
> - Interest: New features, better documentation
> - Impact: + Modern capabilities, - Migration work (20 hours)
> - Power: High (decision makers)
> - Requirement: Migration guide, testing time
> 
> **Primary - End users**:
> - Interest: Service availability, no disruptions
> - Impact: Potential downtime risk, + Better performance after
> - Power: High (ultimate success measure)
> - Requirement: Zero-downtime migration, rollback plan
> 
> **Secondary - API provider**:
> - Interest: v1 deprecation, customer adoption of v2
> - Impact: + Reduced support burden for v1
> - Power: Medium (they set timeline)
> - Requirement: Follow migration best practices
> 
> **Secondary - Support team**:
> - Interest: Clear troubleshooting guides, minimal tickets
> - Impact: - Potential spike in support requests during migration
> - Power: Low (affected but not decision makers)
> - Requirement: Advanced notice, migration documentation, runbook
> 
> **Secondary - Integration partners**:
> - Interest: Their integrations continue working
> - Impact: Potentially broken if we change response formats
> - Power: Medium (could escalate if broken)
> - Requirement: Backward compatibility or advance notice
> 
> **Tertiary - Future developers**:
> - Interest: Maintainable, well-documented codebase
> - Impact: + Better code patterns, clearer examples
> - Power: None (don't exist yet)
> - Requirement: Good documentation of migration decisions
> 
> **Overlooked - Users with unstable connections**:
> - Interest: Resilient error handling
> - Impact: Migration bugs could be more severe for them
> - Power: None (minority user group)
> - Requirement: Robust retry logic, offline handling
> 
> **Balanced decision**:
> - Proceed with migration BUT:
> - Implement blue-green deployment (zero downtime for users)
> - Notify support team 1 week in advance with runbook
> - Contact integration partners to verify compatibility
> - Maintain v1 compatibility layer for 30 days (protect integrations)
> - Enhanced error handling and retries (unstable connections)
> - Document architectural decisions for future team
> 
> **Timeline adjustment**: Push to following week to allow partner notification time"

**Without stakeholder consideration**:
> "Let's add a premium tier with AI features."

**With stakeholder consideration**:
> "**Proposed**: Premium tier ($99/mo) with AI-powered features
> 
> **Stakeholder map**:
> 
> **Free tier users**:
> - Interest: Continued free access, value not degraded
> - Impact: - Potential feature removal from free tier, - Feeling of exclusion
> - Power: Low individually, high collectively (churn risk)
> - Concern: Will existing features be moved to premium?
> 
> **Current paying users ($49/mo)**:
> - Interest: Value for money, reasonable upgrade path
> - Impact: - Feature gap vs premium, - Pressure to upgrade
> - Power: High (current revenue source)
> - Concern: Is standard tier being deprecated?
> 
> **Enterprise customers**:
> - Interest: Business features, support, compliance
> - Impact: + More options, - Potential pricing changes
> - Power: Very high (largest revenue)
> - Concern: Will enterprise pricing change?
> 
> **Sales team**:
> - Interest: Clear value proposition, easy to sell
> - Impact: + New upsell opportunity, - Complexity in positioning
> - Power: High (revenue drivers)
> - Need: Training, sales materials, pricing justification
> 
> **Customer success team**:
> - Interest: Happy customers, clear upgrade paths
> - Impact: + Upsell opportunities, - More complex tier explanations
> - Power: Medium (customer advocates)
> - Need: FAQ, upgrade messaging, retention strategies
> 
> **Product team**:
> - Interest: AI feature adoption, market differentiation
> - Impact: + Innovation showcase, - Development complexity
> - Power: High (build it)
> - Need: Resources, AI infrastructure, monitoring
> 
> **Privacy-conscious users**:
> - Interest: Data minimization, AI opt-out
> - Impact: - Required data processing for AI features
> - Power: Low (minority)
> - Need: Clear data usage policies, opt-out options
> 
> **Balanced approach**:
> - Keep all current features in respective tiers (no degradation)
> - Premium adds NEW AI features only
> - Standard tier at $49 unchanged (protect current paying users)
> - Enterprise gets premium features included (protect largest customers)
> - Grandfather existing users: special loyalty pricing
> - Clear privacy controls: AI features opt-in even for premium
> - Sales enablement: 2-week training before launch
> - CS prep: comprehensive FAQ, upgrade paths, objection handling"

### When to Disable

Disable for contexts where:
- Decision scope is very narrow with obvious stakeholders
- Time-critical situations require immediate action
- Stakeholder input has already been thoroughly gathered
- Over-analysis creates decision paralysis
