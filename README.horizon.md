# Everest for Horizon

This fork supplies the patcher/mod loader for
[Celeste-Switch](https://github.com/pixelomer/Celeste-Switch), using
[Horizon CoreCLR .NET 10](https://github.com/pixelomer/dotnet-runtime).
Everest and its managed dependencies target net8.0. The host provides the
matching .NET 10 framework and runtime hooks; no runtime backport is needed for
this pinned configuration.

## Build

On Linux x86-64 with Python 3.12+, Git and .NET SDK 10.0.1xx:

```sh
python3 build-horizon.py
```

The script fetches exact submodule commits, including
[pixelomer/MonoMod](https://github.com/pixelomer/MonoMod), then publishes Release
outputs to `artifacts/horizon/everest/` and `artifacts/horizon/installer/`.
`--output PATH` selects another build directory; `--fetch-only` fetches source.
`--source-mirrors JSON` maps canonical URLs to Git source mirrors, without
replacing dependencies with prebuilt binaries. NuGet dependencies are restored
through the upstream project graph with separate Horizon restore locks.

The build uses upstream's already stripped references in `lib-stripped`.
Never commit original game assemblies in their place. The pinned `lib-ext`
submodule supplies desktop installer support; its desktop native libraries are
not Switch libraries. The Celeste-Switch preparation tool runs MiniInstaller
against a user-owned PC copy and paired source-built FNA. Mods are loaded
normally from the SD card's `Mods/` folder.

## Compatibility and provenance

The upstream MIT license and dependency notices remain intact. NLua and lib-ext
retain their upstream pins; this repository contains no Nintendo SDK input.
Changes cover the Horizon external-autosplitter boundary, current MonoMod legacy
trampolines and additive lazy-texture-loading events. Actual PC game inputs and
native FMOD libraries belong to
the user's local installation, not this source repository.

Desktop Discord integration, filesystem watchers, external process helpers and
the external autosplitter are unavailable on Horizon.
Use the pinned dependency set from Celeste-Switch to keep the loader, framework,
and runtime interfaces compatible.
