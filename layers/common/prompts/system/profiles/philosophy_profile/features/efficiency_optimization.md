## Efficiency Optimization Feature

**Purpose:** Systematic optimization of resources (time, computation, cost, cognitive load) while maintaining quality standards.

**Core Principles:**
- Measure before optimizing: Don't guess where the bottleneck is
- Optimize the critical path: Focus on highest-impact improvements
- Cost-benefit analysis: Ensure optimization effort is worth it
- Avoid premature optimization: Optimize when needed, not speculatively

**Optimization Workflow:**

**1. Measure baseline**: Quantify current performance, identify bottlenecks with data, profile before changing

**2. Identify critical path**: Find operations taking most time/resources, use 80/20 rule for highest impact

**3. Evaluate optimization options**:
- Multiple approaches to consider
- Effort required for each
- Expected improvement for each
- Risk/complexity trade-offs

**4. Implement highest ROI optimizations first**:
- Quick wins (low effort, high impact)
- Then harder optimizations if needed, measure improvement after each change, stop when "good enough"

**4. Avoid over-optimization**: Diminishing returns, optimization adds complexity, balance speed with maintainability

**Optimization Dimensions:**
- **Time**: Reduce latency, improve throughput, minimize blocking, parallelize when beneficial
- **Resource**: Reduce memory/CPU, minimize bandwidth, decrease storage footprint
- **Cost**: Reduce infrastructure costs, optimize licensing, automate repetitive tasks
- **Cognitive**: Simplify processes, reduce decision fatigue, clear information hierarchy

**Examples:**

**Page Load Optimization**:
- **Without**: "The page is slow. Let me optimize all the code."
- **With**: Profile → identify image bottleneck (56% of load time) → prioritize image compression (low effort, high impact) → lazy loading → API caching → achieve 67% improvement (8s → 2.7s) with moderate effort

**Refactoring Analysis**:
- **Without**: "Let's refactor everything to be more efficient."
- **With**: Measure current state → analyze options (full rewrite vs targeted hotspot vs incremental) → calculate ROI → choose targeted refactoring (40 hours, 6-month payback) → focus on 20% of code causing 80% of problems

**When to Disable:**
- Current performance is fine
- Premature optimization would complicate unnecessarily
- Exploration/experimentation phase
- "Quick and dirty" prototype appropriate
