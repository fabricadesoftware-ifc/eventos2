import dayjs from 'dayjs'
import enCA from 'dayjs/locale/en-ca'
import ptBR from 'dayjs/locale/pt-br'
import LocalizedFormat from 'dayjs/plugin/localizedFormat'
import isBetween from 'dayjs/plugin/isBetween'

dayjs.extend(LocalizedFormat)
dayjs.extend(isBetween)

// Renomear locales para espelhar a configuração do nuxt
dayjs.locale('en', enCA)
dayjs.locale('pt', ptBR)

export default dayjs
