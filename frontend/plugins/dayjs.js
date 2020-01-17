import dayjs from '~/utils/dayjs'

/**
 * Injeta uma instância da bibliteca de manipulação de datas.
 */

export default (_ctx, inject) => {
  inject('dayjs', dayjs)
}
