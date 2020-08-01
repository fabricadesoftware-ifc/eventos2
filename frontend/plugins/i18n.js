/**
 * Sincroniza o locale atual com o estado do store.
 */

export default function ({ app }) {
  app.store.commit('setLocale', app.i18n.locale)

  app.i18n.beforeLanguageSwitch = (_, newLocale) => {
    app.store.commit('setLocale', newLocale)
    // Change date format locale
    app.$dayjs.locale(newLocale)
  }
}
