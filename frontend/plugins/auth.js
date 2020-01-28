import { handleAPIError } from '~/api/utils'

/*
  Esse plugin precisa ser carregado pelo módulo auth,
  e não diretamente pelo nuxt (ou seja, em `auth.plugins` e não `plugins`).
*/
export default function({ app, $auth }) {
  // Tratamento igual a funcões da API
  $auth.onError(handleAPIError)

  /*
  Faz com que os modules
  @nuxtjs/auth e nuxt-i18n funcionem sem conflito.
  Prepende o código da linguagem atual quando
  redireciona o usuário após login, logout, etc.
  */
  $auth.onRedirect((to, _from) => {
    const resolved = app.router.resolve(to)
    if (resolved && resolved.route && resolved.route.name) {
      const basename = app.getRouteBaseName(resolved.route)
      const out = app.localePath({ name: basename })
      return out
    }
    const out = app.localePath({ path: to })
    return out
  })
}
