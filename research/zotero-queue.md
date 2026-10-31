# Adding new sources to Zotero

1. Save the PDF into `research/pdfs/` (any file name) and tell Claude.
2. Claude renames it, reads it, and adds an entry to `research/zotero-queue.json`.
3. In Zotero: **Tools → Developer → Run JavaScript**, tick **Run as async function**,
   paste this one line and click **Run**:

```js
return await new (Object.getPrototypeOf(async function(){}).constructor)(await IOUtils.readUTF8('C:\\Users\\ishan\\Documents\\ELL305-Term-Paper\\scripts\\zotero-import.js'))();
```

The result box lists what was added. Better BibTeX updates `references/references.bib`
within a few seconds. Running it again is harmless: imported entries are skipped.
