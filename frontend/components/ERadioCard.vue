<template>
  <label class="card">
    <div class="card-content">
      <b-radio
        :name="name"
        :disabled="disabled"
        :native-value="nativeValue"
        :value="value"
        @input="$emit('input', $event)"
      >
        <slot></slot>
      </b-radio>
    </div>
  </label>
</template>

<script>
/**
 * Wrapper sobre o radio do Buefy (sem validação)
 */
export default {
  props: {
    name: {
      type: String,
      default: ''
    },
    value: {
      type: [String, Object, null],
      default: null
    },
    nativeValue: {
      type: [String, Object, null],
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss" scoped>
label {
  display: block;
}
</style>
