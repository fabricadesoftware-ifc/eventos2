<template>
  <div>
    <eventos-navbar />

    <div class="columns is-gapless">
      <div class="column is-narrow">
        <eventos-admin-menu />
      </div>
      <div class="column">
        <nuxt />
      </div>
    </div>

    <eventos-footer />
  </div>
</template>

<script>
import EventosFooter from '~/components/EventosFooter'
import EventosNavbar from '~/components/EventosNavbar'
import EventosAdminMenu from '~/components/EventosAdminMenu'

/**
 * Layout admin
 */
export default {
  components: {
    EventosFooter,
    EventosNavbar,
    EventosAdminMenu
  }
}
</script>
