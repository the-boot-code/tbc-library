### Systematic Decomposition Feature

**Purpose:** Structured breakdown of complex problems into manageable, atomic components before attempting solutions.

**Core Principles:**
- Hierarchical breakdown: Decompose recursively to atomic units
- Dependency mapping: Identify relationships between components
- Component isolation: Analyze each part independently
- Synthesis integration: Recombine insights into complete solution

**Decomposition Process:**

**Step 1: Top-level decomposition**:
- Identify major components or subsystems
- Define clear boundaries
- Name each component descriptively

**Step 2: Recursive breakdown**:
- For each component, identify sub-components
- Continue until reaching atomic units
- Atomic = cannot be meaningfully subdivided for the task

**Step 3: Dependency analysis**:
- Map relationships: which components depend on which
- Identify critical path
- Note circular dependencies or coupling

**Step 4: Component analysis**:
- Analyze each atomic component independently
- Document inputs, outputs, constraints
- Identify issues or solutions at this level

**Step 5: Bottom-up synthesis**:
- Integrate component-level insights
- Build solution from atomic units upward
- Validate integration at each level

**Decomposition Dimensions**:
- **Functional**: What different functions does it perform?
- **Structural**: What are the physical/logical parts?
- **Temporal**: What are the sequential stages?
- **Spatial**: What are the geographical/locational divisions?
- **Stakeholder**: Who are the different actors/users?

**Examples:**

**Website Performance**:
- **Without**: "The website is slow. Let me optimize it." (unfocused approach)
- **With**: Systematic breakdown → Level 1: Frontend/Backend/Database/Network → Level 2: Frontend (page load/runtime), Backend (request handling/business logic/queries) → Dependencies mapped → Measure each component → Identify database queries as bottleneck (80% latency) → Focus optimization there

**User Authentication**:
- **Without**: "We need to implement user authentication." (monolithic approach)
- **With**: Decompose → Registration/Login/Session/Recovery/Authorization → Break down Registration (validation/hashing/creation/email) → Break down Login (validation/verification/token/rate limiting) → Dependency-driven implementation sequence → build from atomic units upward

**When to Disable:**
- Problem already well-understood and simple
- Speed more important than thorough analysis
- Exploratory work benefits from holistic thinking
- Over-decomposition creates unnecessary complexity
