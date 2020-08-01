import Vue from 'vue'
import { extend, ValidationObserver, configure } from 'vee-validate'
import { required, email } from 'vee-validate/dist/rules'

import EInput from '~/components/EInput'
import EDatetimepicker from '~/components/EDatetimepicker'

/**
 * Registrar rules
 */
extend('required', required)
extend('email', email)

/**
 * Registrar componentes globais
 */
Vue.component('EInput', EInput)
Vue.component('EDatetimepicker', EDatetimepicker)
Vue.component('ValidationObserver', ValidationObserver)

export default ({ app }) => {
  configure({
    mode: 'eager',

    // Usar traduções do módulo nuxt-i18n
    defaultMessage: (_, values) =>
      app.i18n.t(`forms.validation.${values._rule_}`, values)
  })
}
