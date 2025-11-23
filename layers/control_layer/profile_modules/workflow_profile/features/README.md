# Workflow Feature References

This directory contains detailed instruction files for workflow features.

## How It Works

When a workflow profile has enabled features, the system automatically loads and appends the corresponding feature instruction files to the workflow prompt.

### Configuration

In `system_control.json`:

```json
"workflow_profiles": {
  "guided": {
    "features": {
      "auto_confirmation": {
        "enabled": true,
        "reference": "auto_confirmation.md"
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
- **Structure**: Description, Behavior, Examples, When Disabled

### Creating New Features

1. Add feature to profile in `system_control.json`
2. Create feature file: `features/{feature_name}.md`
3. Document behavior clearly
4. Include examples
5. Explain enabled vs disabled behavior

### Example Flow

**Guided profile active + auto_confirmation enabled:**

```
Content loaded:
1. /profiles/guided.md           (base profile instructions)
2. /features/auto_confirmation.md (feature-specific instructions)
3. /features/verbose_reasoning.md (another enabled feature)

Result: Combined into single workflow prompt
```

## Available Features

- **auto_confirmation.md** - Require user confirmation before significant actions
- **verbose_reasoning.md** - Provide detailed step-by-step reasoning
