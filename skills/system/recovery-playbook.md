# Recovery Playbook

Use this playbook when an install, migration, validation run, adapter rollout, or release task can leave partial state.

## Overview

This recovery playbook provides comprehensive procedures for recovering from failures during system changes. It covers pre-apply preparation, failure detection and response, and post-recovery verification. Following these procedures minimizes downtime, prevents data loss, and ensures system integrity.

## Before Apply

### Pre-Apply Checklist

Complete these steps before applying any system change to production or critical environments.

**1. Run the command in dry-run mode when available.**

Dry-run mode simulates the change without actually modifying the system. It reveals:
- What files will be created, modified, or deleted
- What configuration changes will be applied
- What dependencies will be installed or updated
- What services will be restarted
- Any conflicts or errors that would occur

Dry-run execution:
- Run with identical parameters as planned apply
- Review all planned changes carefully
- Verify targets are expected and correct
- Check for unexpected modifications
- Validate that changes align with intentions
- Document any warnings or anomalies
- Resolve all dry-run failures before proceeding

**2. Confirm the resolved targets are expected for the operating system.**

Different operating systems may resolve paths, dependencies, or configurations differently. Verify:
- Target paths exist and are correct
- File permissions are appropriate
- Dependencies are available for the OS
- Configuration paths are OS-appropriate
- Service names match OS conventions
- User and group IDs are correct
- Path separators are correct (forward vs. backward slash)
- Case sensitivity matches filesystem (Windows vs. Linux)

Platform-specific considerations:
- Windows: Backslash paths, case-insensitive, .exe extensions
- Linux/macOS: Forward slash paths, case-sensitive, no extensions
- macOS: Additional sandboxing and notarization requirements
- Linux distributions: Package manager differences (apt, yum, etc.)

**3. Stage changes into a preview directory when installing for teams or another machine.**

Staging provides a safe environment to:
- Review all changes before deployment
- Test changes in isolation
- Verify compatibility with target systems
- Document changes for review
- Enable rollback if issues are discovered
- Allow team review and approval

Staging process:
- Create isolated staging directory
- Copy or simulate all changes to staging
- Run validation in staging environment
- Perform smoke tests in staging
- Document staging results
- Obtain approvals if required
- Package changes for deployment

**4. Keep backups enabled unless the target is disposable.**

Backups enable recovery if the change causes issues. Backup strategy:
- Create full backup before any modification
- Use timestamp or version in backup names
- Store backups in separate location
- Verify backup integrity after creation
- Define backup retention policy
- Document backup locations
- Test backup restoration periodically

Backup types:
- Full backup: Complete copy of system state
- Incremental backup: Changes since last backup
- Snapshot: Point-in-time system state
- Configuration backup: Only configuration files
- Database backup: Database dumps or snapshots

**5. Use fail-fast mode when partial completion is unacceptable.**

Fail-fast mode stops the operation at the first error, preventing partial state. Use fail-fast when:
- Partial state would leave system inconsistent
- Rollback is complex or risky
- Transaction boundaries cannot be maintained
- Data integrity is critical
- Manual intervention is preferred over automation

Fail-fast configuration:
- Enable fail-fast flag or setting
- Define clear failure criteria
- Document fail-fast behavior
- Provide clear error messages
- Include recovery instructions in error output
- Log failure state for debugging

## During Failure

### Failure Detection

Failures can occur at any point during a change. Detect failures through:

**Automated Detection**
- Exit codes from commands and processes
- Error messages in logs and output
- Health check failures
- Metric thresholds exceeded
- Alert systems triggered

**Manual Detection**
- User reports of issues
- Dashboard monitoring
- Log review
- Performance degradation noticed
- Unexpected behavior observed

### Immediate Response

When a failure is detected:

**1. Stop new writes if the same error repeats.**

Repeating the same failing operation:
- Wastes time and resources
- May worsen the failure state
- Can trigger cascading failures
- May trigger rate limiting or blocking
- Should be avoided until root cause is understood

