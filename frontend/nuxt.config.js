export default {
  mode: 'universal',

  modules: [
    '@nuxtjs/auth',
    '@nuxtjs/axios',
    '@nuxtjs/style-resources',
    'nuxt-i18n',
    // Disable CSS import so we can customize some variables
    // (see ~/assets/vars)
    ['nuxt-buefy', { css: false }]
  ],
  plugins: [
    '~/plugins/api.js',
    '~/plugins/visibility.js',
    '~/plugins/vee-validate.js'
  ],

  build: {
    transpile: ['vee-validate/dist/rules'],
    extend(config, ctx) {
      // Run eslint and show errors when hot-reloading
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }

      // Use inline source maps for the server, and regular ones for the client.
      // Allows the VSCode debugger to work.
      if (ctx.isDev) {
        config.devtool = ctx.isClient ? 'source-map' : 'inline-source-map'
      }
    }
  },

  router: {
    middleware: [
      // Needed for redirection to the login page when not authenticated
      'auth'
    ]
  },

  head: {
    title: 'Eventos2',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Eventos2' }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },

  css: ['~/assets/global.scss'],
  styleResources: { scss: ['~/assets/vars/*.scss'] },
  loading: { color: '#fff' },

  i18n: {
    locales: [
      {
        code: 'en',
        iso: 'en-US',
        name: 'English',
        file: 'en/translations.json'
      },
      {
        code: 'pt',
        iso: 'pt-BR',
        name: 'Português',
        file: 'pt/translations.json'
      }
    ],
    defaultLocale: 'en',
    vueI18n: {
      fallbackLocale: 'en',
      silentTranslationWarn: true,
      silentFallbackWarn: false
    },
    strategy: 'prefix',
    lazy: true,
    langDir: 'locales/',
    rootRedirect: 'en',
    seo: false
  },

  auth: {
    cookie: {
      options: {
        secure: process.env.NODE_ENV === 'production'
      }
    },
    localStorage: false,
    strategies: {
      local: {
        endpoints: {
          login: {
            url: '/api/v1/token/',
            method: 'post',
            propertyName: 'access'
          },
          logout: false,
          user: {
            url: '/api/v1/users/current',
            method: 'get',
            propertyName: false
          }
        }
      }
    },
    redirect: {
      login: '/login/',
      logout: '/login/',
      home: '/'
    },
    plugins: ['~/plugins/auth.js']
  },

  axios: {
    proxy: true
  },
  proxy: {
    '/api/': 'http://localhost:8000/'
  }
}
