<template>
  <div class="container">
    <div class="columns is-gapless is-centered">
      <div class="column is-10">
        <main class="section">
          <h1 class="title">{{ $t('pages.submissions-new.title') }}</h1>
          <ValidationObserver ref="form">
            <form @submit.prevent>
              <b-steps
                ref="steps"
                type="is-primary"
                :destroy-on-hide="stepsWorkaround.destroyOnHide"
                size="is-small"
                mobile-mode="compact"
              >
                <b-step-item
                  v-if="stepsWorkaround.dummyFirstStep"
                ></b-step-item>
                <b-step-item
                  value="details"
                  :label="$t('pages.submissions-new.steps.details.label')"
                >
                  <e-select
                    v-model="form.trackId"
                    :label="$t('forms.labels.track')"
                    :placeholder="
                      $t('pages.submissions-new.steps.details.trackPlaceholder')
                    "
                    rules="required"
                    class="mb-5"
                  >
                    <option
                      v-for="track in openTracks"
                      :key="track.id"
                      :value="track.id"
                      >{{ track.name }}</option
                    >
                  </e-select>
                  <e-input
                    v-model="form.title"
                    name="title"
                    :label="$t('forms.labels.submissionTitle')"
                    rules="required"
                  />
                </b-step-item>
                <b-step-item
                  :label="$t('pages.submissions-new.steps.authors.label')"
                >
                  <div class="columns">
                    <div class="column">
                      <e-user-search @select="addAuthor" />
                    </div>
                    <div class="column">
                      <div class="panel">
                        <div class="panel-heading">
                          {{
                            $t(
                              'pages.submissions-new.steps.authors.selectedAuthors'
                            )
                          }}
                        </div>
                        <div
                          v-for="author in form.authors"
                          :key="author.public_id"
                          class="panel-block"
                        >
                          <b-icon icon="account" class="panel-icon" />
                          <div class="control">
                            {{ author.first_name + ' ' + author.last_name }}
                            &lt;{{ author.email }}&gt;
                          </div>
                          <div class="control">
                            <b-button
                              v-if="author !== $auth.user"
                              icon-left="minus"
                              class="is-pulled-right"
                              size="is-small"
                              @click="removeAuthor(author)"
                              >{{
                                $t(
                                  'pages.submissions-new.steps.authors.removeButton'
                                )
                              }}</b-button
                            >
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </b-step-item>
                <b-step-item
                  :label="$t('pages.submissions-new.steps.documents.label')"
                >
                  <div class="mb-4">
                    {{
                      $tc(
                        'pages.submissions-new.steps.documents.description',
                        submissionDocumentSlots
                          ? submissionDocumentSlots.length
                          : 0
                      )
                    }}
                  </div>
                  <div
                    v-for="slot in submissionDocumentSlots"
                    :key="slot.id"
                    class="mb-3"
                  >
                    <e-upload
                      v-model="form.files[slot.id]"
                      :name="`file-${slot.id}`"
                      :label="slot.name"
                      :placeholder="
                        $t('pages.submissions-new.steps.documents.chooseFile', {
                          fileTypes: validExtensions.join(', ')
                        })
                      "
                      :rules="'required|mimes:' + validMimeTypes.join(',')"
                    ></e-upload>
                  </div>
                </b-step-item>
                <b-step-item
                  value="confirm"
                  :label="$t('pages.submissions-new.steps.confirm.label')"
                >
                  <div class="title is-5">
                    {{ $t('pages.submissions-new.steps.confirm.description') }}
                  </div>
                  <div v-if="form.trackId && form.title" class="panel">
                    <div class="panel-block">
                      <e-status-icon
                        v-model="status.submission"
                        class="panel-icon mr-4"
                      />
                      <div class="control">
                        {{ $t('forms.labels.track') }}:
                        {{ openTracks.find(x => x.id === form.trackId).name }}
                      </div>
                    </div>
                    <div class="panel-block">
                      <e-status-icon
                        v-model="status.submission"
                        class="panel-icon mr-4"
                      />
                      <div class="control">
                        {{ $t('forms.labels.submissionTitle') }}:
                        {{ form.title }}
                      </div>
                    </div>
                    <div class="panel-block">
                      <e-status-icon
                        v-model="status.submission"
                        class="panel-icon mr-4"
                      />
                      <div class="control">
                        {{ authorStr }}
                      </div>
                    </div>
                    <template v-for="slot in submissionDocumentSlots">
                      <div
                        v-if="slot.id in form.files"
                        :key="slot.id"
                        class="panel-block"
                      >
                        <e-status-icon
                          v-model="status.files[slot.id]"
                          class="panel-icon mr-4"
                        />
                        <div class="control">
                          {{ slot.name }}: {{ form.files[slot.id].name }}
                        </div>
                      </div>
                    </template>
                  </div>
                </b-step-item>
                <b-step-item
                  value="done"
                  :label="$t('pages.submissions-new.steps.done.label')"
                >
                  <b-message type="is-success">
                    {{ $t('pages.submissions-new.steps.done.description') }}
                  </b-message>
                </b-step-item>

                <template v-slot:navigation="{ next }">
                  <div v-show="!isStep('done')" class="is-pulled-right">
                    <b-button @click="onClear">{{
                      $t('pages.submissions-new.clearButton')
                    }}</b-button>
                    <template v-if="!isStep('confirm')">
                      <b-button type="is-primary" @click="onNext(next.action)"
                        >{{ $t('pages.submissions-new.nextStepButton') }}
                      </b-button>
                    </template>
                    <template v-else>
                      <b-button
                        type="is-primary"
                        :disabled="isSubmitting"
                        :loading="isSubmitting"
                        @click="onSubmit(next.action)"
                        >{{ $t('pages.submissions-new.submitButton') }}
                      </b-button>
                    </template>
                  </div>
                </template>
              </b-steps>
            </form>
          </ValidationObserver>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import EUserSearch from '~/components/EUserSearch'
