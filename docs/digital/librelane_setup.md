# LibreLane Setup Guide

This guide helps you set up LibreLane for use with the IHP SG13G2 PDK. For complete installation instructions, see the [official LibreLane documentation](https://librelane.readthedocs.io/).

## Prerequisites

Before starting, install LibreLane following the [Nix installation guide for Linux](https://librelane.readthedocs.io/en/latest/installation/nix_installation/installation_linux.html).

**Important:** The official guide uses the Determinate Systems Nix installer which automatically configures the FOSSi Foundation binary cache for faster downloads.

## Quick Start

After installing LibreLane, verify the installation:

```bash
cd /path/to/librelane
nix-shell
librelane --smoke-test
```

If successful, you're ready to use LibreLane with IHP SG13G2.

## PDK Configuration

LibreLane can manage the IHP SG13G2 PDK automatically or use a manual installation.

### Automatic PDK Management (Recommended)

LibreLane uses [Ciel](https://github.com/fossi-foundation/ciel) to automatically download and manage PDK versions:

```bash
librelane --pdk ihp-sg13g2 config.yaml
```

On first run, LibreLane will download the IHP SG13G2 PDK automatically (may take 10-15 minutes). Subsequent runs use the cached version stored in `~/.ciel/`.

### Manual PDK Installation (Optional)

For offline use, development, or testing with the latest PDK version, see the [IHP PDK installation guide](https://ihp-open-pdk-docs.readthedocs.io/en/latest/install/installation.html).

**Clone the PDK:**
```bash
git clone --branch dev --recurse-submodules https://github.com/IHP-GmbH/IHP-Open-PDK.git
cd IHP-Open-PDK
```

**Note:** The `--recurse-submodules` option is required to populate submodules included in the PDK repository. The `dev` branch contains the latest changes and is ahead of `main`.

**Use with LibreLane:**
```bash
# Assuming you are inside the IHP-Open-PDK directory
export PDK_ROOT="$(pwd)"
librelane --pdk ihp-sg13g2 --pdk-root $PDK_ROOT --manual-pdk config.yaml
```

## Next Steps

Continue with the [LibreLane tutorial](librelane.md) to implement your first design with IHP SG13G2.

## Additional Resources

- [LibreLane Documentation](https://librelane.readthedocs.io/)
- [LibreLane GitHub](https://github.com/librelane/librelane)
- [IHP-Open-PDK](https://github.com/IHP-GmbH/IHP-Open-PDK)