Stop criteria:
- Same error occurs 3+ times consecutively
- Error indicates systemic issue (not transient)
- Error affects critical functionality
- Error causes data integrity issues
- Error is not in retryable category

Stop actions:
- Halt the current operation
- Do not retry the failed operation
- Document the failure
- Preserve current system state
- Alert appropriate personnel

**2. Record the failing target, file, component, and command.**

Comprehensive failure documentation enables:
- Faster root cause analysis
- Better understanding of failure scope
- More accurate recovery procedures
- Improved future prevention

Record the following:
- Timestamp of failure (with timezone)
- Command or operation that failed
- Full error message and exit code
- Target file, path, or resource
- Component or service affected
- Input parameters and configuration
- System state at time of failure
- Recent changes that might be related
- Steps taken before failure
- User or process that initiated the change

Documentation format:
```
Failure Record
==============
Timestamp: YYYY-MM-DD HH:MM:SS TZ
Operation: [operation name/command]
Target: [file path, URL, resource ID]
Error Code: [exit code or error code]
Error Message: [full error message]
Component: [affected component/service]
Input: [relevant input parameters]
State: [system state at failure]
Context: [recent changes, related events]
Actions Taken: [steps taken before failure]
Initiated By: [user, process, automation]
```

**3. Check whether the operation failed before write, during write, or after write.**

Failure timing determines recovery strategy:

**Before Write**
- No system state was modified
- Safe to retry or abort
- No cleanup required
- Simplest recovery scenario

Indicators:
- Error occurred during validation
- Error occurred during preparation phase
- No files were modified
- No database changes were made
- Error message indicates pre-write failure

**During Write**
- System state is partially modified
- Recovery depends on operation atomicity
- May require cleanup of partial state
- May require verification of system state

Indicators:
- Error occurred mid-operation
- Some files were modified
- Some database changes were made
- Partial output exists
- Error message indicates write failure

**After Write**
- System state is fully modified
- Change completed but may have issues
- May require rollback
- May require validation of written state

Indicators:
- Error occurred after completion
- All expected files were created/modified
- All database changes were applied
- Operation reported completion
- Error is in post-write validation or verification

**4. Inspect the summary counts for failed, skipped, and copied work.**

Summary information provides overview of operation results:

**Summary Components**
- Total items processed
- Successfully completed items
- Failed items with error details
- Skipped items with reasons
- Copied/created items
- Modified items
- Deleted items
- Warning items

**Analysis Steps**
- Compare counts to expected totals
- Identify patterns in failures
- Determine if failures are isolated or systemic
- Check if skipped items are expected
- Verify copied items match expectations
- Look for unexpected modifications
- Identify any missing items

**Decision Points**
- If few failures: Consider targeted fix and retry
- If many failures: Consider full rollback
- If systemic failures: Investigate root cause
- If unexpected modifications: Consider immediate rollback
- If data integrity issues: Consider emergency rollback

**5. Prefer restoring backups over manually reconstructing overwritten files.**

Backup restoration is preferred because:
- Proven recovery method
- Restores exact previous state
- Faster than manual reconstruction
- Less error-prone
- Maintains file metadata and permissions
- Consistent with change management practices

Restoration process:
1. Identify the most recent valid backup
2. Verify backup integrity before restoration
3. Stop any services using the affected resources
4. Restore from backup using appropriate method
5. Verify restoration succeeded
6. Test system functionality after restoration
7. Document restoration action
8. Investigate failure cause before retrying

When manual reconstruction is necessary:
- No valid backup exists
- Backup is corrupted or incomplete
- Only partial backup exists
- Restoration would cause more issues
- Manual reconstruction is faster

If manual reconstruction is necessary:
- Document each reconstruction step
- Verify each reconstructed file
- Test functionality after reconstruction
- Create backup of reconstructed state
- Investigate backup failure

## After Recovery

### Post-Recovery Verification

After recovering from a failure, verify that the system is in a good state.

**1. Re-run validation and plugin checks.**

Validation confirms system integrity:

