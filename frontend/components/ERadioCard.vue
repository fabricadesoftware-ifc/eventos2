<template>
  <label class="card">
    <div class="card-content">
      <b-radio
        v-model="selectedValue"
        :name="name"
        @input="$emit('select', value)"
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
  model: {
    prop: 'selectedValue',
    event: 'select'
  },
  props: {
    name: {
      type: String,
      default: ''
    },
    value: {
      type: [String, Number, Object],
      default: ''
    }
  },
  data() {
    return {
      selectedValue: null
    }
  }
}
</script>

<style lang="scss" scoped>
label {
  display: block;
}
</style>
