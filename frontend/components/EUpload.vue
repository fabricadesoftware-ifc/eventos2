<template>
  <ValidationProvider
    ref="provider"
    v-slot="{ errors, failed }"
    :vid="vid"
    :name="name"
    :rules="rules"
    slim
  >
    <b-field
      :type="{ 'is-danger': failed }"
      :message="errors"
      :horizontal="horizontal"
      :label="label"
    >
      <b-upload :id="inputId" v-model="innerValue" :name="name">
        <div
          class="button is-primary is-fullwidth"
          :class="{ 'is-loading': loading }"
        >
          <b-icon icon="upload"></b-icon>
          <span>{{
            (innerValue && innerValue.name) ||
            placeholder ||
            $t('components.upload.placeholder')
          }}</span>
        </div>
      </b-upload>
    </b-field>
  </ValidationProvider>
</template>

<script>
import { ValidationProvider } from 'vee-validate'

/**
 * Wrapper sobre o upload do Buefy com validação via VeeValidate
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
    placeholder: {
      type: String,
      default: ''
    },
    value: {
      type: null,
      default: null
    },
    horizontal: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    innerValue: []
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
      this.$refs.provider.validate(newVal)
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
