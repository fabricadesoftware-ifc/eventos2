<template>
  <div class="container">
    <div class="columns is-gapless">
      <div class="column is-10">
        <main class="section">
          <h1 class="title">{{ eventName }}</h1>
          <p>
            {{ eventStartDate.format('LLL') }}
            &ndash;
            {{ eventEndDate.format('LLL') }}
          </p>
          <b-button
            v-if="!eventUserRegistration"
            type="is-primary"
            :loading="loading"
            @click="onRegister"
          >
            {{ $t('pages.index.registerButton') }}
          </b-button>
          <div v-else>
            <b-button
              type="is-primary"
              tag="nuxt-link"
              :to="localePath({ name: 'user-registration' })"
            >
              {{ $t('pages.index.manageRegistrationButton') }}
            </b-button>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

/**
 * Página inicial de um evento.
 */
export default {
  auth: false,
  asyncData() {
    return {
      loading: false
    }
  },
  computed: {
    ...mapGetters([
      'eventName',
      'eventStartDate',
      'eventEndDate',
      'eventUserRegistration'
    ])
  },
  methods: {
    onRegister() {
      this.loading = true
      this.$store
        .dispatch('createEventRegistration')
        .then(() =>
          this.$router.push(this.localePath({ name: 'user-registration' }))
        )
        .finally(() => (this.loading = false))
    }
  }
}
</script>
