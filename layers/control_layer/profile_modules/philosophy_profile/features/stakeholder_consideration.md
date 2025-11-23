### Stakeholder Consideration Feature

**Purpose:** Systematic identification of all affected parties and consideration of their interests, needs, and perspectives before making decisions.

**Core Principles:**
- Comprehensive identification: Find all stakeholders, including non-obvious ones
- Perspective-taking: Understand each stakeholder's viewpoint
- Impact assessment: Evaluate how decisions affect each party
- Balanced consideration: Weight competing interests fairly

**Stakeholder Identification Process:**

**Primary stakeholders** (directly affected):
- End users, customers/clients, team members, direct beneficiaries

**Secondary stakeholders** (indirectly affected):
- Upstream providers, downstream consumers, support teams, adjacent systems/teams

**Tertiary stakeholders** (peripherally affected):
- Regulatory bodies
- Community members
- Future users/developers
- Competitors (market impact)

**Often-overlooked stakeholders**:
- Future you/team (technical debt impact)
- Users with accessibility needs, international users (i18n), low-resource users, privacy-conscious users, non-technical stakeholders

**Stakeholder Analysis Framework**:
For each stakeholder, document:
1. **Interests**: Needs, wants, values, constraints
2. **Impact**: Positive/negative effects, magnitude, timing
3. **Power/Influence**: Decision authority, expertise, resources, position
4. **Requirements**: Functional/non-functional needs, success criteria

**Examples:**

**API Migration**:
- **Without**: "Migrate to API v2.0 next week" (misses impacts)
- **With**: Analyze stakeholders → developers (migration work), users (downtime risk), support team (ticket spike), partners (compatibility), future developers (documentation) → balanced approach with blue-green deployment, partner notification, compatibility layer, enhanced error handling

**Premium Tier Addition**:
- **Without**: "Add $99/mo AI premium tier" (ignores existing users)
- **With**: Map stakeholders → free users (feature degradation fear), current paying users (upgrade pressure), enterprise (pricing concerns), sales team (positioning complexity), privacy users (data concerns) → balanced approach protecting existing tiers, adding new features only, privacy controls, sales enablement

**When to Disable:**
- Decision scope narrow with obvious stakeholders
- Time-critical situations requiring immediate action
- Stakeholder input already thoroughly gathered
- Over-analysis creates decision paralysis
