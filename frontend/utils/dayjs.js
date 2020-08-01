import dayjs from 'dayjs'
import en from 'dayjs/locale/en'
import ptBR from 'dayjs/locale/pt-br'
import LocalizedFormat from 'dayjs/plugin/localizedFormat'
import isBetween from 'dayjs/plugin/isBetween'

dayjs.extend(LocalizedFormat)
dayjs.extend(isBetween)

// Renomear locales para espelhar a configuração do nuxt
dayjs.locale('en', en)
dayjs.locale('pt', ptBR)

export default dayjs
