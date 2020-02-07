<template>
  <div class="outer-wrapper">
    <eventos-navbar />

    <div class="inner-wrapper">
      <nuxt />
    </div>

    <eventos-footer />
  </div>
</template>

<script>
import EventosFooter from '~/components/EventosFooter'
import EventosNavbar from '~/components/EventosNavbar'

/**
 * Layout padrão (duh).
 */
export default {
  components: {
    EventosFooter,
    EventosNavbar
  }
}
</script>

<style lang="scss" scoped>
// Sticky footer
.outer-wrapper {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
.inner-wrapper {
  flex: 1;
}
</style>
