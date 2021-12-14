export default {
  mode: 'universal',

  vue: {
    config: {
      devtools: process.env.EVENTOS2_FRONTEND_DEBUG === 'true'
    }
  },

  modules: [],

  plugins: [
    '~/plugins/api.js',
    '~/plugins/axios.js',
    '~/plugins/dayjs.js',
    '~/plugins/i18n.js',
    '~/plugins/visibility.js',
    '~/plugins/vee-validate.js'
  ],

  publicRuntimeConfig: {
    axios: {
      browserBaseURL: process.env.EVENTOS2_FRONTEND_BROWSER_BASE_URL || '/'
    }
  },

  privateRuntimeConfig: {
    forceEventSlug: process.env.EVENTOS2_FRONTEND_FORCE_SLUG || null,
    axios: {
      baseURL: process.env.EVENTOS2_FRONTEND_BASE_URL || '/'
    }
  },

  buildModules: [
    '@nuxtjs/eslint-module',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/style-resources',
    'nuxt-i18n',
    // Disable CSS import so we can customize some variables
    // (see ~/assets/vars)
    ['nuxt-buefy', { css: false, materialDesignIcons: false }]
  ],

  build: {
    transpile: ['vee-validate/dist/rules'],
    extend(config, ctx) {
      // Use inline source maps for the server, and regular ones for the client.
      // Allows the VSCode debugger to work.
      if (ctx.isDev) {
        config.devtool = ctx.isClient ? 'source-map' : 'inline-source-map'
      }
    }
  },

  render: {
    csp: true
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

  css: ['~/assets/global.scss', '@mdi/font/css/materialdesignicons.css'],
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
        maxAge: 172800,
        secure: process.env.NODE_ENV === 'production'
      }
    },
    localStorage: false,
    strategies: {
      refresh: {
        token: {
          property: 'access',
          maxAge: 1800
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 172800
        },
        user: {
          property: false
        },
        endpoints: {
          login: {
            url: '/api/v1/token/',
            method: 'post'
          },
          refresh: {
            url: '/api/v1/token/refresh/',
            method: 'post'
          },
          user: {
            url: '/api/v1/users/current/',
            method: 'get'
          },
          logout: false
        }
      }
    },
    redirect: {
      login: '/login/',
      logout: '/login/',
      home: '/'
    },
    plugins: ['~/plugins/auth.js']
  }
}
