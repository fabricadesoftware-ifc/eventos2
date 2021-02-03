<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <div class="columns is-gapless">
            <div class="column">
              <h1 class="title is-3">
                {{
                  $tc(
                    'pages.admin-submissions.submissionCount',
                    submissions.length
                  )
                }}
              </h1>
            </div>
          </div>
          <b-table v-if="submissions.length" :data="submissions">
            <b-table-column
              v-slot="props"
              field="title"
              :label="$t('pages.admin-submissions.labels.submissionTitle')"
              sortable
              >{{ props.row.title }}</b-table-column
            >
            <b-table-column
              v-slot="props"
              field="authorsStr"
              :label="$t('pages.admin-submissions.labels.authors')"
              sortable
              >{{ props.row.authorsStr }}</b-table-column
            >
            <b-table-column
              v-slot="props"
              :label="$t('pages.admin-submissions.labels.actions')"
              width="200"
              numeric
            >
              <b-button
                tag="nuxt-link"
                :to="
                  localePath({
                    name: 'admin-submissions',
                    params: { id: props.row.id }
                  })
                "
                >{{ $t('pages.admin-tracks.manageButton') }}</b-button
              ></b-table-column
            >
          </b-table>
          <div v-else>
            <b-message type="is-info">
              {{ $t('pages.admin-submissions.emptyMessage') }}
            </b-message>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  async asyncData({ app, params, store }) {
    const submissions = await app.$api.event
      .listSubmissions(store.state.event.slug)
      .then(submissions =>
        submissions.map(submission => {
          const authors = submission.authors.map(author => ({
            ...author,
            fullName: author.first_name + ' ' + author.last_name
          }))
          const authorsStr = authors.map(author => author.fullName).join('; ')
          return {
            ...submission,
            authors,
            authorsStr
          }
        })
      )
    return {
      submissions
    }
  }
}
</script>
