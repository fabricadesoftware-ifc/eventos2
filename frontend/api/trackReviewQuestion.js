export function createTrackReviewQuestionAPIClient($axios) {
  return {
    create({ trackId, text, answer_type }) {
      return $axios.$post(`api/v1/track_review_questions/`, {
        track: trackId,
        text,
        answer_type
      })
    }
  }
}
