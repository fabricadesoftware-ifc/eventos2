import { createEventAPIClient } from '~/api/event'
import { createEventRegistrationAPIClient } from '~/api/eventRegistration'
import { createUserAPIClient } from '~/api/user'

/*
  Todos os clientes de API dependem da injeção
  de uma instância axios pra realizar os requests.
*/

export function createAPIClient($axios) {
  return {
    event: createEventAPIClient($axios),
    eventRegistration: createEventRegistrationAPIClient($axios),
    user: createUserAPIClient($axios)
  }
}
