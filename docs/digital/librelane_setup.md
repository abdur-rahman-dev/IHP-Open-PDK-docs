# LibreLane Setup Guide

This guide will help you set up LibreLane with the IHP SG13G2 PDK. It covers installation prerequisites, PDK configuration, and verification steps necessary before starting the [LibreLane tutorial](librelane.md).

## Prerequisites

Before installing LibreLane, ensure your system meets the following requirements:

### System Requirements

- **Operating System:** Linux (Ubuntu 24.04 recommended, also works on Ubuntu 22.04+)
- **Disk Space:** At least 10 GB free for PDK and tools
- **RAM:** Minimum 8 GB (16 GB recommended for larger designs)
- **Internet Connection:** Required for downloading packages and PDK

### Required Software

- **Git:** Version control for cloning repositories
- **Nix:** Package manager for reproducible tool environments (recommended method)
  - See [Nix Setup Guide](../install/nix_setup.md) for installation instructions

## Installation Methods

LibreLane can be installed through several methods. The recommended approach is using Nix, which provides reproducible environments with all necessary tools.

### Method 1: Nix Installation (Recommended)

Nix installation provides the most reliable and reproducible setup. See the full [Nix Setup Guide](../install/nix_setup.md) for detailed instructions.

**Quick Start with Nix:**

1. Install Nix (if not already installed):
   ```bash
   sh <(curl -L https://nixos.org/nix/install) --daemon
   ```

2. Enable flakes (required for modern Nix):
   ```bash
   mkdir -p ~/.config/nix
   echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
   ```

3. Enter LibreLane development environment:
   ```bash
   nix run github:librelane/librelane/dev -- --help
   ```

This will download and cache all necessary tools. **The first run may take 30-60 minutes** as Nix downloads and builds the entire EDA toolchain (OpenROAD, Yosys, Magic, KLayout, Verilator, and dependencies). Subsequent runs will use the cached environment and start instantly.

### Method 2: Alternative Installation Methods

