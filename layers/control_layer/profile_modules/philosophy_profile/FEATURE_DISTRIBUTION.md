# Philosophy Profile Feature Distribution

All 19 features are now distributed across the 6 non-default philosophy profiles, with logical groupings based on the profile's core purpose.

## Profile → Feature Mapping

### 🔬 **Research Profile** (6 features)
Academic and scientific rigor, evidence-based reasoning

1. ✅ `epistemic_rigor` - Strict evidence standards, confidence calibration
2. ✅ `source_verification` - Citation requirements, cross-referencing
3. ✅ `skeptical_inquiry` - Question assumptions systematically
4. ✅ `empirical_grounding` - Favor observable evidence over theory
5. ✅ `hypothesis_testing` - Scientific method application
6. ✅ `bias_awareness` - Acknowledge cognitive biases and limitations

**Rationale**: Research requires rigorous epistemological standards, systematic questioning, empirical validation, and awareness of biases that could compromise scientific integrity.

---

### 🎨 **Creative Profile** (3 features)
Innovation, exploration, divergent thinking

1. ✅ `divergent_thinking` - Explore multiple alternatives before converging
2. ✅ `analogical_reasoning` - Cross-domain pattern recognition
3. ✅ `skeptical_inquiry` - Question inherited constraints and assumptions

**Rationale**: Creativity requires exploring many possibilities, drawing insights from diverse domains, and challenging conventional assumptions to find novel solutions.

---

### 📊 **Analytical Profile** (4 features)
Systematic problem-solving, logical rigor

1. ✅ `systematic_decomposition` - Break complex problems into components
2. ✅ `root_cause_analysis` - Deep causal investigation (5 Whys, fishbone)
3. ✅ `hypothesis_testing` - Formulate and test predictions
4. ✅ `empirical_grounding` - Data-driven decision-making

**Rationale**: Analysis requires breaking down complexity, finding root causes, testing hypotheses, and basing conclusions on empirical evidence.

---

### 🤝 **Collaborative Profile** (4 features)
Team-oriented, consensus-driven, stakeholder-focused

1. ✅ `consensus_building` - Agreement-seeking decision processes
2. ✅ `stakeholder_consideration` - Multi-perspective analysis
3. ✅ `transparency_first` - Open reasoning and communication
4. ✅ `bias_awareness` - Acknowledge limitations and perspectives

**Rationale**: Collaboration requires building consensus, considering all stakeholders, transparent communication, and awareness of how biases affect group decisions.

---

### ⚡ **Efficiency Profile** (2 features)
Speed optimization, resource conservation, pragmatic decisions

1. ✅ `satisficing` - "Good enough" over perfectionism
2. ✅ `efficiency_optimization` - Systematic resource optimization

**Rationale**: Efficiency demands pragmatic "satisficing" and systematic optimization of time, resources, and effort.

---

### 🛡️ **Safety Profile** (5 features)
Risk mitigation, harm prevention, conservative defaults

1. ✅ `harm_prevention` - Explicit harm assessment before action
2. ✅ `reversibility_preference` - Favor undo-able actions
3. ✅ `fail_safe_defaults` - Conservative, safe defaults
4. ✅ `consent_respect` - User autonomy and informed consent
5. ✅ `transparency_first` - Clear communication of risks and impacts

**Rationale**: Safety requires preventing harm, preferring reversible actions, using fail-safe defaults, respecting user consent, and transparent communication about risks.

---

## Feature → Profile Reverse Mapping

### Features Used in Multiple Profiles

**`skeptical_inquiry`** (2 profiles):
- Research: Question assumptions in scientific inquiry
- Creative: Challenge constraints to find novel solutions

**`empirical_grounding`** (2 profiles):
- Research: Evidence-based claims and conclusions
- Analytical: Data-driven analysis and decisions

**`hypothesis_testing`** (2 profiles):
- Research: Scientific method for investigation
- Analytical: Formulate and test predictions

**`bias_awareness`** (2 profiles):
- Research: Acknowledge biases that compromise rigor
- Collaborative: Understand how biases affect group decisions

