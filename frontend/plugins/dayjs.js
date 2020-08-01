import dayjs from '~/utils/dayjs'

/**
 * Injeta uma instância da bibliteca de manipulação de datas.
 */

export default ({ app }, inject) => {
  const currentLocale = app.i18n.locale
  if (currentLocale) {
    // Change date format locale on load
    dayjs.locale(currentLocale)
  }
  inject('dayjs', dayjs)
}
