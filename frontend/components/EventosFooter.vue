<template>
  <footer class="footer">
    <div class="container">
      <div class="columns is-desktop">
        <div class="column">
          {{ $t('components.footer.menuTitle') }}
          <links-menu class="menu" :links="links" dark />
        </div>
        <div class="column">
          <language-picker-footer class="is-hidden-desktop" />
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import LanguagePickerFooter from '~/components/LanguagePickerFooter'
import LinksMenu from '~/components/LinksMenu'

/**
 * Footer geral do sistema.
 */

export default {
  components: {
    LanguagePickerFooter,
    LinksMenu
  },
  computed: {
    links() {
      return [
        {
          title: this.$t('components.footer.menuItems.home'),
          icon: 'home',
          to: { name: 'index' }
        },
        {
          title: this.$t('components.footer.menuItems.login'),
          icon: 'login',
          to: { name: 'login' }
        },
        {
          title: this.$t('components.footer.menuItems.signup'),
          icon: 'account-plus',
          to: { name: 'signup' }
        }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
.menu {
  margin-top: 1em;
}
</style>
