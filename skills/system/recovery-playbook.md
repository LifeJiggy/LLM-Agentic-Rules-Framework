# Recovery Playbook

Use this playbook when an install, migration, validation run, adapter rollout, or release task can leave partial state.

## Before Apply

1. Run the command in dry-run mode when available.
2. Confirm the resolved targets are expected for the operating system.
3. Stage changes into a preview directory when installing for teams or another machine.
4. Keep backups enabled unless the target is disposable.
5. Use fail-fast mode when partial completion is unacceptable.

## During Failure

1. Stop new writes if the same error repeats.
2. Record the failing target, file, component, and command.
3. Check whether the operation failed before write, during write, or after write.
4. Inspect the summary counts for failed, skipped, and copied work.
5. Prefer restoring backups over manually reconstructing overwritten files.

## After Recovery

1. Re-run validation and plugin checks.
2. Re-run the dry-run command to confirm no unexpected destinations remain.
3. Re-run apply mode only after permissions, path conflicts, or manifest errors are fixed.
4. Record the recovery action in release notes or operational evidence.
5. Add a regression check if the failure mode is likely to recur.

