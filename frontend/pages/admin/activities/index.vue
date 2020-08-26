<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <div class="columns is-gapless">
            <div class="column">
              <h1 class="title">{{ $t('pages.admin-activities.title') }}</h1>
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
              <b-table-column
                v-slot="props"
                field="name"
                :label="$t('pages.admin-activities.labels.name')"
                sortable
                >{{ props.row.name }}</b-table-column
              >
              <b-table-column
                v-slot="props"
                field="registration_count"
                :label="$t('pages.admin-activities.labels.registrationCount')"
                width="100"
                sortable
                numeric
              >
                {{ props.row.registration_count }}
              </b-table-column>
              <b-table-column
                v-slot="props"
                field="status"
                :label="$t('pages.admin-activities.labels.status')"
                width="100"
                sortable
              >
                <b-tag v-if="props.row.is_open" type="is-success">{{
                  $t('pages.admin-activities.registrationsOpen')
                }}</b-tag>
              </b-table-column>
              <b-table-column
                :label="$t('pages.admin-activities.labels.actions')"
                width="200"
                numeric
              >
                <template v-slot:default="props">
                  <b-button
                    tag="nuxt-link"
                    :to="
                      localePath({
                        name: 'admin-activities-slug-manage',
                        params: { slug: props.row.slug }
                      })
                    "
                    >{{ $t('pages.admin-activities.manageButton') }}</b-button
                  >
                </template>
              </b-table-column>
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
        activity.name = activity.name_english
      }
      delete activity.name_english
      return activity
    })
    return {
      error: null,
      activities: activitiesLocalized
    }
  }
}
</script>
