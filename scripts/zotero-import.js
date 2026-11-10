// ELL305: import queued PDFs from research/pdfs/ into Zotero, one parent item each,
// added to the "ELL305 Term Paper" collection. Better BibTeX then exports them to
// references/references.bib automatically.
//
// Queue: research/zotero-queue.json. Entries with
// "status": "imported" are skipped; an entry whose URL is already in the library
// is marked imported without creating a duplicate. The script writes the results
// (status, Zotero key) back into the queue file.
//
// Run from Zotero: Tools > Developer > Run JavaScript, tick "Run as async function",
// paste the one-line loader from research/zotero-queue.md, click Run.

const project = 'C:\\Users\\ishan\\Documents\\ELL305-Term-Paper\\';
const pdfDir = project + 'research\\pdfs\\';
const queuePath = project + 'research\\zotero-queue.json';
const lib = Zotero.Libraries.userLibraryID;
const coll = Zotero.Collections.getByLibrary(lib).find(c => c.name === 'ELL305 Term Paper');
if (!coll) return 'Stopped: collection "ELL305 Term Paper" not found.';

const queue = JSON.parse(await IOUtils.readUTF8(queuePath));
const items = await Zotero.Items.getAll(lib, true);
const knownUrls = new Set(items.filter(i => i.isRegularItem()).map(i => i.getField('url')).filter(Boolean));

const log = [];
for (const e of queue) {
  if (e.status === 'imported') continue;
  const url = e.fields && e.fields.url;
  if (url && knownUrls.has(url)) {
    e.status = 'imported'; e.note = 'already in library';
    log.push('skipped (already in library): ' + e.file);
    continue;
  }
  if (!(await IOUtils.exists(pdfDir + e.file))) {
    e.status = 'missing-file';
    log.push('MISSING FILE: ' + e.file);
    continue;
  }
  try {
    const it = new Zotero.Item(e.itemType || 'webpage');
    it.libraryID = lib;
    for (const [k, v] of Object.entries(e.fields || {})) it.setField(k, v);
    it.setCreators(e.creators || []);
    it.setCollections([coll.id]);
    await it.saveTx();
    await Zotero.Attachments.importFromFile({ file: pdfDir + e.file, parentItemID: it.id });
    e.status = 'imported'; e.zoteroKey = it.key; e.importedAt = new Date().toISOString();
    log.push('added: ' + e.file + ' (' + it.key + ')');
  } catch (err) {
    e.status = 'error'; e.error = String(err);
    log.push('ERROR ' + e.file + ': ' + err);
  }
}
await IOUtils.writeUTF8(queuePath, JSON.stringify(queue, null, 2) + '\n');
return log.length ? log.join('\n') : 'Nothing to import.';
