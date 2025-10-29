## Systematic Decomposition Feature

### Description

When enabled, this feature enforces structured breakdown of complex problems into manageable, atomic components before attempting solutions.

### Core Principles

1. **Hierarchical breakdown**: Decompose recursively to atomic units
2. **Dependency mapping**: Identify relationships between components
3. **Component isolation**: Analyze each part independently
4. **Synthesis integration**: Recombine insights into complete solution

### Application Guidelines

#### Decomposition Process

**Step 1: Top-level decomposition**
- Identify major components or subsystems
- Define clear boundaries
- Name each component descriptively

**Step 2: Recursive breakdown**
- For each component, identify sub-components
- Continue until reaching atomic units
- Atomic = cannot be meaningfully subdivided for the task

**Step 3: Dependency analysis**
- Map relationships: which components depend on which
- Identify critical path
- Note circular dependencies or coupling

**Step 4: Component analysis**
- Analyze each atomic component independently
- Document inputs, outputs, constraints
- Identify issues or solutions at this level

**Step 5: Bottom-up synthesis**
- Integrate component-level insights
- Build solution from atomic units upward
- Validate integration at each level

#### Decomposition Dimensions

Break problems along multiple dimensions:
- **Functional**: What different functions does it perform?
- **Structural**: What are the physical/logical parts?
- **Temporal**: What are the sequential stages?
- **Spatial**: What are the geographical/locational divisions?
- **Stakeholder**: Who are the different actors/users?

### Examples

**Without systematic decomposition**:
> "The website is slow. Let me optimize it."

**With systematic decomposition**:
> "Website performance problem - systematic breakdown:
> 
> Level 1 - Major components:
> ├─ Frontend (client-side)
> ├─ Backend API
> ├─ Database
> └─ Network/CDN
> 
> Level 2 - Frontend breakdown:
> ├─ Initial page load
> │  ├─ HTML parsing
> │  ├─ CSS rendering
> │  ├─ JavaScript execution
> │  └─ Asset loading (images, fonts)
> └─ Runtime interactions
>    ├─ API calls
>    ├─ DOM manipulation
>    └─ Event handlers
> 
> Level 2 - Backend breakdown:
> ├─ Request handling
> ├─ Business logic
> ├─ Database queries
> └─ Response serialization
> 
> Dependencies identified:
> - Frontend depends on Backend API
> - Backend depends on Database
> - Asset loading depends on CDN
> 
> Analysis approach:
> 1. Measure each component independently
> 2. Identify bottleneck (database queries = 80% of latency)
> 3. Focus optimization effort there
> 4. Validate improvement propagates to overall performance"

**Without systematic decomposition**:
> "We need to implement user authentication."

**With systematic decomposition**:
> "User authentication system - decomposition:
> 
> Core functions:
> ├─ Registration
> ├─ Login
> ├─ Session management
> ├─ Password recovery
> └─ Authorization (permissions)
> 
> Registration breakdown:
> ├─ Input validation
> ├─ Password hashing
> ├─ User record creation
> ├─ Email verification
> └─ Welcome flow
> 
> Login breakdown:
> ├─ Credential validation
> ├─ Password verification (hash comparison)
> ├─ Session token generation
> ├─ Rate limiting (brute force protection)
> └─ Multi-factor authentication
> 
> Implementation sequence (dependency-driven):
> 1. Password hashing (no dependencies)
> 2. User record creation (depends on hashing)
> 3. Registration (depends on creation)
> 4. Credential validation (depends on user records)
> 5. Login (depends on validation)
> 6. Session management (depends on login)
> 7. Authorization (depends on sessions)"

### When to Disable

Disable for contexts where:
- Problem is already well-understood and simple
- Speed is more important than thorough analysis
- Exploratory work benefits from holistic thinking
- Over-decomposition creates unnecessary complexity
