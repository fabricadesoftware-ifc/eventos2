<template>
  <div class="container">
    <div class="columns is-gapless">
      <div class="column is-10">
        <main class="section">
          <h1 class="title">{{ eventNameLocalized }}</h1>
          <p>
            {{ eventStartDate }}
            &ndash;
            {{ eventEndDate }}
          </p>

          <b-button
            v-if="!eventRegistration"
            type="is-primary"
            :loading="loading"
            @click="onRegister"
          >
            {{ $t('pages.index.registerButton') }}
          </b-button>
          <div v-else>
            <b-button
              v-if="event.has_tracks"
              type="is-primary"
              tag="nuxt-link"
              :to="localePath({ name: 'submissions-new' })"
            >
              {{ $t('pages.index.newSubmissionButton') }}
            </b-button>
            <b-button
              v-if="event.has_activities"
              :type="event.has_tracks ? 'is-secondary' : 'is-primary'"
              tag="nuxt-link"
              :to="localePath({ name: 'activities' })"
            >
              {{ $t('pages.index.manageActivitiesButton') }}
            </b-button>
            <b-button
              type="is-secondary"
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
/**
 * Página inicial de um evento.
 */
export default {
  auth: false,
  asyncData({ app, store }) {
    const event = store.state.event

    let eventNameLocalized = event.name
    if (store.state.locale === 'en' && event.name_english) {
      eventNameLocalized = event.name_english
    }

    const eventStartDate = app.$dayjs(event.starts_on).format('LLL')
    const eventEndDate = app.$dayjs(event.ends_on).format('LLL')

    return {
      loading: false,
      event,
      eventNameLocalized,
      eventStartDate,
      eventEndDate,
      eventRegistration: store.state.eventRegistration
    }
  },
  methods: {
    onRegister() {
      if (this.$auth.user === null) {
        this.$router.push(this.localePath({ name: 'login' }))
        return
      }
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
