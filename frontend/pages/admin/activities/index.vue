<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <div class="columns is-gapless">
            <div class="column">
              <h1 class="title">
                {{ $t('pages.admin-activities.title') }}
              </h1>
            </div>
            <div class="column is-narrow">
              <b-button
                type="is-success"
                tag="nuxt-link"
                :to="
                  localePath({
                    name: 'admin-activities-new'
                  })
                "
                >{{ $t('pages.admin-activities.addButton') }}</b-button
              >
            </div>
          </div>
          <div class="section">
            <b-table :data="activities" default-sort="name">
              <template v-slot="{ row }">
                <b-table-column
                  field="name"
                  :label="$t('pages.admin-activities.labels.name')"
                  sortable
                >
                  {{ row.name }}
                </b-table-column>
                <b-table-column
                  :label="$t('pages.admin-activities.labels.actions')"
                  width="200"
                  numeric
                >
                  <b-button
                    tag="nuxt-link"
                    :to="
                      localePath({
                        name: 'admin-activities-slug',
                        params: {
                          slug: row.slug
                        }
                      })
                    "
                    >{{ $t('pages.admin-activities.editButton') }}</b-button
                  >
                </b-table-column>
              </template>
            </b-table>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  async asyncData({ store, app }) {
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
      loading: false,
      error: null,
      activities: activitiesLocalized
    }
  }
}
</script>

<style lang="scss" scoped>
.activity {
  margin-bottom: 1em;
}
.activity .card-footer-item {
  padding: 0;
}
.activity .button {
  width: 100%;
  height: 100%;
  border-radius: 0;
  border: none;
}
</style>
