<template>
  <b-dropdown position="is-bottom-left">
    <template v-slot:trigger>
      <b-button
        type="is-primary"
        icon-left="translate"
        icon-right="menu-down"
        inverted
        outlined
      >
        {{ currentLocale.name }}
      </b-button>
    </template>
    <b-dropdown-item
      v-for="locale in availableLocales"
      :key="locale.code"
      has-link
    >
      <nuxt-link :to="switchLocalePath(locale.code)">{{
        locale.name
      }}</nuxt-link>
    </b-dropdown-item>
  </b-dropdown>
</template>

<script>
/**
 * Dropdown menu para mudar de locale.
 * Feito para uso no footer.
 */

export default {
  computed: {
    currentLocale() {
      return this.$i18n.locales.filter(
        locale => locale.code === this.$i18n.locale
      )[0]
    },
    availableLocales() {
      return this.$i18n.locales.filter(
        locale => locale.code !== this.$i18n.locale
      )
    }
  }
}
</script>

<style lang="scss" scoped>
.language-icon {
  margin-right: 6px;
}
</style>
