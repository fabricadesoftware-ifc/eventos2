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
                      v-if="activity.registration"
                      type="is-secondary"
                      expanded
                      @click="onDeregister(activity)"
                      >{{
                        $t('pages.activities.cancelRegistrationButton')
                      }}</b-button
                    >
                    <b-button
                      v-else-if="!activity.is_open"
                      type="is-secondary"
                      expanded
                      disabled
                      >{{
                        $t('pages.activities.registrationsClosed')
                      }}</b-button
                    >
                    <b-button
                      v-else
                      type="is-success"
                      expanded
                      @click="onRegister(activity)"
                      >{{ $t('pages.activities.registerButton') }}</b-button
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
import errorMixin from '~/mixins/errorMixin'

/**
 * Lista das atividades do evento.
 */
export default {
  mixins: [errorMixin],

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
      if (store.state.locale === 'en' && activity.name_english) {
        activity.name = activity.name_english
      }
      delete activity.name_english
      activity.registration =
        registrations.find(x => x.activity.slug === activity.slug) || null
      return activity
    })
    return {
      activities: activitiesLocalized
    }
  },
  methods: {
    onRegister(activity) {
      this.$api.activityRegistration
        .register({ activitySlug: activity.slug })
        .then(registration => (activity.registration = registration))
        .catch(this.handleGenericError)
    },
    onDeregister(activity) {
      const message = activity.is_open
        ? 'cancelRegistrationDialogMessage'
        : 'cancelRegistrationClosedDialogMessage'
      this.$buefy.dialog.confirm({
        message: this.$t(`pages.activities.${message}`),
        confirmText: this.$t('pages.activities.cancelRegistrationButton'),
        cancelText: this.$t('pages.activities.dialogCancelButton'),
        focusOn: 'cancel',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => {
          this.$api.activityRegistration
            .deregister({ registrationId: activity.registration.id })
            .then(() => {
              activity.registration = null
            })
            .catch(this.handleGenericError)
        }
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
