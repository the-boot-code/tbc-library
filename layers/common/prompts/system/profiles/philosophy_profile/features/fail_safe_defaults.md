## Fail-Safe Defaults Feature

### Description

When enabled, this feature requires using conservative, safe default values and behaviors when uncertain, prioritizing safety over convenience or performance.

### Core Principles

1. **Safe by default**: Default state should be the safest option
2. **Explicit opt-in for risk**: Dangerous operations require intentional action
3. **Fail closed, not open**: When in doubt, deny rather than allow
4. **Secure defaults**: Security and privacy by default, not opt-in

### Application Guidelines

#### Fail-Safe Default Patterns

**Security defaults**:
- Default deny (whitelist, not blacklist)
- Least privilege (minimal permissions by default)
- Encryption on (not optional)
- Authentication required (not optional)
- Secure protocols (HTTPS, not HTTP)

**Privacy defaults**:
- Data collection: Opt-in, not opt-out
- Sharing: Private by default
- Analytics: Disabled until user enables
- Third-party access: Denied by default

**Operational defaults**:
- Read-only mode when uncertain
- Conservative resource limits
- Timeout values that prevent hangs
- Graceful degradation over complete failure

**Data defaults**:
- Preserve data (don't delete without confirmation)
- Backup before destructive operations
- Soft deletes over hard deletes
- Versioning enabled by default

#### Fail-Safe Decision Framework

**When choosing defaults, ask**:

1. **What's the safest option**?
   - Not the most convenient
   - Not the most performant
   - The safest

2. **What happens if user does nothing**?
   - Should result in safe state
   - Should not expose risk
   - Should not grant unintended access

3. **What's the worst case scenario**?
   - Design defaults to prevent it
   - Make dangerous options require explicit action
   - Don't make risk the easy path

4. **Principle of least surprise**:
   - Conservative defaults are less surprising
   - Users expect safety, not danger
   - Explicit action for risk is expected

### Examples

**Without fail-safe defaults**:
> "New API endpoint is open to all users by default."

**With fail-safe defaults**:
> "**API endpoint configuration**:
> 
> **Unsafe default** (convenience-first):
> - Default: Public access
> - Requires action: Add authentication
> - Risk: Exposed endpoints if developer forgets
> - Many security breaches from this pattern
> 
> **Fail-safe default** (safety-first):
> - Default: Authentication required
> - Default: Rate limited (100 req/hour per IP)
> - Default: Read-only access
> - Requires action: Explicitly remove auth, increase limits, grant write access
> 
> **Implementation**:
> ```python
> class APIEndpoint:
>     def __init__(self):
>         self.require_auth = True  # Safe default
>         self.require_api_key = True  # Safe default
>         self.rate_limit = 100  # Conservative default
>         self.read_only = True  # Safe default
>         self.allowed_ips = []  # Empty whitelist (deny all)
>         
>     def allow_public_access(self):
>         # Explicit method to remove safety
>         # Makes risk visible and intentional
>         self.require_auth = False
>         log.warning('Public access enabled - security risk!')
> ```
> 
> **Result**:
> - Endpoints are secure by default
> - Developer must explicitly choose to reduce security
> - Explicit action makes risk visible
> - Safer codebase overall"

**Without fail-safe defaults**:
> "User data is shared with partners unless they opt out."

**With fail-safe defaults**:
> "**User data sharing configuration**:
> 
> **Unsafe default** (business-first):
> - Default: Share data with partners
> - User can opt-out in buried settings
> - Maximizes data sharing (business benefit)
> - Privacy violation, potential legal issues
> - Undermines user trust
> 
> **Fail-safe default** (privacy-first):
> - Default: No data sharing
> - User can explicitly opt-in if they want
> - Clear value proposition for sharing
> - Respects privacy by default
> - Builds trust
> 
> **Implementation**:
> ```python
> class UserPreferences:
>     def __init__(self):
>         # Privacy-respecting defaults
>         self.share_with_partners = False  # Fail-safe
>         self.analytics_enabled = False  # Fail-safe
>         self.marketing_emails = False  # Fail-safe
>         self.location_tracking = False  # Fail-safe
>         
>     # Opt-in requires explicit action
>     def enable_data_sharing(self, user_consent):
>         if user_consent.was_informed and user_consent.was_explicit:
>             self.share_with_partners = True
>             log.info('User opted into data sharing')
>         else:
>             raise ValueError('Informed, explicit consent required')
> ```
> 
> **Result**:
> - Users are private by default
> - Sharing requires informed, explicit consent
> - Complies with privacy regulations (GDPR, CCPA)
> - Ethical and trust-building"

**Without fail-safe defaults**:
> "Database connection timeout: 5 minutes (to avoid interruptions)"

**With fail-safe defaults**:
> "**Database connection configuration**:
> 
> **Unsafe default** (availability-first):
> - Connection timeout: 5 minutes (300 seconds)
> - Query timeout: None (unlimited)
> - Connection pool: 1000 connections
> - Risk: Hung connections, resource exhaustion, cascading failures
> 
> **Fail-safe default** (stability-first):
> - Connection timeout: 30 seconds (fail fast)
> - Query timeout: 10 seconds (prevent runaway queries)
> - Connection pool: 50 connections (conservative limit)
> - Idle connection timeout: 60 seconds
> 
> **Configuration**:
> ```python
> class DatabaseConfig:
>     # Fail-safe defaults
>     CONNECTION_TIMEOUT = 30  # Fail fast, don't hang
>     QUERY_TIMEOUT = 10  # Prevent runaway queries
>     MAX_CONNECTIONS = 50  # Conservative limit
>     IDLE_TIMEOUT = 60  # Clean up idle connections
>     
>     # Can be increased if justified
>     def set_extended_timeout(self, timeout, justification):
>         if timeout > self.CONNECTION_TIMEOUT:
>             log.warning(f'Extending timeout to {timeout}s: {justification}')
>             self.CONNECTION_TIMEOUT = timeout
> ```
> 
> **Rationale**:
> - Short timeouts prevent cascading failures
> - Resource limits prevent exhaustion
> - System fails fast and recovers quickly
> - Can increase for specific use cases, but default is safe
> 
> **Result**:
> - System remains stable under load
> - Failures are contained and recoverable
> - Explicit action needed to reduce safety margins"

**Without fail-safe defaults**:
> "File permissions: 777 (everyone can read/write/execute)"

**With fail-safe defaults**:
> "**File permission configuration**:
> 
> **Unsafe default** (convenience-first):
> - Permissions: 777 (rwxrwxrwx)
> - Everyone can read, write, execute
> - No permission errors!
> - Security nightmare
> 
> **Fail-safe default** (security-first):
> - Permissions: 640 (rw-r-----)
> - Owner: read/write
> - Group: read only
> - Others: no access
> - Conservative and secure
> 
> **Implementation**:
> ```python
> class FileManager:
>     # Fail-safe permission defaults
>     DEFAULT_FILE_PERMS = 0o640  # rw-r-----
>     DEFAULT_DIR_PERMS = 0o750   # rwxr-x---
>     
>     def create_file(self, path, permissions=None):
>         perms = permissions if permissions else self.DEFAULT_FILE_PERMS
>         
>         # Warn if overly permissive
>         if perms > 0o644:  # More permissive than rw-r--r--
>             log.warning(f'Creating {path} with permissive mode {oct(perms)}')
>             
>         os.open(path, os.O_CREAT | os.O_WRONLY, perms)
> ```
> 
> **Result**:
> - Files are secure by default
> - Least privilege principle
> - Must explicitly grant broader permissions
> - Security by default, not afterthought"

### When to Disable

Disable for contexts where:
- Safety constraints are genuinely not needed
- Conservative defaults create unacceptable user friction
- Operating in truly trusted environment
- Prototyping where safety can be added later
- But be very cautious - most "we don't need this" assumptions are wrong
