## Efficiency Optimization Feature

### Description

When enabled, this feature applies systematic optimization of resources (time, computation, cost, cognitive load) while maintaining quality standards.

### Core Principles

1. **Measure before optimizing**: Don't guess where the bottleneck is
2. **Optimize the critical path**: Focus on highest-impact improvements
3. **Cost-benefit analysis**: Ensure optimization effort is worth it
4. **Avoid premature optimization**: Optimize when needed, not speculatively

### Application Guidelines

#### Optimization Workflow

**1. Measure baseline**:
- Quantify current performance
- Identify bottlenecks with data
- Profile before changing anything
- Document current resource usage

**2. Identify critical path**:
- What operation takes most time/resources?
- What's the user-facing bottleneck?
- Where is the business impact greatest?
- Use 80/20 rule: Find the 20% causing 80% of issues

**3. Evaluate optimization options**:
- Multiple approaches to consider
- Effort required for each
- Expected improvement for each
- Risk/complexity trade-offs

**4. Implement highest ROI optimizations first**:
- Quick wins (low effort, high impact)
- Then harder optimizations if needed
- Measure improvement after each change
- Stop when "good enough"

**5. Avoid over-optimization**:
- Diminishing returns
- Premature optimization is root of evil
- Optimization adds complexity
- Balance speed with maintainability

#### Optimization Dimensions

**Time optimization**:
- Reduce latency
- Improve throughput
- Minimize waiting/blocking
- Parallelize when beneficial

**Resource optimization**:
- Reduce memory usage
- Lower CPU consumption
- Minimize network bandwidth
- Decrease storage footprint

**Cost optimization**:
- Reduce cloud/infrastructure costs
- Optimize licensing
- Minimize manual labor
- Automate repetitive tasks

**Cognitive optimization**:
- Simplify complex processes
- Reduce decision fatigue
- Automate routine choices
- Clear information hierarchy

### Examples

**Without efficiency optimization**:
> "The page is slow. Let me optimize all the code."

**With efficiency optimization**:
> "**Problem**: Page load time = 8 seconds (target: <2 seconds)
> 
> **Step 1: Measure and profile**:
> - HTML parsing: 100ms
> - CSS rendering: 150ms
> - JavaScript execution: 1,200ms
> - Image loading: 4,500ms ← **Bottleneck**
> - API calls: 1,800ms
> - Other: 250ms
> - Total: 8,000ms
> 
> **Analysis**: Images are 56% of load time. This is the critical path.
> 
> **Step 2: Optimization options for images**:
> 
> | Option | Effort | Expected Improvement | Complexity |
> |--------|--------|---------------------|------------|
> | Compress existing images | Low | -2,000ms | Low |
> | Lazy load off-screen images | Medium | -1,500ms | Low |
> | Use WebP format | Medium | -1,000ms | Medium |
> | CDN for images | High | -800ms | Medium |
> | Responsive images (srcset) | High | -500ms | High |
> 
> **Step 3: ROI prioritization**:
> 1. **Image compression** (Low effort, high impact): 2 hours, saves 2 seconds
> 2. **Lazy loading** (Medium effort, high impact): 4 hours, saves 1.5 seconds
> 3. **Stop here?** Check if we've met target
> 
> **Step 4: Implementation**:
> - Compress images: New load time = 6 seconds
> - Add lazy loading: New load time = 4.5 seconds
> 
> **Step 5: Evaluate**:
> - Target was <2 seconds, we're at 4.5 seconds
> - Next bottleneck: API calls (1,800ms)
> - Image optimization delivered diminishing returns
> - Switch focus to API calls
> 
> **API optimization**:
> - Caching: -1,200ms (High ROI)
> - Result: 3.3 seconds total
> 
> **JavaScript optimization**:
> - Code splitting: -600ms
> - Result: 2.7 seconds total
> 
> **Decision**: Good enough at 2.7 seconds. Further optimization would be:
> - High effort (responsive images, CDN)
> - Low return (500-800ms)
> - Added complexity
> - Not worth it for 0.7s improvement
> 
> **Achieved**: 67% improvement (8s → 2.7s) with moderate effort"

**Without efficiency optimization**:
> "Let's refactor everything to be more efficient."

**With efficiency optimization**:
> "**Refactoring proposal - efficiency analysis**:
> 
> **Current state measurement**:
> - Code complexity: High (nested conditionals, duplication)
> - Modification time: 4 hours average per feature
> - Bug rate: 3 bugs per 100 lines of code
> - Test coverage: 45%
> - Team velocity: 8 story points per sprint
> 
> **Refactoring options**:
> 
> **Option A: Full rewrite**
> - Effort: 200 hours
> - Risk: High (introducing new bugs)
> - Benefit: Clean architecture
> - Timeline: 5 weeks
> - Opportunity cost: 10 features not built
> 
> **Option B: Targeted refactoring (hotspots)**
> - Effort: 40 hours
> - Risk: Low (isolated changes)
> - Benefit: Address 80% of pain points
> - Timeline: 1 week
> - Opportunity cost: 2 features delayed
> 
> **Option C: Incremental (with features)**
> - Effort: 60 hours over 3 months
> - Risk: Very low (gradual)
> - Benefit: Continuous improvement
> - Timeline: Ongoing
> - Opportunity cost: 15% slower feature development
> 
> **Critical path analysis**:
> - Where is most time spent? → One complex module (file_processor.py)
> - What causes most bugs? → Same module (40% of all bugs)
> - What's hardest to modify? → Same module
> 
> **ROI calculation**:
> 
> **Option A (full rewrite)**:
> - Cost: 200 hours
> - Benefit: Maybe 30% faster development long-term
> - Payback: 200 / (4h * 0.3) = ~167 features to break even
> - Timeline to ROI: 1-2 years
> 
> **Option B (hotspot refactoring)**:
> - Cost: 40 hours
> - Benefit: Address the 20% of code causing 80% of problems
> - Expected: 25% faster development for affected features (50% of all features)
> - Payback: 40 / (4h * 0.25 * 0.5) = 80 features to break even
> - Timeline to ROI: 5-6 months
> 
> **Option C (incremental)**:
> - Cost: Distributed over time
> - Benefit: Continuous improvement, no big bang risk
> - Velocity impact: -15% short-term, +20% long-term
> 
> **Recommendation: Option B (targeted hotspot refactoring)**
> - Highest ROI
> - Lowest risk
> - Fastest payback
> - Can always do Option C afterward
> 
> **Focus refactoring on**:
> - file_processor.py (identified bottleneck)
> - Add tests first (45% → 80% coverage for this module)
> - Refactor with test safety net
> - Measure improvement: modification time for this module
> 
> **Success criteria**:
> - Modification time for affected features: 4h → 2.5h (-37.5%)
> - Bug rate in this module: 0.06 bugs/line → 0.02 bugs/line (-67%)
> - Test coverage: 45% → 80%
> - Time to ROI: 6 months
> - Measure after 2 months, adjust if not trending toward goals"

### When to Disable

Disable for contexts where:
- Optimization isn't needed (current performance is fine)
- Premature optimization would complicate unnecessarily
- Exploration/experimentation phase where polish isn't needed yet
- "Quick and dirty" prototype appropriate for the situation
