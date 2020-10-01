<template>
  <b-navbar type="is-primary" shadow>
    <template v-slot:brand>
      <b-navbar-item
        tag="nuxt-link"
        class="navbar-item"
        :to="localePath({ name: 'index' })"
      >
        {{ eventNameLocalized }}
      </b-navbar-item>
    </template>
    <template v-slot:end>
      <b-navbar-dropdown v-if="isLoggedin">
        <template v-slot:label>
          <b-icon icon="account-circle"></b-icon>
          {{ currentUser.first_name }}
        </template>
        <b-navbar-item
          tag="nuxt-link"
          exact-active-class="is-active"
          :to="localePath({ name: 'user-settings' })"
        >
          <b-icon icon="wrench"></b-icon>
          {{ $t('components.navbar.userMenu.settings') }}
        </b-navbar-item>
        <b-navbar-item @click="logout">
          <b-icon icon="logout-variant"></b-icon>
          {{ $t('components.navbar.userMenu.logout') }}
        </b-navbar-item>
      </b-navbar-dropdown>

      <b-navbar-dropdown class="is-hidden-touch">
        <template v-slot:label>
          <b-icon icon="translate"></b-icon>
          <span>{{ currentLocale.name }}</span>
        </template>
        <b-navbar-item
          v-for="locale in availableLocales"
          :key="locale.code"
          tag="nuxt-link"
          :to="switchLocalePath(locale.code)"
          >{{ locale.name }}
        </b-navbar-item>
      </b-navbar-dropdown>
    </template>
  </b-navbar>
</template>

<script>
/**
 * Navbar geral do sistema.
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
    },
    currentUser() {
      return this.$auth.user
    },
    isLoggedin() {
      return this.$auth.loggedIn
    },
    eventNameLocalized() {
      const event = this.$store.state.event
      if (!event) {
        return
      }
      if (this.$store.state.locale === 'en' && event.name_english) {
        return event.name_english
      }
      return event.name
    }
  },

  methods: {
    async logout() {
      await this.$store.dispatch('logoutUser')
      this.$auth.redirect('home')
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar-item.has-dropdown .icon {
  margin-right: 6px;
}
</style>
