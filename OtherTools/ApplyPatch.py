"""Apply an upgrade patch once, preserving rejects and a manual progress checklist."""
import argparse
import hashlib
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', default='../MooaToon-Engine')
    parser.add_argument('--epic-remote', default='epic')
    parser.add_argument('--target-branch', default='5.8')
    parser.add_argument('--patch', default='diff.patch')
    parser.add_argument('--inventory-only', action='store_true', help='Rebuild an untouched checklist from the existing log; never reapply.')
    args = parser.parse_args()
    repo = (Path(__file__).resolve().parent / args.repository).resolve()

    def git(*arguments, check=True):
        result = subprocess.run(['git', '-C', str(repo), *arguments], capture_output=True)
        if check and result.returncode:
            raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
        return result

    repo = Path(git('rev-parse', '--show-toplevel').stdout.decode().strip())
    patch = (repo / args.patch).resolve()
    report = repo / 'PatchConflicts.md'
    log = repo / 'ApplyPatch.log'
    fallback_dir = repo / 'PatchConflicts'
    if not args.inventory_only and (report.exists() or log.exists() or fallback_dir.exists()):
        raise RuntimeError('Previous apply artifacts exist; preserve/review them before another application.')
    if args.inventory_only and report.exists() and '- [x]' in report.read_text(encoding='utf-8').lower():
        raise RuntimeError('Checklist has completed entries; preserve progress instead of rebuilding it.')
    target = f'refs/remotes/{args.epic_remote}/{args.target_branch}'
    head = git('rev-parse', 'HEAD').stdout.decode().strip()
    if head != git('rev-parse', '--verify', target).stdout.decode().strip():
        raise RuntimeError(f'HEAD must equal {target}. This script does not switch branches.')
    status = git('status', '--porcelain', '--untracked-files=all').stdout
    # The input patch may be untracked after switching from the custom branch.
    relative_patch = patch.relative_to(repo).as_posix() if patch.is_relative_to(repo) else None
    allowed = f'?? {relative_patch}'.encode() if relative_patch else None
    dirty = [line for line in status.splitlines() if line != allowed]
    if dirty and not args.inventory_only:
        raise RuntimeError('Working tree is not clean:\n' + b'\n'.join(dirty).decode(errors='replace'))
    data = patch.read_bytes()
    if not data:
        raise RuntimeError('Patch is empty.')
    git('apply', '--stat', str(patch))  # Validate patch syntax before mutation.
    if args.inventory_only:
        output = log.read_bytes()
        previous = report.read_text(encoding='utf-8')
        exit_code = int(re.search(r'Git apply exit code: (\d+)', previous).group(1))
        if hashlib.sha256(data).hexdigest() not in previous or head not in previous:
            raise RuntimeError('Patch or target differs from the previous application.')
    else:
        existing = git('ls-files', '--others', '--ignored', '--exclude-standard', '--', '*.rej').stdout.splitlines()
        if existing:
            raise RuntimeError('Existing ignored .rej files found; review them before applying.')
        print(f'Applying {patch} to {target} ({head})', flush=True)
        result = git('apply', '--reject', '--binary', '--whitespace=nowarn', str(patch), check=False)
        exit_code = result.returncode
        output = result.stdout + result.stderr
        log.write_bytes(output)
    decoded = output.decode('utf-8', errors='replace')
    # Git can fail a whole file (e.g. missing file or binary mismatch) without a .rej.
    # Preserve those full diff blocks separately, in addition to normal hunk rejects.
    blocks = re.split(br'(?=^diff --git )', data, flags=re.MULTILINE)
    entries = []
    covered_errors = set()
    errors = [line for line in decoded.splitlines() if line.startswith('error:') and line != 'error: while searching for:']
    for block in blocks:
        if not block.startswith(b'diff --git '):
            continue
        parsed = subprocess.run(['git', 'apply', '--numstat', '-z', '-'], input=block, capture_output=True)
        if parsed.returncode or not parsed.stdout:
            raise RuntimeError(f'Cannot inventory a patch block; inspect {log} before continuing.')
        path = parsed.stdout.rstrip(b'\0').split(b'\t', 2)[2].decode('utf-8')
        source = (repo / path).resolve()
        if not source.is_relative_to(repo):
            raise RuntimeError(f'Patch path escapes repository: {path}')
        reject = Path(str(source) + '.rej')
        file_errors = [e for e in errors if path in e]
        if reject.exists():
            entries.append((reject.relative_to(repo).as_posix(), 'rejected hunks'))
            covered_errors.update(file_errors)
        elif file_errors:
            fallback_dir.mkdir(exist_ok=True)
            artifact = fallback_dir / f'{len(entries) + 1:04d}.patch'
            artifact.write_bytes(block)
            entries.append((artifact.relative_to(repo).as_posix(), f'whole-file failure: {path}'))
            covered_errors.update(file_errors)
    unclassified = [e for e in errors if e not in covered_errors]
    unexpected = exit_code not in (0, 1) or bool(unclassified) or (exit_code != 0 and not entries)
    lines = [
        '# Patch conflict progress', '',
        f'- Applied at: {re.search(r"Applied at: (.+)", previous).group(1) if args.inventory_only else datetime.now(timezone.utc).isoformat()}',
        f'- Target: `{target}`', f'- Target commit: `{head}`',
        f'- Input patch: `{patch.name}`',
        f'- SHA256: `{hashlib.sha256(data).hexdigest()}`',
        f'- Git apply exit code: {exit_code}',
        f'- Conflict files: {len(entries)}',
        '- Log: [ApplyPatch.log](ApplyPatch.log)', '',
        'Mark `[x]` only after manually resolving and verifying every rejected hunk in that file.',
        'Keep completed entries as history; deleting a reject alone does not prove completion.', '',
    ]
    lines += [f'- [ ] [{path}]({path}) - {kind}' for path, kind in entries]
    if unexpected:
        lines += ['', '- [ ] [ApplyPatch.log](ApplyPatch.log) - investigate unclassified apply failure']
        lines += [f'    {e}' for e in unclassified]
    if not entries and not unexpected:
        lines += ['No conflicts reported.']
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Git apply exit code: {exit_code}; conflict files: {len(entries)}')
    print(f'Progress: {report}\nLog: {log}')
    if unexpected:
        raise RuntimeError('Unclassified apply failure; see progress list and log. Do not reapply.')
    # Expected rejects are a completed inventory operation, not a completed merge.
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as error:
        print(f'ERROR: {error}')
        raise SystemExit(1)
