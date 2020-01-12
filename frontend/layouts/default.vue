<template>
  <div class="wrapper">
    <eventos-navbar />

    <div class="content">
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
.wrapper {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
.content {
  flex: 1;
}
</style>
