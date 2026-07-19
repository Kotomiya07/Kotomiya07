# Regenerating the Profile README

This profile is generated from [Profile Control Plane](https://github.com/majiayu000/profile-control-plane) and [`profile.yaml`](profile.yaml). The generator and its dependencies are pinned by a full commit SHA and the upstream `package-lock.json`.

## Requirements

- Node.js 20 or later
- npm

On this Mac, use the Node.js environment provided by Nix.

## Generation Steps

```bash
git clone https://github.com/majiayu000/profile-control-plane.git ../profile-control-plane
git -C ../profile-control-plane checkout a1185c74ac8d973d51c86989c3fd438531ca0009
npm ci --prefix ../profile-control-plane --no-audit --no-fund
npm run --prefix ../profile-control-plane build

node ../profile-control-plane/dist/cli.js check --config profile.yaml --online
node ../profile-control-plane/dist/cli.js build --config profile.yaml --out .profile-output --force
python3 scripts/apply-dark-theme-colors.py .profile-output/assets
cp .profile-output/README.md README.md
cp .profile-output/assets/*.svg assets/
```

Do not edit the generated `README.md` or `assets/*.svg` directly. Update `profile.yaml` and regenerate them whenever the displayed content changes. The post-processing step gives small accent text in the dark-theme SVGs sufficient contrast while preserving the darker accents used by the light-theme SVGs.

## Verification Checklist

- Confirm that all content is readable in both dark and light themes
- Confirm that a 390px viewport has no horizontal overflow
- Confirm that animations stop when `prefers-reduced-motion` is enabled
- Confirm that the featured repositories match the current GitHub pinned repositories
- Confirm that `git diff --check` succeeds
