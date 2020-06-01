import { createActivityAPIClient } from '~/api/activity'
import { createActivityRegistrationAPIClient } from '~/api/activityRegistration'
import { createEventAPIClient } from '~/api/event'
import { createEventRegistrationAPIClient } from '~/api/eventRegistration'
import { createUserAPIClient } from '~/api/user'

/*
  Todos os clientes de API dependem da injeção
  de uma instância axios pra realizar os requests.
*/

export function createAPIClient($axios) {
  return {
    activity: createActivityAPIClient($axios),
    activityRegistration: createActivityRegistrationAPIClient($axios),
    event: createEventAPIClient($axios),
    eventRegistration: createEventRegistrationAPIClient($axios),
    user: createUserAPIClient($axios)
  }
}
