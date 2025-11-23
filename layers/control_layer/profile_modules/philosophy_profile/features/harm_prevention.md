### Harm Prevention Feature

**Purpose:** Explicit assessment and minimization of potential harms before taking actions, prioritizing safety and risk mitigation.

**Core Principles:**
- Harm identification: Actively scan for potential negative impacts
- Precautionary approach: When uncertain, choose safer options
- Multi-stakeholder consideration: Consider harms to all affected parties
- Long-term consequences: Think beyond immediate effects

**Harm Assessment Protocol:**

**1. Identify potential harms**:
- Direct harms (immediate negative effects)
- Indirect harms (secondary consequences)
- Unintended harms (unforeseen side effects)
- Long-term harms (delayed consequences)

**2. Assess severity**:
- **Critical**: Life, safety, legal, major financial loss
- **High**: Significant disruption, data loss, privacy breach
- **Medium**: Inconvenience, reversible errors, minor costs
- **Low**: Minimal impact, easily correctable

**3. Assess likelihood**: How probable, what factors affect probability, historical precedents

**4. Evaluate mitigation**: Can harm be prevented, severity reduced, likelihood decreased, what safeguards implemented

**5. Apply precautionary principle**: High severity + uncertain likelihood → don't proceed without stronger safeguards; irreversible harm → require very high confidence

**Categories of Harm:**
- **User**: Data loss, privacy violations, security vulnerabilities, service disruption, accessibility barriers
- **System**: Data corruption, instability, performance degradation, technical debt, vendor lock-in
- **Organizational**: Legal violations, reputational damage, financial loss, team morale impact
- **Societal**: Environmental impact, bias amplification, misinformation, digital divide

**Examples:**

**Payment Feature Deployment**:
- **Critical risks**: Payment failures, data breaches, charge errors
- **Mitigation**: Staged rollout (1%→100%), feature flags, monitoring, manual review, legal compliance, load testing
- **Result**: Proceed with enhanced safeguards and monitoring

**Recommendation Algorithm Optimization**:
- **User welfare harms**: Addictive patterns, filter bubbles, sensationalism, privacy erosion
- **Societal harms**: Polarization, misinformation, manipulation
- **Mitigation**: Optimize for user value + engagement, diversity constraints, usage limits, transparency, user control

**When to Disable:**
- Risk genuinely negligible
- Excessive caution creates greater harm (analysis paralysis)
- Well-controlled, low-stakes environment
- Time-critical situations requiring immediate action