- Run all validation tests
- Check configuration correctness
- Verify plugin compatibility
- Test all affected functionality
- Verify no corruption exists
- Check for orphaned resources
- Verify permissions and access controls
- Confirm service health

Validation scope:
- Affected components and services
- Related dependencies
- Integration points
- Data integrity
- Configuration consistency
- Security settings

**2. Re-run the dry-run command to confirm no unexpected destinations remain.**

Dry-run verification ensures:
- No partial changes remain
- No unexpected modifications exist
- System is in expected state
- No orphaned temporary files
- No incomplete operations
- No pending changes in progress

Dry-run verification steps:
1. Run dry-run with same parameters as original
2. Verify output shows no pending changes
3. Confirm no unexpected files or modifications
4. Check for temporary files from failed operation
5. Verify no lock files remain
6. Confirm system state matches expectations

**3. Re-run apply mode only after permissions, path conflicts, or manifest errors are fixed.**

Resume apply only when root cause is addressed:

**Permission Issues**
- Verify file and directory permissions
- Check user and group ownership
- Ensure service accounts have required access
- Verify no permission conflicts
- Test write access to target locations

**Path Conflicts**
- Resolve any path conflicts
- Remove or rename conflicting files
- Verify no naming collisions
- Check for case sensitivity issues
- Validate path accessibility

**Manifest Errors**
- Correct manifest syntax errors
- Validate manifest schema
- Verify manifest references are valid
- Test manifest parsing
- Confirm manifest completeness

Resumption criteria:
- All identified issues are resolved
- Root cause is understood and addressed
- Pre-apply checklist is satisfied
- Team approval obtained if required
- Rollback plan is ready

**4. Record the recovery action in release notes or operational evidence.**

Documentation ensures:
- Future teams understand what happened
- Recovery actions are auditable
- Lessons are learned and shared
- Compliance requirements are met
- Post-incident reviews are informed

Documentation content:
- Timestamp of failure and recovery
- Description of failure
- Impact assessment
- Recovery actions taken
- Time to recover
- Root cause (if known)
- Preventive measures planned
- Responsible personnel

Documentation locations:
- Release notes for deployment-related failures
- Operational runbooks for service failures
- Incident management system for major failures
- Change management system for all changes
- Team communication channels

**5. Add a regression check if the failure mode is likely to recur.**

Preventive measures reduce future failures:

**Regression Checks**
- Automated test that reproduces the failure
- Test verifies fix or workaround
- Test runs in CI/CD pipeline
- Test alerts on recurrence
- Test is maintained and updated

**Failure Mode Analysis**
- Identify why the failure occurred
- Determine if it can recur
- Assess recurrence likelihood
- Evaluate impact if it recurs
- Design preventive measures

**Preventive Actions**
- Fix root cause if identified
- Add monitoring for recurrence
- Update procedures to prevent recurrence
- Add safeguards to prevent recurrence
- Improve error handling
- Enhance validation
- Update documentation

## Recovery Scenarios

### Scenario 1: Installation Failure

**Symptoms**
- Package installation fails mid-process
- Dependencies are partially installed
- Configuration files are partially written
- Services fail to start

**Immediate Actions**
1. Stop installation process
2. Record failure details
3. Identify which phase failed
4. Assess partial state
5. Decide on recovery approach

**Recovery Options**
- Rollback: Restore from backup or uninstall partially installed packages
- Resume: Fix issues and continue installation
- Cleanup: Remove partial installation and start fresh

**Post-Recovery**
- Verify all dependencies are correctly installed
- Test all affected functionality
- Document failure and recovery
- Add regression test

### Scenario 2: Configuration Update Failure

**Symptoms**
- Configuration update fails
- Service fails to start with new configuration
- Configuration is partially applied
- Service behavior is inconsistent

**Immediate Actions**
1. Stop configuration change
2. Record error details
3. Identify which configuration failed
4. Check service status
5. Determine if rollback is needed

**Recovery Options**
- Rollback: Restore previous configuration
- Fix: Correct configuration errors and retry
- Partial rollback: Rollback failed components only

