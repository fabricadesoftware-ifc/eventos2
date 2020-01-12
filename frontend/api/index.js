import { createUserAPIClient } from '~/api/user'

/*
  Todos os clientes de API dependem da injeção
  de uma instância axios pra realizar os requests.
*/

export function createAPIClient($axios) {
  return {
    user: createUserAPIClient($axios)
  }
}
