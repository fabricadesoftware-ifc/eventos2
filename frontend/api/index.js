import { createActivityAPIClient } from '~/api/activity'
import { createActivityRegistrationAPIClient } from '~/api/activityRegistration'
import { createDocumentAPIClient } from '~/api/document'
import { createEventAPIClient } from '~/api/event'
import { createEventRegistrationAPIClient } from '~/api/eventRegistration'
import { createSubmissionAPIClient } from '~/api/submission'
import { createTrackAPIClient } from '~/api/track'
import { createTrackReviewQuestionAPIClient } from '~/api/trackReviewQuestion'
import { createTrackSubmissionDocumentSlotAPIClient } from '~/api/trackSubmissionDocumentSlot'
import { createUserAPIClient } from '~/api/user'

/*
  Todos os clientes de API dependem da injeção
  de uma instância axios pra realizar os requests.
*/

export function createAPIClient($axios) {
  return {
    activity: createActivityAPIClient($axios),
    activityRegistration: createActivityRegistrationAPIClient($axios),
    document: createDocumentAPIClient($axios),
    event: createEventAPIClient($axios),
    eventRegistration: createEventRegistrationAPIClient($axios),
    submission: createSubmissionAPIClient($axios),
    track: createTrackAPIClient($axios),
    trackReviewQuestion: createTrackReviewQuestionAPIClient($axios),
    trackSubmissionDocumentSlot:
      createTrackSubmissionDocumentSlotAPIClient($axios),
    user: createUserAPIClient($axios)
  }
}
