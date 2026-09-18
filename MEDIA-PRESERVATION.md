# Media preservation

Git preserves the durable code, source documents, exact import baseline,
migration decisions, operations and journal. Binary source media use Git LFS
according to `.gitattributes`. A local commit is not an external backup:
remote Git and LFS availability must be checked separately when a push or
external recovery is authorized. See the [reconstruction record](genealogy2/docs/reconstruction.md)
for the actual verification scope; a complete fresh-clone rebuild is not yet proved.

## Frozen evidence archive

`genealogy/` is frozen after the verified Genealogy2 cutover. Its media remain
at their existing paths and are still used directly. The frozen
`genealogy/media-manifest.json` inventories the retained legacy media with
path, byte size, SHA-256, citation/source references and provenance level:

- `exact`: the citation names and checksums the individual file;
- `source-scoped`: the file belongs to a citation/source context, but the
  older record does not name and checksum that individual batch member;
- `citation-scoped`: a citation exists but no structured source record was located;
- `unlinked`: no citation record can currently be connected to the file.

The manifest preserves historical provenance gaps; it never upgrades evidence.
Verify it with `node scripts/media-manifest.mjs --check`. Do not regenerate it
or add files under genealogy. Later provenance corrections belong in Genealogy2.
The import manifest also covers other retained artifacts outside genealogy/media.

## New source media

Register new originals through `stage-media` and `apply`, with source provenance
and links to the correct source record, according to the [working guide](genealogy2/docs/working.md).
Their hash-addressed bytes live under `genealogy2/media/objects/`; the native
asset registry and revisions describe their provenance. These extensionless
objects use Git LFS too. Do not add them to the frozen legacy manifest.

`stage-media` prepares a file; it does not alone register a successful research
operation or preserve it remotely. Keep the accepted operation, durable journal
receipt and referenced original together. `verify-assets` checks the actual
bytes of both old and registered new assets; an LFS pointer is not an original.
A new Git LFS rule does not upload anything or rewrite earlier history.

## Checks and recovery

A clone needs Git LFS to materialize the original media:

```sh
git lfs install
git lfs pull
node scripts/media-manifest.mjs --check
node scripts/validate-genealogy.mjs
```

Those archive checks alone do not verify the current database. With a restored
or rebuilt Genealogy2 database, also run:

```sh
node genealogy2/cli.mjs verify
node genealogy2/cli.mjs verify-source
node genealogy2/cli.mjs verify-assets
```

Follow [database recovery](genealogy2/README.md#backup-och-återställning) for
`backup-bundle`, restoration, later journal replay and later media. The ignored
SQLite file and temporary verification copies are not Git backups. Operations
and journal do not contain the image bytes. Split dumps and restic remain parked;
they are not routine commands or prerequisites for research.

Retained final PDF editions also use LFS. Temporary downloads, crops, review
renders and authenticated-session state are excluded. A crop or montage must
not replace the retained full original.

The owner made the repository public on 2026-09-04 (PCD-2026-09-04-007).
Publication and push still require their own mandate. Minimize living-person
data and never retain credentials, authenticated-session state or unrestricted
private source material. Existing source evidence and its provenance remain intact.
