#!/usr/bin/env python3
"""Fetch paired source dependencies and build Everest plus its standard installer."""
import argparse, json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'eng/horizon'))
from support import digest, read_mirrors, run, submodules
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--output', type=Path, default=ROOT / 'artifacts/horizon')
p.add_argument('--dotnet', default='dotnet')
p.add_argument('--source-mirrors', type=Path)
p.add_argument('--fetch-only', action='store_true')
a = p.parse_args()
submodules(ROOT, read_mirrors(a.source_mirrors))
if a.fetch_only: sys.exit(0)
out = a.output.resolve()
for project, folder in [('Celeste.Mod.mm', 'everest'), ('MiniInstaller', 'installer')]:
    run([a.dotnet, 'publish', ROOT / project / (project + '.csproj'), '-c', 'Release',
         '-o', out / folder, '-p:ArtifactsPath=' + str(out / 'build'),
         '-p:RoslynVersion=5.0.0', '-p:MMUseSdkCompiler=true', '-p:UseSharedCompilation=false',
         '-p:NuGetLockFilePath=packages.horizon.lock.json'], cwd=ROOT)
(out / 'manifest.json').write_text(json.dumps({'revision': subprocess.check_output(['git', '-C', ROOT, 'rev-parse', 'HEAD'], text=True).strip(),
    'sdk': subprocess.check_output([a.dotnet, '--version'], cwd=ROOT, text=True).strip(),
    'files': {str(f.relative_to(out)): digest(f) for folder in ['everest', 'installer'] for f in (out / folder).rglob('*') if f.is_file()}}, indent=2) + '\n')
print(out)