**Post-Recovery**
- Verify configuration is correct
- Test all affected functionality
- Validate configuration syntax
- Document failure and recovery

### Scenario 3: Migration Failure

**Symptoms**
- Data migration fails mid-process
- Database is in inconsistent state
- Some data is migrated, some is not
- Application cannot access data

**Immediate Actions**
1. Stop migration process
2. Record migration state
3. Assess data integrity
4. Check for locks or blocking transactions
5. Decide on recovery approach

**Recovery Options**
- Rollback: Restore database from backup
- Resume: Continue from last checkpoint
- Fix: Correct migration script and retry
- Manual: Complete migration manually

**Post-Recovery**
- Verify data integrity
- Run data validation checks
- Test application functionality
- Document migration state and recovery
- Plan for re-migration if needed

### Scenario 4: Deployment Failure

**Symptoms**
- Deployment fails mid-process
- Some services are updated, some are not
- Traffic is routed to incompatible versions
- Health checks are failing

**Immediate Actions**
1. Stop deployment process
2. Record deployment state
3. Identify which components failed
4. Assess system state
5. Determine if rollback is needed

**Recovery Options**
- Rollback: Revert to previous version
- Forward-fix: Fix issues and continue deployment
- Partial rollback: Rollback failed components only
- Blue-green: Switch traffic to previous version

**Post-Recovery**
- Verify all services are healthy
- Test all affected functionality
- Check monitoring and alerting
- Document deployment failure and recovery
- Review deployment process for improvements

### Scenario 5: Validation Run Failure

**Symptoms**
- Validation process fails
- Some validations pass, some fail
- Validation state is inconsistent
- Reports are incomplete or incorrect

**Immediate Actions**
1. Stop validation process
2. Record validation state
3. Identify which validations failed
4. Assess validation results
5. Determine recovery approach

**Recovery Options**
- Retry: Fix issues and rerun validation
- Skip: Skip failed validations and continue
- Partial: Run only failed validations
- Full: Reset and rerun all validations

**Post-Recovery**
- Verify all validations pass
- Generate complete validation report
- Document validation failure and recovery
- Update validation procedures if needed

### Scenario 6: Adapter Rollout Failure

**Symptoms**
- Adapter rollout fails
- Some instances updated, some not
- Adapter compatibility issues discovered
- Service behavior is inconsistent

**Immediate Actions**
1. Stop adapter rollout
2. Record rollout state
3. Identify which instances failed
4. Assess service impact
5. Determine recovery approach

**Recovery Options**
- Rollback: Revert to previous adapter version
- Canary: Pause rollout and assess
- Fix: Address compatibility issues and retry
- Partial: Rollback failed instances only

**Post-Recovery**
- Verify all instances are consistent
- Test all affected functionality
- Monitor for adapter-related issues
- Document rollout failure and recovery
- Review adapter compatibility before retry

### Scenario 7: Release Task Failure

**Symptoms**
- Release process fails
- Some release steps completed, some not
- Release artifacts are incomplete
- Release notes are inaccurate

**Immediate Actions**
1. Stop release process
2. Record release state
3. Identify which steps failed
4. Assess release artifacts
5. Determine recovery approach

**Recovery Options**
- Rollback: Cancel release and revert changes
- Resume: Fix issues and continue release
- Abort: Cancel release and investigate
- Patch: Apply fixes and create new release

**Post-Recovery**
- Verify release is complete and correct
- Test release artifacts
- Validate release notes
- Document release failure and recovery
- Review release process for improvements

## Recovery Decision Tree

Use this decision tree to determine appropriate recovery action:

```
Failure Detected
    |
    v
Is system in safe state? --- No ---> Immediate rollback
    |
    Yes
    |
    v
Is data integrity intact? --- No ---> Immediate rollback
    |
    Yes
    |
    v
Is failure transient? --- Yes ---> Retry with backoff
    |
    No
    |
    v
Can failure be fixed quickly? --- Yes ---> Fix and retry
    |
    No
    |
    v
Is partial state recoverable? --- Yes ---> Attempt recovery
    |
    No
    |
    v
Rollback to last known good state
```

