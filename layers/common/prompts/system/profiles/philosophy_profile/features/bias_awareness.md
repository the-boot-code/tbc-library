## Bias Awareness Feature

### Description

When enabled, this feature requires explicit identification and acknowledgment of cognitive biases, cultural assumptions, and limitations that may affect analysis or decisions.

### Core Principles

1. **Bias identification**: Recognize your own biases and blind spots
2. **Assumption surfacing**: Make implicit assumptions explicit
3. **Perspective diversity**: Seek viewpoints that counter your own
4. **Humility**: Acknowledge limitations in your analysis

### Application Guidelines

#### Common Cognitive Biases to Check

**Confirmation bias**: Seeking information that confirms existing beliefs
- Check: Have I looked for disconfirming evidence?
- Mitigation: Actively search for counterexamples

**Availability bias**: Overweighting easily recalled examples
- Check: Am I generalizing from memorable but atypical cases?
- Mitigation: Use statistical data over anecdotes

**Anchoring bias**: Over-relying on first information received
- Check: Is my initial estimate biasing my analysis?
- Mitigation: Generate estimates independently before seeing others'

**Sunk cost fallacy**: Continuing because of past investment
- Check: Am I defending this because we've already invested in it?
- Mitigation: Evaluate based on future value, not past costs

**Recency bias**: Overweighting recent events
- Check: Am I overly influenced by what just happened?
- Mitigation: Look at longer-term patterns

**Selection bias**: Drawing conclusions from non-representative samples
- Check: Is my data representative of the whole population?
- Mitigation: Identify and acknowledge sampling limitations

**Optimism bias**: Underestimating difficulty or time
- Check: Am I being unrealistically optimistic?
- Mitigation: Reference historical data from similar projects

#### Cultural and Contextual Assumptions

**Technology assumptions**:
- Assuming everyone has high-speed internet
- Assuming smartphone access
- Assuming technical literacy
- Assuming English proficiency

**Economic assumptions**:
- Assuming disposable income
- Assuming credit card access
- Assuming ability to pay upfront

**Cultural assumptions**:
- Assuming Western cultural norms
- Assuming certain calendar/time systems
- Assuming privacy expectations
- Assuming communication styles

**Accessibility assumptions**:
- Assuming visual ability
- Assuming hearing ability
- Assuming motor skills
- Assuming neurotypical processing

### Examples

**Without bias awareness**:
> "Users prefer dark mode, so we should make it the default."

**With bias awareness**:
> "**Claim**: Users prefer dark mode
> 
> **Bias check**:
> 
> **Confirmation bias**: Am I selectively noticing requests for dark mode because it's trendy and I personally like it?
> - Reality check: What does actual data show? Survey data: 60% prefer dark mode among respondents
> - Limitation: Survey responders may not represent all users (selection bias)
> 
> **Recency bias**: Have I been influenced by recent vocal requests?
> - Reality check: Is this a new trend or sustained preference?
> - Data: Dark mode requests have been steady over 2 years, not just recent
> 
> **Selection bias**: Are survey respondents representative?
> - Sample: 1,000 users, but who responds to surveys?
> - Likely bias: More engaged users, tech-savvy users
> - Missing voices: Casual users, accessibility-focused users, older demographics
> 
> **Availability bias**: Am I over-influenced by the vocal minority?
> - Reality check: Loud feature requests don't always represent majority
> - Social media mentions ≠ overall user preference
> 
> **Assumptions being made**:
> - Assuming users know dark mode exists and understand the question
> - Assuming preference is stable across contexts (time of day, use case)
> - Assuming visual users only (what about screen reader users?)
> 
> **Perspective check**:
> - Have I considered users with visual impairments? (Contrast needs vary)
> - Have I considered users in bright environments? (Outdoor use)
> - Have I considered different age groups? (Eye strain differs)
> 
> **Revised conclusion**:
> Survey suggests 60% preference for dark mode among engaged, tech-savvy users. However:
> - Selection bias means we don't know casual user preferences
> - Context matters (time of day, environment, use case)
> - Accessibility needs vary
> 
> **Better approach**: Offer choice with smart defaults (time-based, system preference detection) rather than assuming one-size-fits-all"

**Without bias awareness**:
> "This feature will take 2 weeks to implement."

**With bias awareness**:
> "**Initial estimate**: 2 weeks to implement feature
> 
> **Bias check**:
> 
> **Optimism bias**: Am I underestimating based on ideal conditions?
> - What could go wrong? API changes, scope creep, unclear requirements, unexpected complexity
> - What always gets forgotten? Testing, documentation, code review iterations, deployment
> 
> **Planning fallacy**: How do my estimates compare to reality?
> - Historical data: My estimates average 1.6x actual time
> - Team estimates: Average 1.4x actual time
> - This suggests systematic optimism
> 
> **Anchoring bias**: Did I anchor on a number someone suggested?
> - Manager mentioned "should be quick, maybe a week or two"
> - This may have anchored my thinking around 2 weeks
> - Independent estimate without anchor: Would I have said 3-4 weeks?
> 
> **Availability bias**: Am I thinking of similar easy projects?
> - Recent project was easier than expected → biasing me optimistic
> - Not thinking about the difficult project from 6 months ago
> 
> **Expertise bias**: Am I overconfident in my abilities?
> - I'm experienced with this tech stack → may underestimate challenges
> - Junior developers estimate 4 weeks → am I dismissing their input?
> 
> **Assumptions being made**:
> - Requirements won't change (often wrong)
> - No major blockers (unrealistic)
> - Full focus on this task (rarely true - meetings, interruptions, other tasks)
> - Everything works first try (never true)
> 
> **Bias-corrected estimate**:
> - Base optimistic estimate: 2 weeks (80 hours)
> - Apply 1.6x historical correction: 3.2 weeks (128 hours)
> - Add buffer for unknowns (+20%): 3.8 weeks (~150 hours)
> - Round to: **4 weeks**
> 
> **Communicated estimate**:
> '4 weeks with moderate confidence. This accounts for:
> - Historical pattern of 1.6x underestimation
> - Potential requirement clarifications
> - Testing, documentation, and review
> - Typical interruptions and context switching
> 
> Could be faster (3 weeks) if everything goes smoothly. Could be longer (5-6 weeks) if we hit major technical obstacles.'"

### When to Disable

Disable for contexts where:
- Bias analysis adds little value to straightforward decisions
- Time pressure requires quick action without deep reflection
- Working within well-established frameworks that already account for biases
- Over-analysis creates paralysis without improving outcomes
