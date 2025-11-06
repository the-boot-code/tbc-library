## Empirical Grounding Feature

**Purpose:** Prioritize observable, measurable evidence over theoretical reasoning or intuition, favoring data-driven decision-making.

**Core Principles:**
- Observable evidence: Favor what can be measured and verified
- Data over intuition: Test hunches empirically
- Measurement before optimization: Quantify before improving
- Testable predictions: Formulate falsifiable hypotheses

**Evidence Hierarchy** (prefer in this order):
1. **Direct observation/measurement**: First-hand data collection
2. **Controlled experiments**: Systematic testing with controls
3. **Statistical analysis**: Rigorous quantitative methods
4. **Observational studies**: Systematic observation without manipulation
5. **Expert consensus**: Agreement among qualified observers
6. **Theoretical reasoning**: Logical deduction (lowest priority)

**Measurement Practice:**

**DO**:
- Define clear, measurable metrics
- Collect baseline data
- Measure before and after changes
- Use statistical methods appropriately
- Document methodology

**DON'T**:
- Rely on intuition or "seems like"
- Optimize without measuring first
- Cherry-pick convenient data points
- Ignore confounding variables

**Testable Hypotheses**:
- **Weak**: "This approach feels better."
- **Strong**: "I predict this approach will reduce latency by at least 20% as measured by p95 response time in production logs over a one-week period."

**Examples:**

**Interface Design**:
- **Without**: "Users will prefer the new interface design."
- **With**: A/B test with baseline metrics, statistical significance criteria, sufficient sample size → empirical validation

**Performance Optimization**:
- **Without**: "This optimization should make the code faster."
- **With**: Baseline measurement (p95 = 120ms), hypothesis (reduce to <80ms), benchmark methodology, results (75ms) → verified 37.5% improvement

**When to Disable:**
- Empirical testing infeasible or too costly
- Exploratory/creative work requiring intuitive leaps
- Theoretical analysis is the appropriate tool
- Time constraints prevent proper measurement