## Recovery Tools and Procedures

### Backup Restoration

**Database Backup Restoration**
1. Stop application services
2. Verify backup integrity
3. Restore database from backup
4. Verify database consistency
5. Run database validation
6. Restart application services
7. Test application functionality
8. Document restoration

**File System Backup Restoration**
1. Stop affected services
2. Create backup of current state (if not corrupted)
3. Restore files from backup
4. Verify file permissions
5. Verify file integrity
6. Restart services
7. Test functionality
8. Document restoration

**Configuration Backup Restoration**
1. Identify configuration backup
2. Verify backup is valid
3. Stop affected services
4. Restore configuration files
5. Validate configuration syntax
6. Restart services
7. Test configuration
8. Document restoration

### State Cleanup

**Partial State Cleanup**
1. Identify partial state components
2. Determine cleanup requirements
3. Create cleanup script or procedure
4. Execute cleanup in safe environment
5. Verify cleanup completed
6. Test system functionality
7. Document cleanup

**Temporary File Cleanup**
1. Identify temporary files
2. Verify they are not needed
3. Remove temporary files
4. Verify removal
5. Check for lock files
6. Document cleanup

**Lock File Cleanup**
1. Identify lock files
2. Verify no processes are using locks
3. Remove lock files
4. Verify system can proceed
5. Test functionality
6. Document cleanup

### Verification Procedures

**System Verification**
1. Verify all services are running
2. Check service health endpoints
3. Verify no error logs
4. Check resource utilization
5. Test critical functionality
6. Verify data integrity
7. Check monitoring and alerting

**Functional Verification**
1. Test all affected features
2. Verify expected behavior
3. Check error handling
4. Test edge cases
5. Verify performance
6. Check user-facing functionality

**Data Verification**
1. Verify data integrity
2. Check data consistency
3. Validate data relationships
4. Verify data completeness
5. Check for data corruption
6. Verify backup integrity

## Recovery Metrics

Track these metrics to measure recovery effectiveness:

**Time to Detect (TTD)**
- Time from failure to detection
- Target: < 5 minutes
- Measurement: Failure timestamp - Detection timestamp

**Time to Acknowledge (TTA)**
- Time from detection to acknowledgment
- Target: < 2 minutes
- Measurement: Acknowledgment timestamp - Detection timestamp

**Time to Recovery (TTR)**
- Time from failure to recovery
- Target: < 30 minutes
- Measurement: Recovery timestamp - Failure timestamp

**Recovery Success Rate**
- Percentage of successful recoveries
- Target: > 95%
- Measurement: Successful recoveries / Total failures

**Rollback Rate**
- Percentage of failures requiring rollback
- Target: < 20%
- Measurement: Rollbacks / Total changes

**Mean Time Between Failures (MTBF)**
- Average time between failures
- Target: Increasing over time
- Measurement: Total time / Number of failures

## Recovery Team and Responsibilities

### Roles

**Incident Commander**
- Coordinates recovery effort
- Makes recovery decisions
- Communicates with stakeholders
- Escalates when necessary

**Technical Lead**
- Executes recovery procedures
- Provides technical expertise
- Implements fixes
- Validates recovery

**Communications Lead**
- Updates stakeholders
- Documents recovery progress
- Manages communication channels
- Coordinates with external teams

**Subject Matter Expert**
- Provides domain expertise
- Advises on recovery options
- Validates recovery correctness
- Identifies potential side effects

### Escalation Matrix

**Level 1: On-Call Engineer**
- First responder
- Initial assessment
- Standard recovery procedures
- Escalation if not resolved in 15 minutes

**Level 2: Technical Lead**
- Complex recovery scenarios
- Escalation from Level 1
- Decision on rollback vs. fix
- Escalation if not resolved in 30 minutes

**Level 3: Engineering Manager**
- Major incidents
- Escalation from Level 2
- Resource allocation
- Customer communication approval
- Escalation if not resolved in 1 hour

