# Media preservation

The private GitHub repository preserves the complete durable genealogy
workspace. Binary source artifacts under `genealogy/media/` and retained final
PDF editions use Git LFS. Transient downloads, authenticated-session state,
crops, and rendered review pages under `tmp/` and generated output directories
are excluded.

`genealogy/media-manifest.json` is the canonical machine-readable inventory of
retained media. Every entry records the repository path, byte size, SHA-256,
filename-derived citation identity, located citation and source records, and a
truthful provenance level:

- `exact`: a citation record names the individual file and contains its exact
  SHA-256;
- `source-scoped`: the file belongs to a citation and source context, but the
  older record does not name and checksum that individual batch member;
- `citation-scoped`: a citation record exists but no structured source record
  was located;
- `unlinked`: no citation record can currently be connected to the file.

The manifest does not upgrade historical evidence or invent missing metadata.
It gives every retained artifact an exact integrity identity while keeping
older provenance gaps visible for later repair.

Regenerate and verify it with:

```sh
node scripts/media-manifest.mjs --write
node scripts/media-manifest.mjs --check
```

A clean clone requires Git LFS to materialize the binary evidence archive:

```sh
git lfs install
git lfs pull
node scripts/media-manifest.mjs --check
node scripts/validate-genealogy.mjs
```

The repository is private because its research memory includes minimized
information about living people and family-supplied evidence even though most
archival images come from openly accessible public records.
