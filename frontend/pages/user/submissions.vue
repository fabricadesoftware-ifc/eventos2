<template>
  <div class="container">
    <div class="columns is-gapless is-centered">
      <div class="column is-8">
        <main class="section">
          <h1 class="title mb-5">{{ $t('pages.user-submissions.title') }}</h1>
          <template v-if="submissions.length != 0">
            <div
              v-for="submission in submissions"
              :key="submission.id"
              class="card mb-4"
            >
              <div class="card-content">
                <div class="submission-header">
                  <div class="submission-title">{{ submission.title }}</div>
                  <template v-if="submission.status == 'waiting_review'">
                    <div class="tag is-warning">
                      {{ $t('pages.user-submissions.statusWaitingReview') }}
                    </div>
                  </template>
                  <template v-if="submission.status == 'accepted'">
                    <div class="tag is-success">
                      {{ $t('pages.user-submissions.statusAccepted') }}
                    </div>
                  </template>
                  <template v-else-if="submission.status == 'rejected'">
                    <div class="tag is-danger">
                      {{ $t('pages.user-submissions.statusRejected') }}
                    </div>
                  </template>
                </div>
                <div class="columns">
                  <div class="column">
                    <div class="item">
                      <div class="item-title">
                        {{ $t('pages.user-submissions.itemTrack') }}
                      </div>
                      {{ submission.track.name }}
                    </div>
                    <div class="item">
                      <div class="item-title">
                        {{ $t('pages.user-submissions.itemAuthors') }}
                      </div>
                      <div
                        v-for="author in submission.authors"
                        :key="author.public_id"
                      >
                        {{ author.first_name }} {{ author.last_name }}
                      </div>
                    </div>
                  </div>
                  <div class="column">
                    <div v-if="submission.documents.length !== 0" class="item">
                      <div class="item-title">
                        {{ $t('pages.user-submissions.itemDocuments') }}
                      </div>
                      <ul>
                        <li
                          v-for="document in submission.documents"
                          :key="document.slot.id"
                        >
                          <a
                            :href="
                              $axios.defaults.baseURL.replace(/\/$/, '') +
                              document.document.url
                            "
                            >{{ document.slot.name }}</a
                          >
                          {{ $t('pages.user-submissions.documentSubmittedOn') }}
                          {{ $dayjs(document.submitted_on).format('llll') }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="mb-4">
              {{ $t('pages.user-submissions.empty') }}
            </div>

            <b-button
              v-if="event.has_tracks"
              type="is-primary"
              tag="nuxt-link"
              :to="localePath({ name: 'submissions-new' })"
            >
              {{ $t('pages.user-submissions.firstSubmissionButton') }}
            </b-button>
          </template>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import errorMixin from '~/mixins/errorMixin'

export default {
  mixins: [errorMixin],
  async asyncData({ app, store }) {
    const event = store.state.event
    const submissions = (await app.$api.user.listSubmissions()).map(
      submission => ({
        ...submission,
        status: 'waiting_review'
      })
    )
    return {
      event,
      submissions
    }
  }
}
</script>

<style lang="scss" scoped>
.submission-header {
  margin-bottom: 1.2em;
}
.submission-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.5em;
  line-height: 1.25;
}
.item {
  margin-bottom: 1em;
}
.item-title {
  font-weight: bold;
  font-size: 0.9rem;
  color: #444;
  margin-bottom: 0.2em;
}
</style>
