<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <div class="columns is-gapless">
            <div class="column">
              <h1 class="title is-3">{{ trackLocalized.name }}</h1>
            </div>
            <div v-if="!needsConfiguration" class="column is-narrow">
              <b-button
                type="is-secondary"
                tag="nuxt-link"
                :to="
                  localePath({
                    name: 'admin-tracks-slug-edit',
                    params: { slug: trackLocalized.slug }
                  })
                "
                >{{ $t('pages.admin-tracks-slug-manage.editButton') }}</b-button
              >
              <b-button
                type="is-primary"
                tag="nuxt-link"
                :to="
                  localePath({
                    name: 'admin-tracks-slug-manage-slots',
                    params: { slug: trackLocalized.slug }
                  })
                "
                >{{
                  $t(
                    'pages.admin-tracks-slug-manage.manageSubmissionDocumentSlots'
                  )
                }}</b-button
              >
            </div>
          </div>
          <div v-if="!needsConfiguration">
            <b-message
              :type="trackLocalized.is_open ? 'is-success' : 'is-info'"
              >{{ statusMessage }}</b-message
            >
            <h2 class="title is-4">
              {{
                $tc(
                  'pages.admin-tracks-slug-manage.submissionCount',
                  submissions.length
                )
              }}
            </h2>
            <b-table
              v-if="submissions.length"
              :data="submissions"
              :columns="submissionColumns"
              default-sort="id"
            />
          </div>
          <div v-else>
            <b-message type="is-warning">
              <div class="mb-4">
                {{
                  $t(
                    'pages.admin-tracks-slug-manage.noSubmissionDocumentSlotsMessage'
                  )
                }}
              </div>

              <b-button
                type="is-primary"
                tag="nuxt-link"
                :to="
                  localePath({
                    name: 'admin-tracks-slug-manage-slots',
                    params: { slug: trackLocalized.slug }
                  })
                "
                icon-left="arrow-right"
                >{{
                  $t(
                    'pages.admin-tracks-slug-manage.manageSubmissionDocumentSlots'
                  )
                }}</b-button
              >
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
    const track = await app.$api.track.getBySlug(params.slug)
    if (store.state.locale === 'en' && track.name_english) {
      track.name = track.name_english
    }
    delete track.name_english

    const submissionDocumentSlots = await app.$api.track.listSubmissionDocumentSlots(
      track.slug
    )

    const submissions = await app.$api.track
      .listSubmissions(track.slug)
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
      trackLocalized: track,
      submissionDocumentSlots,
      submissions
    }
  },
  computed: {
    submissionColumns() {
      return [
        {
          field: 'title',
          label: this.$t(
            'pages.admin-tracks-slug-manage.labels.submissionTitle'
          ),
          sortable: true
        },
        {
          field: 'authorsStr',
          label: this.$t('pages.admin-tracks-slug-manage.labels.authors'),
          sortable: true
        }
      ]
    },
    statusMessage() {
      const startsOn = this.$dayjs(this.trackLocalized.starts_on)
      const endsOn = this.$dayjs(this.trackLocalized.ends_on)

      const isOpen = this.trackLocalized.is_open
      const willOpen = this.$dayjs().isBefore(startsOn)

      const status = isOpen ? 'isOpen' : willOpen ? 'willOpen' : 'wasOpen'
      const messagePath = `pages.admin-tracks-slug-manage.status.${status}`
      return this.$t(messagePath, {
        startDate: startsOn.format('LLLL'),
        endDate: endsOn.format('LLLL')
      })
    },
    needsConfiguration() {
      return (
        !this.submissionDocumentSlots ||
        this.submissionDocumentSlots.length === 0
      )
    }
  }
}
</script>
