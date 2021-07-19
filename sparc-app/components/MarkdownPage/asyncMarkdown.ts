import createClient from "~/plugins/contentful";

const client = createClient()

/**
 * helper to drop into the asyncData method of respective pages
 */
export const asyncMarkdown = async (entryId: string, headerField: string, bodyField: string):
  Promise<{ header: string, body: string }> => {
  try {
    const { fields } = await client.getEntry(entryId)
    return { header: fields[headerField] ?? '', body: fields[bodyField] ?? '' }
  } catch (e) {
    console.error(e)
    return { header: '', body: '' }
  }
}