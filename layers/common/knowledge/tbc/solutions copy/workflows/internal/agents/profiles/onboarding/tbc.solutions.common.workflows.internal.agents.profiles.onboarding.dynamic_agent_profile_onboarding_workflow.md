# tbc.solutions.workflows.internal.agents.profiles.onboarding.dynamic_agent_profile_onboarding_workflow.md

**Formalized Workflow: Dynamic Onboarding of Subordinate Agent Prompt Profiles**

## Introduction
This document outlines a formalized, robust, and administrator-guided workflow for dynamically onboarding new subordinate agent prompt profiles into the Agent Zero system. This process leverages symbolic links to make agent profiles available without requiring system restarts or complex, permanent configurations like bind mounts or Docker Compose, thereby offering significant operational flexibility.

## Problem Statement
The challenge is to reliably and safely introduce new subordinate agent profiles into the Agent Zero framework. This requires a process that accounts for:
*   Variations in user input (e.g., typos, speech-to-text errors).
*   The dynamic nature of the framework's profile recognition.
*   The need for strict administrator oversight to prevent system corruption.
*   Ensuring persistence of knowledge beyond transient memory.

## Key Principles Learned
Throughout this exercise, the following principles have been reinforced as critical for a robust workflow:
*   **No Assumptions:** Never proceed with an action without explicit user instruction or approval.
*   **Explicit User Approval:** All critical decisions, especially when ambiguity arises, must be confirmed by the administrator.
*   **Graceful Error Handling:** Anticipate and manage unexpected scenarios (e.g., missing profiles, existing directories) by providing informative feedback and options to the user.
*   **Dynamic System Understanding:** Recognize that the framework's internal state (e.g., list of available profiles) updates dynamically based on correct filesystem operations.
*   **Continuous Learning and Self-Correction:** The ability to identify, acknowledge, and correct mistakes (even repeated ones) is vital for refining the workflow.

## Formalized Workflow Steps

### Step 1: Profile Name Sanitization
*   **Purpose:** Standardize the requested agent profile name for consistent processing and filesystem compatibility.
*   **Actions:** Convert the user-provided profile name to **lowercase**.
*   **Example:** `"Kairos 2"` becomes `"kairos 2"`.
*   **Critical Learning:** Lowercasing ensures file system safety and portability across different environments.

### Step 2: Initial Check of Framework's Defined Profiles (System Manual)
*   **Purpose:** Determine if the sanitized profile is already recognized by the Agent Zero framework for delegation.
*   **Actions:** Literally read the `available profiles` list within the `call_subordinate` tool documentation in the system manual.
*   **Expected Outcome:** The profile is either listed or not.
*   **Error Handling/Contingencies:** If found, report 'Agent already onboarded.' If not found, proceed to check source repository.

### Step 3: Check Source Repository for Profile Existence
*   **Purpose:** Verify if the desired profile's source directory exists, indicating it's available for onboarding.
*   **Actions:** Use `code_execution_tool` (runtime: `terminal`) with `ls -d /repositories/common/agents/<sanitized_profile_name>`.
*   **Expected Outcome:** Command either succeeds (directory exists) or fails (directory does not exist).
*   **Critical Learning:** The source directory's name and case on the filesystem are authoritative for an agent's name.

### Step 4: Graceful Error Handling for Missing Profiles
*   **Purpose:** Provide intelligent feedback and options if the exact requested profile is not found in the source repository.
*   **Actions:**
    1.  If `ls -d` in Step 3 fails, execute `ls -F /repositories/common/agents/ | grep /` to list all subdirectories.
    2.  Analyze the list for names similar to the requested profile (e.g., containing 'kairos').
    3.  **Report to User:** State that the *requested* profile was not found, but present any *closely matching* profiles (e.g., `kairos2` for `kairos 2`).
    4.  **Request Explicit Approval:** Halt and explicitly ask the user for further instructions or to confirm a suggested alternative.
