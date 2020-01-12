import { handleAxiosError } from '~/api/utils'

/*
  Esse plugin precisa ser carregado pelo módulo auth,
  e não diretamente pelo nuxt (ou seja, em `auth.plugins` e não `plugins`).
*/
export default function({ app, $auth }) {
  // Tratamento igual a funcões da API
  $auth.onError(handleAxiosError)

  /*
  Faz com que os modules
  @nuxtjs/auth e nuxt-i18n funcionem sem conflito.
  Prepende o código da linguagem atual quando
  redireciona o usuário após login, logout, etc.
  */
  $auth.onRedirect((to, from) => {
    const currentLocale = app.i18n.locale
    return '/' + currentLocale + to
  })
}
