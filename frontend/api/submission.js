export function createSubmissionAPIClient($axios) {
  return {
    create({ trackId, title, title_english, other_authors, documents }) {
      return $axios.$post(`api/v1/submissions/`, {
        track: trackId,
        title,
        title_english,
        other_authors,
        documents
      })
    },
    addDocument({ submissionId, slotId, attachmentKey }) {
      return $axios.$post(`api/v1/submission_documents/`, {
        submission: submissionId,
        slot: slotId,
        document_attachment_key: attachmentKey
      })
    }
  }
}
