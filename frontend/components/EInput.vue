<template>
  <ValidationProvider
    v-slot="{ errors, failed }"
    :vid="vid"
    :name="name"
    :rules="rules"
    slim
  >
    <b-field
      :label="label"
      :label-for="inputId"
      :type="{ 'is-danger': failed }"
      :message="errors"
      :horizontal="horizontal"
    >
      <b-input
        :id="inputId"
        v-model="innerValue"
        :type="type"
        :name="name"
        :password-reveal="passwordReveal"
        :autocomplete="autocomplete"
      ></b-input>
    </b-field>
  </ValidationProvider>
</template>

<script>
import { ValidationProvider } from 'vee-validate'

/**
 * Wrapper sobre o input do Buefy com validação via VeeValidate
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
    },
    type: {
      type: String,
      default: 'text'
    },
    value: {
      type: null,
      default: null
    },
    horizontal: {
      type: Boolean,
      default: false
    },
    passwordReveal: {
      type: Boolean,
      default: false
    },
    autocomplete: {
      type: String,
      default: 'on'
    }
  },
  data: () => ({
    innerValue: ''
  }),
  computed: {
    inputId() {
      let id = this.name
      if (this.vid) {
        id += '-' + this.vid
      }
      return id
    }
  },
  watch: {
    // Handles internal model changes
    innerValue(newVal) {
      this.$emit('input', newVal)
    },
    // Handles external model changes
    value(newVal) {
      this.innerValue = newVal
    }
  },
  created() {
    if (this.value) {
      this.innerValue = this.value
    }
  }
}
</script>
