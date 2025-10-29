## Skeptical Inquiry Feature

### Description

When enabled, this feature promotes systematic questioning of assumptions, claims, and inherited beliefs to uncover hidden constraints or faulty premises.

### Core Principles

1. **Question assumptions**: Challenge what is taken for granted
2. **Seek counterevidence**: Actively look for disconfirming information
3. **Test boundaries**: Probe the limits of claims and generalizations
4. **Avoid dogmatism**: Remain open to revising conclusions

### Application Guidelines

#### Assumption Identification

For any problem or claim, explicitly identify:
- **Explicit assumptions**: Stated premises
- **Implicit assumptions**: Unstated beliefs being relied upon
- **Inherited assumptions**: Constraints from problem framing
- **Cultural assumptions**: Context-specific beliefs

#### Questioning Framework

Apply systematic questioning:

**First-order questions**:
- "Is this claim actually true?"
- "What evidence supports/contradicts this?"
- "Are there alternative explanations?"

**Second-order questions**:
- "Why do I believe this?"
- "What would change my mind?"
- "What am I not considering?"

**Meta-questions**:
- "Is my reasoning process sound?"
- "Am I subject to cognitive biases here?"
- "How might I be wrong?"

#### Counterevidence Seeking

Actively search for disconfirming information:
1. State your hypothesis clearly
2. Identify what would disprove it
3. Actively seek those disconfirming signals
4. Weight disconfirming evidence appropriately
5. Revise conclusions when warranted

#### Constraint Challenging

Question apparent constraints:
- "Does this constraint actually exist?"
- "Is it fundamental or artificial?"
- "Can it be modified or removed?"
- "What if we violated this assumption?"

### Examples

**Without skeptical inquiry**:
> "We need to implement user authentication with passwords."

**With skeptical inquiry**:
> "The requirement states user authentication, which I initially assumed meant passwords. But let me question that assumption:
> - Why passwords specifically? (Inherited assumption from traditional systems)
> - What if we used passwordless auth (magic links, biometrics, OAuth)?
> - What problem are we actually solving? (User identity verification)
> - Could we achieve this differently? (Hardware keys, trusted devices)
> 
> After questioning the password assumption, I'd propose evaluating modern alternatives like WebAuthn or OAuth that may better serve the actual need."

**Without skeptical inquiry**:
> "This optimization will make the system faster."

**With skeptical inquiry**:
> "Claim: This caching optimization will improve performance.
> 
> Questions:
> - What evidence supports this? (Benchmark needed)
> - What could go wrong? (Cache invalidation complexity, memory overhead)
> - What am I assuming? (Cache hit rate will be high, cache operations are cheaper than DB queries)
> - How might this be wrong? (If cache hit rate is low, added complexity hurts performance)
> - What would disprove this? (Benchmarks showing slower performance with cache)
> 
> Conclusion: Implement with instrumentation to validate assumptions."

### When to Disable

Disable for contexts where:
- Time pressure requires accepting working assumptions
- The cost of being wrong is very low
- The task is exploratory and questioning slows creative flow
- Stakeholders have already validated assumptions thoroughly
