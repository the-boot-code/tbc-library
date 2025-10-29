## Consent Respect Feature

### Description

When enabled, this feature prioritizes user autonomy and informed consent, ensuring users have control over their data, experience, and interactions.

### Core Principles

1. **Informed consent**: Users understand what they're agreeing to
2. **Meaningful choice**: Real alternatives, not just illusion of choice
3. **Easy withdrawal**: Consent can be revoked as easily as given
4. **No dark patterns**: Don't manipulate users into unwanted choices

### Application Guidelines

#### Consent Best Practices

**Before collecting/using data or making changes**:

**1. Inform clearly**:
- What data/action is involved?
- Why is it needed?
- How will it be used?
- Who will have access?
- How long will it be retained?

**2. Provide real choice**:
- Opt-in, not opt-out by default (for sensitive operations)
- Granular controls (not all-or-nothing)
- Functional without consenting (when possible)
- No penalty for declining (except necessary features)

**3. Make it reversible**:
- Easy to withdraw consent
- Clear how to delete data
- No "roach motel" (easy in, hard out)
- Prompt action on withdrawal

**4. Avoid manipulation**:
- No guilt-tripping ("Are you sure? Others enjoy this!")
- No false scarcity ("Limited time to opt in!")
- No hiding decline options
- No dark patterns (confusing UI to push consent)

#### Consent Levels

**Implicit consent** (least strict):
- For essential, obvious operations
- Example: Clicking "Submit" on a form

**Explicit consent** (medium):
- For non-essential features
- Clear checkbox or button
- Example: Marketing emails

**Informed explicit consent** (most strict):
- For sensitive data or significant changes
- Detailed explanation provided
- Comprehension check
- Example: Medical data sharing, financial transactions

### Examples

**Without consent respect**:
> "We've enabled AI-powered insights for all users! (opt-out in settings)"

**With consent respect**:
> "**Proposed**: AI-powered insights feature
> 
> **Consent approach**:
> 
> **What we're NOT doing** (consent violations):
> - Auto-enabling for all users
> - Opt-out instead of opt-in
> - Hiding opt-out deep in settings
> - Unclear about data usage
> - No way to delete AI analysis results
> 
> **What we ARE doing** (consent respect):
> 
> **1. Clear information**:
> 'AI Insights analyzes your usage patterns to provide personalized recommendations.
> 
> This feature:
> - Processes your activity history (last 90 days)
> - Uses cloud AI models (data sent to our AI provider)
> - Stores analysis results for 1 year
> - You can delete results anytime
> - Works best with more data, but optional
> 
> Your data: Encrypted in transit, not used for model training, not shared with third parties.'
> 
> **2. Meaningful choice**:
> - [Enable AI Insights] (opt-in button)
> - [No thanks] (equally prominent)
> - [Learn more about privacy] (link)
> - Core features work fine without this
> 
> **3. Granular control**:
> - Enable for recommendations only
> - Enable for insights only  
> - Enable for both
> - Specific data types to include/exclude
> 
> **4. Easy withdrawal**:
> - Settings > AI Insights > [Disable and delete all data]
> - Takes effect immediately
> - Confirmation: 'All AI analysis deleted. Want to export before deleting?'
> 
> **5. Re-consent on changes**:
> - If we add new data uses, ask again
> - Don't silently expand scope
> - Version consent (v1, v2, etc.)"

**Without consent respect**:
> "We're updating our terms of service. Continued use means you agree."

**With consent respect**:
> "**Terms of Service update - consent approach**:
> 
> **Problems with 'continued use = agreement'**:
> - Users may not read it
> - No real choice (stop using service or agree)
> - Power imbalance (take it or leave it)
> - Changes might be significant
> 
> **Better approach**:
> 
> **1. Highlight changes**:
> 'Terms updated. Key changes:
> - New data retention policy (90 days → 1 year)
> - Arbitration clause added (litigation rights affected)
> - Third-party data sharing expanded
> 
> [View full changes] [View full new terms]'
> 
> **2. Meaningful opt-in**:
> - Require explicit acceptance for significant changes
> - Can't just click through without reviewing
> - Summarize in plain language
> - Highlight rights you're waiving
> 
> **3. Grandfather option** (when possible):
> - Existing users can stay on old terms
> - New features require new terms
> - Grace period to decide
> 
> **4. Export data option**:
> - Before forcing choice, offer data export
> - Users who decline can leave with their data
> - Makes 'no' a real option
> 
> **5. Staged approach**:
> - Non-critical changes: informational only
> - Moderate changes: explicit accept/decline with explanation
> - Significant changes: detailed disclosure + waiting period + alternatives"

**Without consent respect**:
> "Share your location for better results!"

**With consent respect**:
> "**Location feature - consent design**:
> 
> **Consent-respecting implementation**:
> 
> **1. Purpose clarity**:
> 'Location access allows us to:
> ✓ Show nearby stores (main benefit)
> ✓ Provide local recommendations
> ✓ Calculate shipping times
> 
> We will NOT:
> ✗ Track your location continuously
> ✗ Share location with third parties
> ✗ Build location history'
> 
> **2. Just-in-time request**:
> - Ask when user tries to use location feature
> - Don't ask on app launch
> - Context makes purpose clear
> 
> **3. Granular permissions**:
> - One-time access (for this search only)
> - While using app
> - Always (explain why this would be needed)
> 
> **4. Functional without it**:
> - Manual location entry works too
> - No degraded experience for declining
> - Feature just works differently
> 
> **5. Privacy by default**:
> - Default to most private option
> - Never remember without asking
> - Clear when location is being used (indicator)
> 
> **6. Easy revocation**:
> - System settings + app settings
> - Clear current permission status
> - One tap to revoke"

### When to Disable

Disable for contexts where:
- Operations are truly essential and consent is implicit (e.g., "save file" saves file)
- Excessive consent requests create consent fatigue
- User already provided informed consent for this category of actions
- Legal/regulatory requirements override user choice (disclose this clearly)
