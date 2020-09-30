<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <div class="columns is-gapless">
            <div class="column">
              <h1 class="title">{{ $t('pages.admin-tracks.title') }}</h1>
            </div>
            <div class="column is-narrow">
              <b-button
                type="is-success"
                tag="nuxt-link"
                :to="
                  localePath({
                    name: 'admin-tracks-new'
                  })
                "
                >{{ $t('pages.admin-tracks.addButton') }}</b-button
              >
            </div>
          </div>
          <div class="section">
            <b-table :data="tracks" default-sort="name">
              <b-table-column
                v-slot="props"
                field="name"
                :label="$t('pages.admin-tracks.labels.name')"
                sortable
                >{{ props.row.name }}</b-table-column
              >
              <b-table-column
                v-slot="props"
                field="submission_count"
                :label="$t('pages.admin-tracks.labels.submissionCount')"
                width="100"
                sortable
                numeric
              >
                {{ props.row.submission_count }}
              </b-table-column>
              <b-table-column
                field="status"
                :label="$t('pages.admin-tracks.labels.status')"
                width="100"
                sortable
              >
                <template v-slot:default="props">
                  <b-tag v-if="props.row.is_open" type="is-success">{{
                    $t('pages.admin-tracks.submissionsOpen')
                  }}</b-tag>
                </template>
              </b-table-column>
              <b-table-column
                :label="$t('pages.admin-tracks.labels.actions')"
                width="200"
                numeric
              >
                <template v-slot:default="props">
                  <b-button
                    tag="nuxt-link"
                    :to="
                      localePath({
                        name: 'admin-tracks-id-manage',
                        params: { id: props.row.id }
                      })
                    "
                    >{{ $t('pages.admin-tracks.manageButton') }}</b-button
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
    let tracks = []
    tracks = await app.$api.event.listTracks(store.state.event.slug)
    const tracksLocalized = tracks.map(track => {
      if (store.state.locale === 'en' && track.name_english) {
        track.name = track.name_english
      }
      delete track.name_english
      return track
    })
    return {
      error: null,
      tracks: tracksLocalized
    }
  }
}
</script>