import EStatusIcon from '~/components/EStatusIcon'

function getFirstIfSingleItem(array) {
  return array.length === 1 ? array[0] : null
}

const validContentTypes = {
  PDF: 'application/pdf',
  ODT: 'application/vnd.oasis.opendocument.text',
  DOC: 'application/msword',
  DOCX:
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}
const validExtensions = Object.keys(validContentTypes)
const validMimeTypes = Object.values(validContentTypes)

/**
 * Lista das submissões.
 */
export default {
  components: {
    EUserSearch,
    EStatusIcon
  },
  async asyncData({ app, store }) {
    const openTracks = (
      await app.$api.event.listTracks(store.state.event.slug)
    ).filter(track => track.is_open)
    const preSelectedTrack = getFirstIfSingleItem(openTracks)

    const initialForm = {
      trackId: preSelectedTrack ? preSelectedTrack.id : null,
      title: '',
      authors: [(await app.$auth.fetchUser()).data],
      files: {}
    }
    const form = JSON.parse(JSON.stringify(initialForm))

    const initialStatus = {
      submission: false,
      files: {}
    }
    const status = JSON.parse(JSON.stringify(initialStatus))

    // Workaround to make steps component work with Nuxt SSR (see mounted())
    const stepsWorkaround = {
      // When rendering in the server, include an extra empty first step.
      // Otherwise the actual first step won't render at all (don't know why).
      dummyFirstStep: true,
      // When rendering in the server, generate steps, not just the current one.
      // Otherwise only the first step will be created.
      destroyOnHide: false
    }

    return {
      openTracks,
      form,
      initialForm,
      status,
      initialStatus,
      submissionDocumentSlots: null,
      isSubmitting: false,
      stepsWorkaround,
      validExtensions,
      validMimeTypes
    }
  },
  computed: {
    authorStr() {
      const authors = this.form.authors.map(
        x => `${x.first_name} ${x.last_name}`
      )
      return this.$tc(
        'pages.submissions-new.steps.confirm.authors',
        authors.length,
        { authors: authors.join(', ') }
      )
    }
  },
  watch: {
    'form.trackId': {
      immediate: true,
      handler(trackId) {
        if (trackId) {
          this.$api.track
            .listSubmissionDocumentSlots(trackId)
            .then(slots => (this.submissionDocumentSlots = slots))
        } else {
          this.submissionDocumentSlots = null
        }
      }
    }
  },
  mounted() {
    // Workaround to make steps component work with Nuxt SSR (see asyncData())
    this.stepsWorkaround = {
      // When rendering in the client, don't show the extra first step.
      dummyFirstStep: false,
      // When rendering in the client, destroy steps that aren't the current one.
      // Otherwise the validation will run for fields that are not currently visible,
      // preventing the user from advancing to the next step.
      destroyOnHide: true
    }
  },
  methods: {
    onClear() {
      this.$buefy.dialog.confirm({
        message: this.$t('pages.submissions-new.clearDialogMessage'),
        confirmText: this.$t('dialogs.confirmButton'),
        cancelText: this.$t('dialogs.cancelButton'),
        focusOn: 'confirm',
        type: 'is-primary',
        hasIcon: true,
        onConfirm: () => {
          this.form = this.initialForm
          this.status = this.initialStatus
          this.$refs.steps.activeId = 'details'
          this.$refs.form.reset()
        }
      })
    },
    isStep(stepId) {
      if (this.$refs.steps) {
        return this.$refs.steps.activeId === stepId
      }
      return false
    },
    onNext(goToNextStep) {
      this.$refs.form.validate().then(isValid => {
        if (!isValid) {
          return
        }
        goToNextStep()
      })
    },
    addAuthor(user) {
      const alreadyAdded = this.form.authors.some(
        x => x.public_id === user.public_id
      )
      if (alreadyAdded) {
        return
      }
      this.form.authors.push(user)
    },
    removeAuthor(user) {
      this.form.authors = this.form.authors.filter(
        x => x.public_id !== user.public_id
      )
    },
    async onSubmit(goToNextStep) {
      this.isSubmitting = true

      const documents = {}
      for (const [slotId, file] of Object.entries(this.form.files)) {
        const document = await this.$api.document.create({ file })
        documents[slotId] = document
      }

      const otherAuthors = this.form.authors.filter(
        x => x.public_id !== this.$auth.user.public_id
      )
      const submission = await this.$api.submission.create({
        trackId: this.form.trackId,
        title: this.form.title,
        other_authors: otherAuthors.map(x => x.public_id)
      })
      this.status.submission = true

      for (const [slotId, document] of Object.entries(documents)) {
        await this.$api.submission.addDocument({
          submissionId: submission.id,
          slotId,
          attachmentKey: document.attachment_key
        })
        this.$set(this.status.files, slotId, true)
      }

      setTimeout(() => {
        goToNextStep()
        this.isSubmitting = false
      }, 1000)
    }
  }
}
</script>

<style lang="scss" scoped>
.track-card {
  margin-bottom: 1em;
}
</style>

<style lang="scss">
.b-steps .steps {
  margin-bottom: 1.5em;
}
.b-steps .steps + .step-content {
  margin-bottom: 1em;
  padding: 0 !important;
}
.b-steps .steps + .step-content .step-item {
  border-left: 0.4em solid $primary-light;
  padding: 1em 2em;
}
.b-steps .steps .step-items .step-item .step-marker {
  border: 0.4em solid #fff;
}
</style>