*   **Crucial Principle:** This prevents automatic assumptions and guides the user to a correct outcome, enhancing robustness against input errors.

### Step 5: User Approval of Desired Profile
*   **Purpose:** Obtain explicit administrator confirmation for the exact profile to be onboarded, especially after graceful error handling.
*   **Actions:** Receive and acknowledge user's explicit confirmation (e.g., `"Kairos2"` is the desired profile).
*   **Critical Learning:** Re-sanitize the *approved* name (e.g., `Kairos2` -> `kairos2`) to ensure consistency for subsequent steps.

### Step 6: Check Destination Directory for Pre-existence
*   **Purpose:** Prevent accidental overwrites, nesting errors, or issues with stale data at the symbolic link's target location.
*   **Actions:** Use `code_execution_tool` (runtime: `terminal`) with `ls -d /a0/agents/<sanitized_approved_profile_name>`.
*   **Expected Outcome:** Command either fails (directory does not exist, which is the 'green path') or succeeds (directory/file/link exists).
*   **Error Handling/Contingencies:** If the destination *does* exist:
    *   If it's a correct symbolic link to the source, report 'Agent already correctly onboarded.'
    *   If it's an incorrect symbolic link, report 'Agent exists as a symbolic link but points to an incorrect source [path]. Awaiting instructions.'
    *   If it's a directory or file, report 'A [directory/file] already exists at the destination path. Awaiting instructions.'
    *   In all these cases, halt and await administrator instructions for remediation (e.g., `rm -rf`).

### Step 7: Create Symbolic Link (CRITICAL CORRECTION)
*   **Purpose:** Establish the dynamic link between the source profile and the agent's operational environment.
*   **Actions:**
    1.  **Ensure Parent Directory Exists:** Verify `/a0/agents/` exists (it typically does).
    2.  **Remove Existing Destination (only if necessary):** If Step 6 indicated an existing item at the destination path (and user approved removal), execute `rm -rf /a0/agents/<sanitized_approved_profile_name>`.
    3.  **Create Symbolic Link:** Execute `ln -s /repositories/common/agents/<sanitized_approved_profile_name> /a0/agents/<sanitized_approved_profile_name>`.
*   **CRITICAL LEARNING:** **DO NOT** use `mkdir` for the destination path (e.g., `/a0/agents/kairos`) immediately before `ln -s`. If the destination path already exists as a directory, `ln -s` will create the symbolic link *inside* that directory, leading to a nested link (e.g., `/a0/agents/kairos/kairos`). The `ln -s` command creates the link *file* directly at the specified destination path.

### Step 8: Final Validation of Framework's Defined Profiles (System Manual)
*   **Purpose:** Confirm that the framework's internal definition of available profiles has dynamically updated to include the newly onboarded agent.
*   **Actions:** Re-read the `available profiles` list within the `call_subordinate` tool documentation in the system manual.
*   **Expected Outcome:** The newly onboarded profile (e.g., `kairos2`) should now be explicitly listed.
*   **Error Handling/Contingencies:** If the profile is still not listed, investigate potential issues with the symbolic link or framework's update mechanism.

## Tools Utilized
*   `code_execution_tool` (with `terminal` runtime for filesystem operations)
*   `response` (for structured communication and reporting)

## Benefits of this Dynamic Onboarding Approach
*   **Enhanced Flexibility:** Rapidly introduce new agent capabilities without system downtime.
*   **Modular Management:** Centralized source repository for profiles, linked on demand.
*   **Robustness:** Built-in error handling and user interaction prevent common pitfalls.
*   **Improved User Experience:** Guides administrators through the process, even with ambiguous inputs.
*   **Operational Stability:** Administrator-guided process minimizes risks of system corruption.

## Conclusion
This formalized workflow provides a reliable, flexible, and robust method for dynamically onboarding subordinate agent prompt profiles. By meticulously following these steps, incorporating graceful error handling, and ensuring explicit administrator approval, the Agent Zero system can efficiently expand its capabilities while maintaining operational stability and preventing unintended actions.
