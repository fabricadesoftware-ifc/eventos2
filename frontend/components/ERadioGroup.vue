<template>
  <ValidationProvider
    v-slot="{ errors, failed }"
    :vid="vid"
    :name="name"
    :rules="rules"
    slim
  >
    <b-field :label="label" :type="{ 'is-danger': failed }" :message="errors">
      <slot />
    </b-field>
  </ValidationProvider>
</template>

<script>
import { ValidationProvider } from 'vee-validate'

/**
 * Wrapper para radios do Buefy com validação via VeeValidate
 */
export default {
  components: {
    ValidationProvider
  },
  props: {
    vid: {
      type: [String, null],
      default: null
    },
    rules: {
      type: [Object, String],
      default: ''
    },
    name: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: ''
    }
  }
}
</script>