**`transparency_first`** (2 profiles):
- Collaborative: Open communication in team settings
- Safety: Clear disclosure of risks and impacts

### Features Used in Single Profiles

**Epistemological** (unique to Research):
- `epistemic_rigor`
- `source_verification`

**Methodological**:
- `divergent_thinking` (Creative)
- `analogical_reasoning` (Creative)
- `systematic_decomposition` (Analytical)
- `root_cause_analysis` (Analytical)

**Ethical** (distributed):
- `harm_prevention` (Safety)
- `stakeholder_consideration` (Collaborative)
- `consent_respect` (Safety)

**Operational**:
- `efficiency_optimization` (Efficiency)
- `satisficing` (Efficiency)
- `consensus_building` (Collaborative)
- `reversibility_preference` (Safety)
- `fail_safe_defaults` (Safety)

---

## Feature Count by Profile

| Profile | Feature Count | Features |
|---------|---------------|----------|
| **Research** | 6 | epistemic_rigor, source_verification, skeptical_inquiry, empirical_grounding, hypothesis_testing, bias_awareness |
| **Creative** | 3 | divergent_thinking, analogical_reasoning, skeptical_inquiry |
| **Analytical** | 4 | systematic_decomposition, root_cause_analysis, hypothesis_testing, empirical_grounding |
| **Collaborative** | 4 | consensus_building, stakeholder_consideration, transparency_first, bias_awareness |
| **Efficiency** | 2 | satisficing, efficiency_optimization |
| **Safety** | 5 | harm_prevention, reversibility_preference, fail_safe_defaults, consent_respect, transparency_first |
| **Default** | 0 | (none - balanced general-purpose) |

---

## All 19 Features ✓

### Epistemological (4)
- [x] epistemic_rigor → Research
- [x] source_verification → Research
- [x] skeptical_inquiry → Research, Creative
- [x] empirical_grounding → Research, Analytical

### Methodological (5)
- [x] systematic_decomposition → Analytical
- [x] divergent_thinking → Creative
- [x] hypothesis_testing → Research, Analytical
- [x] analogical_reasoning → Creative
- [x] root_cause_analysis → Analytical

### Ethical (5)
- [x] harm_prevention → Safety
- [x] transparency_first → Collaborative, Safety
- [x] stakeholder_consideration → Collaborative
- [x] bias_awareness → Research, Collaborative
- [x] consent_respect → Safety

### Operational (5)
- [x] efficiency_optimization → Efficiency
- [x] satisficing → Efficiency
- [x] consensus_building → Collaborative
- [x] reversibility_preference → Safety
- [x] fail_safe_defaults → Safety

**Total: 19/19 features distributed ✓**

---

## Usage Examples

### Research Philosophy
```json
{
  "philosophy": {"active_profile": "research"}
}
```
**Result**: Agent applies strict evidence standards, cites sources, questions assumptions, grounds claims empirically, uses hypothesis testing, and acknowledges biases. Ideal for academic research, fact-checking, technical analysis.

### Creative Philosophy
```json
{
  "philosophy": {"active_profile": "creative"}
}
```
**Result**: Agent explores multiple alternatives, draws cross-domain insights, challenges constraints. Ideal for brainstorming, innovation, design thinking.

### Safety Philosophy
```json
{
  "philosophy": {"active_profile": "safety"}
}
```
**Result**: Agent assesses harm, prefers reversible actions, uses conservative defaults, respects consent, communicates risks transparently. Ideal for production deployments, user data operations, high-stakes decisions.

---

## Synergies and Overlaps

### Research + Analytical
Both share `empirical_grounding` and `hypothesis_testing` - complementary for scientific problem-solving

### Collaborative + Safety
Both share `transparency_first` - critical for team decisions with risk considerations

### Research + Collaborative
Both share `bias_awareness` - important for group research and peer review

### Creative + Research
Both share `skeptical_inquiry` - questioning assumptions drives both innovation and scientific rigor

---

**Updated**: October 29, 2025  
**Status**: All 19 features distributed across 6 profiles with logical groupings
