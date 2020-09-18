<template>
  <b-icon
    :icon="value ? doneIcon : defaultIcon"
    :class="[
      classProp,
      {
        'has-text-gray': !value,
        'has-text-success': value
      }
    ]"
  ></b-icon>
</template>

<script>
export default {
  props: {
    value: {
      type: null,
      default: null
    },
    classProp: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      defaultIcon: 'circle-outline',
      doneIcon: 'check-circle-outline'
    }
  }
}
</script>
