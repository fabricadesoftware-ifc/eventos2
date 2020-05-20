<template>
  <div class="container">
    <div class="columns is-gapless">
      <div class="column is-10">
        <main class="section">
          <h1 class="title">{{ $t('pages.activities.title') }}</h1>
          <div class="columns is-multiline">
            <div
              v-for="activity in activities"
              :key="activity.id"
              class="column is-half"
            >
              <div class="card">
                <div class="card-content">
                  {{ activity.name }}
                </div>
                <div class="card-footer">
                  <div class="card-footer-item is-paddingless">
                    <b-button type="is-success" expanded>Register</b-button>
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
    let activities = []
    activities = await app.$api.event.listActivities(store.state.event.slug)
    const activitiesLocalized = activities.map(activity => {
      if (store.state.locale === 'en' && activity.name_english) {
        return {
          id: activity.id,
          name: activity.name_english,
          starts_on: activity.starts_on,
          ends_on: activity.ends_on,
          slug: activity.slug
        }
      }
      return activity
    })
    return {
      activities: activitiesLocalized
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