For non-Nix installations, consult the [LibreLane documentation](https://librelane.readthedocs.io/). These methods require manual installation of all EDA tools (Yosys, OpenROAD, Magic, KLayout, Netgen) and may have version compatibility issues.

## PDK Configuration

LibreLane needs access to the IHP SG13G2 PDK. There are two approaches: automatic management via Ciel, or manual PDK installation.

### Automatic PDK Management (Default)

By default, LibreLane uses [Ciel](https://github.com/fossi-foundation/ciel) to automatically manage PDK downloads and versions.

When you run:
```bash
librelane --pdk ihp-sg13g2 config.yaml
```

LibreLane will:
1. Check if `ihp-sg13g2` is available locally
2. Download it automatically if missing (first run only)
3. Store it in `~/.ciel/` by default
4. Use the version specified in LibreLane's configuration

**Advantages:**
- No manual setup required
- Automatic version management
- Consistent across different machines

**First-Run Behavior:**
The first time you specify `--pdk ihp-sg13g2`, you will see:
```
Version cb7daaa8... not found locally, attempting to download...
Downloading sg13g2_stdcell.tar.zst... 100%
```

This is normal. Subsequent runs will use the cached PDK.

### Manual PDK Installation

For development, testing, offline use, or when you need the latest PDK updates (Ciel may use older versions), you may want to manually install the PDK.

**Step 1: Clone the PDK Repository**

```bash
cd ~/git  # Or your preferred location
git clone https://github.com/IHP-GmbH/IHP-Open-PDK.git
cd IHP-Open-PDK
```

**Step 2: Checkout Recommended Version**

```bash
# Use the latest from dev branch (recommended)
git checkout dev

# Or a specific commit for reproducibility
git checkout cb716cc8291193fb63ef16c94c9e12526f9221be
```

**Step 3: Set Environment Variables**

```bash
export PDK_ROOT="$HOME/git/IHP-Open-PDK"
export PDK="ihp-sg13g2"
export STD_CELL_LIBRARY="sg13g2_stdcell"
```

Add these to your `~/.bashrc` or `~/.zshrc` to make them permanent.

**Step 4: Use Manual PDK with LibreLane**

```bash
librelane --pdk ihp-sg13g2 --pdk-root $PDK_ROOT --manual-pdk config.yaml
```

The `--manual-pdk` flag tells LibreLane to use your environment variables instead of Ciel.

## PDK Structure Overview

Understanding the PDK structure helps when troubleshooting or customizing your flow.

```
IHP-Open-PDK/
└── ihp-sg13g2/
    ├── libs.ref/              # Reference libraries
    │   ├── sg13g2_stdcell/    # Standard cell library (digital gates)
    │   ├── sg13g2_io/         # I/O pad cells
    │   └── sg13g2_sram/       # SRAM macros
    └── libs.tech/             # Tool-specific configurations
        ├── librelane/         # LibreLane configuration files
        ├── klayout/           # KLayout technology and DRC/LVS
        ├── magic/             # Magic technology files
        └── openroad/          # OpenROAD configuration
```

**Key Directories for LibreLane:**

- `libs.ref/sg13g2_stdcell/`: Contains 84 standard cells
  - `lef/`: Physical abstracts for placement
  - `lib/`: Timing libraries (typical, fast, slow corners)
  - `gds/`: Full layouts for verification
  - `verilog/`: Behavioral models for simulation

- `libs.tech/librelane/`: LibreLane-specific configuration
  - `config.tcl`: Main PDK configuration for LibreLane
  - `sg13g2_stdcell/`: Library-specific settings

## Environment Variables

LibreLane uses several environment variables for PDK location and configuration:

| Variable | Purpose | Example |
|----------|---------|---------|
| `PDK_ROOT` | Root directory of PDK installation | `/home/user/git/IHP-Open-PDK` |
| `PDK` | PDK variant to use | `ihp-sg13g2` |
| `STD_CELL_LIBRARY` | Standard cell library name | `sg13g2_stdcell` |

**When Using Automatic PDK Management (Default):**
- You do not need to set these variables
- LibreLane manages them internally via Ciel

**When Using Manual PDK Installation:**
- Set all three variables before running LibreLane
- Use `--manual-pdk` flag to enable manual mode
- Alternatively, use `--pdk-root` flag to specify PDK location directly

**Example Setup Script:**
```bash
#!/bin/bash
# setup_ihp.sh - Set IHP PDK environment

export PDK_ROOT="$HOME/git/IHP-Open-PDK"
export PDK="ihp-sg13g2"
export STD_CELL_LIBRARY="sg13g2_stdcell"

echo "IHP SG13G2 PDK environment configured"
echo "PDK_ROOT: $PDK_ROOT"
```

Source this script before running LibreLane:
```bash
source setup_ihp.sh
librelane --pdk ihp-sg13g2 --manual-pdk config.yaml
```

## Verification

After setup, verify your installation before proceeding to the tutorial.

### Verify LibreLane Installation

```bash
# Check LibreLane is accessible
librelane --version

# Expected output:
# LibreLane vX.X.X
```

### Verify EDA Tools

If using Nix, verify tools are available in the development shell:

```bash
nix develop github:librelane/librelane/dev --command bash -c "yosys --version | head -3"
nix develop github:librelane/librelane/dev --command bash -c "openroad -version"
nix develop github:librelane/librelane/dev --command bash -c "klayout -v"
```

### Verify PDK Access

**For Automatic PDK (Ciel):**

Run a test command - Ciel will download the PDK if needed:
```bash
librelane --pdk ihp-sg13g2 --smoke-test
```

**For Manual PDK:**

Check the PDK structure:
```bash
# Verify PDK_ROOT is set
echo $PDK_ROOT

# Check standard cell library exists
ls $PDK_ROOT/ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/

# Expected output should include:
# sg13g2_stdcell.lef
# sg13g2_tech.lef
```

Verify the standard cell count:
```bash
wc -l $PDK_ROOT/ihp-sg13g2/libs.ref/sg13g2_stdcell/doc/sg13g2_stdcell.celllist

# Expected output: 84 cells
```

Check LibreLane configuration exists:
```bash
ls $PDK_ROOT/ihp-sg13g2/libs.tech/librelane/

# Expected output should include:
# config.tcl
# sg13g2_stdcell/
```

### Verification Checklist

Before proceeding to the LibreLane tutorial, confirm:

- [ ] LibreLane command is accessible (`librelane --version` works)
- [ ] Either:
  - [ ] Ciel automatic PDK download works (default), OR
  - [ ] Manual PDK is cloned and variables are set
- [ ] Standard cell library contains 84 cells
- [ ] LibreLane configuration files exist in `libs.tech/librelane/`
- [ ] Nix development environment works (if using Nix)

## Troubleshooting

### LibreLane Command Not Found

**Symptom:** `bash: librelane: command not found`

**Solutions:**
- If using Nix, ensure you're in the development shell:
  ```bash
  nix develop github:librelane/librelane/dev
  ```
- If using system installation, check your PATH includes LibreLane location
- Verify LibreLane was installed successfully

### PDK Not Found

**Symptom:** `Error: PDK 'ihp-sg13g2' not found`

**Solutions:**
- **For automatic mode:** Check internet connection, Ciel should download automatically
- **For manual mode:**
  - Verify `PDK_ROOT` is set: `echo $PDK_ROOT`
  - Check PDK exists: `ls $PDK_ROOT/ihp-sg13g2/`
  - Use `--manual-pdk` flag when running LibreLane
  - Use `--pdk-root` flag to specify location explicitly

### Wrong PDK Version

**Symptom:** Tool errors or missing files during flow execution

**Solutions:**
- For automatic mode: LibreLane manages versions automatically
- For manual mode: Checkout the recommended commit:
  ```bash
  cd $PDK_ROOT
  git fetch
  git checkout dev  # or specific commit hash
  ```

### Nix Build Takes Too Long

**Symptom:** First Nix run appears stuck for an extended period

**Solution:** This is normal behavior for first-time downloads. Nix is downloading several GB of EDA tools. Progress may not always be visible. Wait for completion - subsequent runs will be much faster.

### Missing Standard Cells

**Symptom:** Synthesis fails with "cell not found" errors

**Solutions:**
- Verify standard cell library path:
  ```bash
  ls $PDK_ROOT/ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/
  ```
- Should contain `.lib` timing files
- Re-download PDK if files are missing

## Next Steps

Once verification is complete, proceed to:

- **[LibreLane Tutorial](librelane.md):** Learn to implement a simple counter design
- **[Full Chip Design](librelane_full_chip.md):** Advanced full-chip flows with pad rings

## Additional Resources

- [LibreLane Documentation](https://librelane.readthedocs.io/): Complete LibreLane reference
- [LibreLane Repository](https://github.com/librelane/librelane): Source code and examples
- [IHP SG13G2 PDK](https://github.com/IHP-GmbH/IHP-Open-PDK): PDK source and documentation
- [Nix Setup Guide](../install/nix_setup.md): Detailed Nix installation and usage
- [Ciel PDK Manager](https://github.com/fossi-foundation/ciel): PDK version management tool

## Getting Help

If you encounter issues not covered in this guide:

1. Check the [LibreLane documentation troubleshooting section](https://librelane.readthedocs.io/)
2. Review [IHP-Open-PDK issues](https://github.com/IHP-GmbH/IHP-Open-PDK/issues)
3. Ask in relevant community forums or contact IHP support

Ensure you have completed all verification steps above before seeking help, and provide:
- LibreLane version (`librelane --version`)
- PDK location and version (commit hash)
- Operating system and Nix version (if applicable)
- Complete error messages and logs
