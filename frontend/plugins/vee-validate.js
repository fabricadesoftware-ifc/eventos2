import Vue from 'vue'
import { extend, ValidationObserver, configure } from 'vee-validate'
import { required, email, mimes } from 'vee-validate/dist/rules'

import EInput from '~/components/EInput'
import EDatetimepicker from '~/components/EDatetimepicker'
import ERadioCard from '~/components/ERadioCard'
import ESelect from '~/components/ESelect'
import EUpload from '~/components/EUpload'

/**
 * Registrar rules
 */
extend('required', required)
extend('email', email)
extend('mimes', mimes)

/**
 * Registrar componentes globais
 */
Vue.component('EInput', EInput)
Vue.component('ERadioCard', ERadioCard)
Vue.component('ESelect', ESelect)
Vue.component('EDatetimepicker', EDatetimepicker)
Vue.component('EUpload', EUpload)
Vue.component('ValidationObserver', ValidationObserver)

export default ({ app }) => {
  configure({
    mode: 'eager',

    // Usar traduções do módulo nuxt-i18n
    defaultMessage: (_, values) =>
      app.i18n.t(`forms.validation.${values._rule_}`, values)
  })
}
