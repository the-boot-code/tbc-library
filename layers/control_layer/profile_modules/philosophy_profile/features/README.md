# Philosophy Feature References

This directory contains detailed instruction files for philosophy features that can be enabled across different philosophy profiles.

## How It Works

When a philosophy profile has enabled features, the system automatically loads and appends the corresponding feature instruction files to the philosophy prompt.

### Configuration

In `system_control.json`:

```json
"philosophy_profiles": {
  "research": {
    "features": {
      "epistemic_rigor": {
        "enabled": true,
        "reference": "epistemic_rigor.md"
      },
      "source_verification": {
        "enabled": true,
        "reference": "source_verification.md"
      }
    }
  }
}
```

### Loading Behavior

1. **Profile loads first**: `/profiles/{profile_name}.md`
2. **For each enabled feature**: Load `/features/{reference}.md`
3. **Combine**: Append feature instructions after profile content
4. **Graceful fallback**: Missing files are skipped with log message

### Convention

- **File naming**: Use `reference` field or default to `{feature_name}.md`
- **Content format**: Standard markdown with clear sections
- **Structure**: Description, Principles, Application, Examples

### Creating New Features

1. Add feature to profile in `system_control.json`
2. Create feature file: `features/{feature_name}.md`
3. Document principles and application clearly
4. Include concrete examples
5. Explain how it modifies behavior

## Feature Categories

### Epistemological Features (How we know)
- **epistemic_rigor** - Strict evidence standards and confidence levels
- **source_verification** - Citation and cross-referencing requirements
- **skeptical_inquiry** - Question assumptions systematically
- **empirical_grounding** - Favor observable evidence

### Methodological Features (How we approach)
- **systematic_decomposition** - Break down complex problems
- **divergent_thinking** - Explore multiple alternatives
- **hypothesis_testing** - Scientific method application
- **analogical_reasoning** - Cross-domain insights
- **root_cause_analysis** - Deep causal investigation

### Ethical Features (What guides us)
- **harm_prevention** - Minimize negative impacts
- **transparency_first** - Open communication priority
- **stakeholder_consideration** - Multi-perspective analysis
- **bias_awareness** - Acknowledge limitations
- **consent_respect** - User autonomy priority

### Operational Features (How we execute)
- **efficiency_optimization** - Speed/resource trade-offs
- **satisficing** - Good enough principle
- **consensus_building** - Agreement-seeking approaches
- **reversibility_preference** - Favor undo-able actions
- **fail_safe_defaults** - Conservative choices

## Composability

Features can be combined across profiles. For example, a custom profile might combine:
- `epistemic_rigor` (epistemological)
- `harm_prevention` (ethical)
- `systematic_decomposition` (methodological)

This creates a rigorous, safety-conscious, analytical approach.
