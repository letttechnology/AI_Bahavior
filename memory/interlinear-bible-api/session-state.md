# Session State — 2026-05-30

## Done
- Fixed grep tool: installed ripgrep 15.1.0 via winget (attempted fix; actual root cause was different)
- Root cause analysis on grep/glob tool failures: both tools invoke a bundled `rg` internally; when `path` is omitted or set to `D:\`, rg scans the drive root and hits protected Windows system dirs ($RECYCLE.BIN, System Volume Information) → access denied on stderr → tool parser fails with "invalid ripgrep output"
- Added "Root cause analysis" as a core value in `.opencode/memory.md`
- Updated `preferences.md` Rule 3 (grep fix documented)
- Updated `.opencode/memory.md` with correct memory location path and proper glob/grep usage
- Reviewed TSR status: still at step 1 (build POST /admin/import-sense-selections endpoint)
- **FIXED** glob/grep access denied errors: Created `D:\.rgignore` excluding `$RECYCLE.BIN/` and `System Volume Information/`. Bundled rg honors `.rgignore` and skips these directories during walk, avoiding access denied errors entirely.