**Level 4: VP Engineering**
- Critical system outages
- Major data loss
- Security incidents
- Business continuity issues

## Continuous Improvement

### Post-Recovery Review

After every recovery, conduct a review:

**Review Meeting**
- Within 24 hours of recovery
- Include all involved personnel
- Review timeline of events
- Discuss what went well
- Discuss what could be improved
- Identify action items

**Review Documentation**
- Document review findings
- Track action items
- Assign owners and due dates
- Review action item completion

**Process Updates**
- Update recovery procedures based on lessons learned
- Update runbooks
- Update monitoring and alerting
- Improve automation where possible

### Metrics Review

Review recovery metrics regularly:

**Weekly Review**
- Review all failures from the week
- Identify patterns
- Address immediate issues
- Update risk assessment

**Monthly Review**
- Review recovery metrics trends
- Identify systemic issues
- Plan improvements
- Update procedures

**Quarterly Review**
- Comprehensive review of recovery capability
- Update recovery playbook
- Conduct recovery drills
- Update training materials

## Appendix: Recovery Templates

### Failure Report Template

```
FAILURE REPORT
==============
Report ID: [unique identifier]
Date/Time: YYYY-MM-DD HH:MM:SS TZ
Reporter: [name and contact]
Severity: [P0/P1/P2/P3]

Description:
[Detailed description of failure]

Impact:
[Description of impact on users and systems]

Timeline:
- HH:MM - [event]
- HH:MM - [event]
- HH:MM - [event]

Root Cause:
[Root cause analysis]

Resolution:
[How the failure was resolved]

Preventive Actions:
- [Action 1]
- [Action 2]

Post-Incident Review:
[Date and attendees]

Status: [Open/In Progress/Resolved]
```

### Recovery Checklist Template

```
RECOVERY CHECKLIST
==================
Failure ID: [unique identifier]
Date/Time: YYYY-MM-DD HH:MM:SS TZ
Recovery Lead: [name]

Pre-Recovery
- [ ] Failure documented
- [ ] Impact assessed
- [ ] Recovery approach selected
- [ ] Team notified
- [ ] Stakeholders informed

Recovery Execution
- [ ] Backup verified
- [ ] Services stopped (if required)
- [ ] Recovery action executed
- [ ] Recovery verified
- [ ] Services restarted (if stopped)
- [ ] Functionality tested

Post-Recovery
- [ ] System state verified
- [ ] Monitoring confirmed operational
- [ ] Stakeholders notified of recovery
- [ ] Failure report created
- [ ] Root cause analysis initiated
- [ ] Preventive actions identified

Sign-off: _______________
Date: _______________
```

### Communication Template

```
INCIDENT COMMUNICATION
======================
To: [stakeholders]
From: [communications lead]
Date: YYYY-MM-DD HH:MM TZ
Subject: [Incident title and severity]

Summary:
[Brief description of incident]

Impact:
[Description of impact on users]

Current Status:
[Current status and ETA for resolution]

Next Update:
[When next update will be provided]

Contact:
[Contact information for questions]
```

## Appendix: Emergency Contacts

Maintain up-to-date emergency contact information:

- On-call rotation schedule
- Escalation contact list
- Vendor support contacts
- Infrastructure provider contacts
- Security team contacts
- Communications team contacts
- Legal/compliance contacts

## Appendix: Recovery Resources

Maintain readily available recovery resources:

- Backup storage locations and access procedures
- Recovery scripts and automation
- Runbooks and procedures
- System documentation
- Configuration backups
- Infrastructure diagrams
- Dependency maps
- Contact information

## Appendix: Recovery Drills

Conduct regular recovery drills:

**Monthly Drills**
- Single component failure
- Standard recovery procedures
- Team familiarization

**Quarterly Drills**
- Multi-component failure
- Complex recovery scenarios
- Cross-team coordination

**Annual Drills**
- Major incident simulation
- Full disaster recovery
- Business continuity testing

Drill documentation:
- Drill scenario and objectives
- Drill execution timeline
- Issues encountered
- Lessons learned
- Action items for improvement
