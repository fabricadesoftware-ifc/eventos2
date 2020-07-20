<template>
  <div class="container">
    <div class="columns is-gapless">
      <div class="column is-10">
        <main class="section">
          <h1 class="title">{{ $t('pages.activities.title') }}</h1>
          <div class="columns is-multiline">
            <div
              v-for="activity in activities"
              :key="activity.slug"
              class="column is-half"
            >
              <div class="card">
                <div class="card-content">
                  {{ activity.name }}
                </div>
                <div class="card-footer">
                  <div class="card-footer-item is-paddingless">
                    <b-button
                      v-if="!activity.registration"
                      type="is-success"
                      expanded
                      @click="onRegister(activity)"
                      >{{ $t('pages.activities.registerButton') }}</b-button
                    >
                    <b-button
                      v-else
                      type="is-secondary"
                      expanded
                      @click="onDeregister(activity)"
                      >{{
                        $t('pages.activities.cancelRegistrationButton')
                      }}</b-button
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * Lista das atividades do evento.
 */
export default {
  async asyncData({ app, store }) {
    const activities = await app.$api.event.listActivities(
      store.state.event.slug
    )
    const registrations = await app.$api.activityRegistration.listByUserAndEvent(
      {
        userPublicId: app.$auth.user.public_id,
        eventSlug: store.state.event.slug
      }
    )
    const activitiesLocalized = activities.map(activity => {
      let localizedName = activity.name
      if (store.state.locale === 'en' && activity.name_english) {
        localizedName = activity.name_english
      }
      return {
        name: localizedName,
        starts_on: activity.starts_on,
        ends_on: activity.ends_on,
        slug: activity.slug,
        registration:
          registrations.find(x => x.activity.slug === activity.slug) || null
      }
    })
    return {
      activities: activitiesLocalized
    }
  },
  methods: {
    onRegister(activity) {
      this.$api.activityRegistration
        .register({ activitySlug: activity.slug })
        .then(registration => {
          activity.registration = registration
        })
    },
    onDeregister(activity) {
      this.$api.activityRegistration
        .deregister({ registrationId: activity.registration.id })
        .then(() => {
          activity.registration = null
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.card-footer-item .button {
  border: none !important;
  border-radius: 0 !important;
}
</style>
