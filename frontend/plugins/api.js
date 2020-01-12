import { createAPIClient } from '~/api'

/*
  Esse plugin injeta o objeto `this.$api`,
  para possibilitar a interação com a API de qualquer lugar da aplicação.
*/

export default (ctx, inject) => {
  const apiClients = createAPIClient(ctx.$axios)
  inject('api', apiClients)
}
