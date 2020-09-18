export function createSubmissionAPIClient($axios) {
  return {
    create({ trackSlug, title, title_english, other_authors }) {
      return $axios.$post(`api/v1/submissions/`, {
        track: trackSlug,
        title,
        title_english,
        other_authors
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
