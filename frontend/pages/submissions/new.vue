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
                  :clickable="false"
                >
                  <b-message v-if="error" type="is-danger">
                    {{ error }}
                  </b-message>
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
                      v-for="track in tracks"
                      :key="track.id"
                      :value="track.id"
                      :disabled="!track.is_open"
                      >{{ track.name }}
                      <template v-if="!track.is_open">{{
                        $t('pages.submissions-new.steps.details.trackClosed')
                      }}</template></option
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
                  :clickable="false"
                >
                  <b-message v-if="error" type="is-danger">
                    {{ error }}
                  </b-message>
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
                  :clickable="false"
                >
                  <b-message v-if="error" type="is-danger">
                    {{ error }}
                  </b-message>
                  <div class="mb-4">
                    {{
                      $tc(
                        'pages.submissions-new.steps.documents.description',
                        openSlots ? openSlots.length : 0
                      )
                    }}
                  </div>
                  <div v-for="slot in openSlots" :key="slot.id" class="mb-3">
                    <e-upload
                      :ref="`field-file-${slot.id}`"
                      v-model="form.files[slot.id]"
                      :loading="status.documentsCreated[slot.id] === false"
                      :name="`file-${slot.id}`"
                      :label="slot.name"
                      :placeholder="
                        $t('pages.submissions-new.steps.documents.chooseFile', {
                          fileTypes: validExtensions.join(', ')
                        })
                      "
                      :rules="'required|mimes:' + validMimeTypes.join(',')"
                      @input="onDocumentSelect(slot.id)"
                    ></e-upload>
                  </div>
                </b-step-item>
                <b-step-item
                  value="confirm"
                  :label="$t('pages.submissions-new.steps.confirm.label')"
                  :clickable="false"
                >
                  <div class="title is-5">
                    {{ $t('pages.submissions-new.steps.confirm.description') }}
                  </div>
                  <b-message v-if="error" type="is-danger">
                    {{ error }}
                  </b-message>
                  <div v-if="form.trackId && form.title" class="panel">
                    <div class="panel-block">
                      <e-status-icon
                        v-model="status.submissionCreated"
                        class="panel-icon mr-4"
                      />
                      <div class="control">
                        {{ $t('forms.labels.track') }}:
                        {{ tracks.find(x => x.id === form.trackId).name }}
                      </div>
                    </div>
                    <div class="panel-block">
                      <e-status-icon
                        v-model="status.submissionCreated"
                        class="panel-icon mr-4"
                      />
                      <div class="control">
                        {{ $t('forms.labels.submissionTitle') }}:
                        {{ form.title }}
                      </div>
                    </div>
                    <div class="panel-block">
                      <e-status-icon
                        v-model="status.submissionCreated"
                        class="panel-icon mr-4"
                      />
                      <div class="control">
                        {{ authorStr }}
                      </div>
                    </div>
                    <template v-for="slot in openSlots">
                      <div
                        v-if="slot.id in form.files"
                        :key="slot.id"
                        class="panel-block"
                      >
                        <e-status-icon
                          v-model="status.documentsLinked[slot.id]"
                          class="panel-icon mr-4"
                        />
                        <div class="control">
                          {{ slot.name }}:
                          {{ form.files[slot.id] && form.files[slot.id].name }}
                        </div>
                      </div>
                    </template>
                  </div>
                </b-step-item>
                <b-step-item
                  value="done"
                  :label="$t('pages.submissions-new.steps.done.label')"
                  :clickable="false"
                >
                  <b-message type="is-success">
                    <div>
                      {{ $t('pages.submissions-new.steps.done.description') }}
                    </div>
                    <div class="is-pulled-right mt-4">
                      <b-button
                        icon-left="plus"
                        class="mr-2"
                        @click="doClear"
                        >{{
                          $t(
                            'pages.submissions-new.steps.done.addAnotherSubmissionButton'
                          )
                        }}</b-button
                      >
                      <b-button
                        type="is-primary"
                        icon-left="arrow-right"
                        tag="nuxt-link"
                        :to="localePath({ name: 'user-submissions' })"
                        >{{
                          $t(
                            'pages.submissions-new.steps.done.viewSubmissionsButton'
                          )
                        }}</b-button
                      >
                    </div>
                  </b-message>
                </b-step-item>

                <template v-slot:navigation="{ previous, next }">
                  <div v-show="!isStep('done')" class="is-pulled-right">
                    <b-button
                      type="is-danger"
                      class="mr-3"
                      icon-left="cancel"
                      outlined
                      @click="onClear"
                      >{{ $t('pages.submissions-new.clearButton') }}</b-button
                    >

                    <b-button
                      type="is-primary is-light"
                      class="mr-2"
                      icon-left="arrow-left"
                      :disabled="error"
                      @click="onPrevious(previous.action)"
                      >{{ $t('pages.submissions-new.previousStepButton') }}
                    </b-button>

                    <template v-if="!isStep('confirm')">
                      <b-button
                        type="is-primary"
                        icon-left="arrow-right"
                        :disabled="error"
                        @click="onNext(next.action)"
                        >{{ $t('pages.submissions-new.nextStepButton') }}
                      </b-button>
                    </template>
                    <template v-else>
                      <b-button
                        type="is-primary"
                        icon-left="check"
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
import errorMixin from '~/mixins/errorMixin'

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
  mixins: [errorMixin],
  async asyncData({ app, error, store }) {
    let pageError = null
    let tracks
    try {
      tracks = await app.$api.event.listTracks(store.state.event.slug)
    } catch (err) {
      error({
        message: app.i18n.t('genericErrors.network')
      })
      return
    }
    const openTracks = tracks.filter(track => track.is_open)

    if (openTracks.length === 0) {
      pageError = app.i18n.t('pages.submissions-new.errorNoOpenTracks')
    }

    const preSelectedTrack = getFirstIfSingleItem(openTracks)

    const initialForm = {
      trackId: preSelectedTrack ? preSelectedTrack.id : null,
      title: '',
      authors: [(await app.$auth.fetchUser()).data],
      files: {}
    }
    const form = JSON.parse(JSON.stringify(initialForm))

    const initialStatus = {
      submissionCreated: false,
      documentsCreated: {},
      documentsLinked: {}
    }
    const status = JSON.parse(JSON.stringify(initialStatus))

    return {
      tracks,
      form,
      initialForm,
      status,
      initialStatus,
      uploadedDocuments: {},
      error: pageError,
      openSlots: null,
      isSubmitting: false,
      // Workaround to make steps component work with Nuxt SSR (see mounted())
      stepsWorkaround: {
        // When rendering in the server, include an extra empty first step.
        // Otherwise the actual first step won't render at all (don't know why).
        dummyFirstStep: true,
        // When rendering in the server, generate steps, not just the current one.
        // Otherwise only the first step will be created.
        destroyOnHide: false
      },
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
      async handler(trackId) {
        let openSlots = null
        if (trackId) {
          try {
            const slots = await this.$api.track.listSubmissionDocumentSlots(
              trackId
            )
            openSlots = slots.filter(x => x.is_open)
          } catch (err) {
            this.handleGenericError(err)
          }
        }
        this.openSlots = openSlots
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
    doClear() {
      this.error = null
      this.form = JSON.parse(JSON.stringify(this.initialForm))
      this.status = JSON.parse(JSON.stringify(this.initialStatus))
      this.uploadedDocuments = {}
      this.$refs.steps.activeId = 'details'
      this.$refs.form.reset()
    },
    onClear() {
      this.$buefy.dialog.confirm({
        message: this.$t('pages.submissions-new.clearDialogMessage'),
        confirmText: this.$t('dialogs.confirmButton'),
        cancelText: this.$t('dialogs.cancelButton'),
        focusOn: 'confirm',
        type: 'is-primary',
        hasIcon: true,
        onConfirm: this.doClear
      })
    },
    isStep(stepId) {
      if (this.$refs.steps) {
        return this.$refs.steps.activeId === stepId
      }
      return false
    },
    onPrevious(goToPreviousStep) {
      goToPreviousStep()
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
    async onDocumentSelect(slotId) {
      const field = this.$refs[`field-file-${slotId}`][0]
      const validationProvider = field.$refs.provider
      const { valid: isValid } = await validationProvider.validate()
      if (!isValid) {
        return
      }

      this.$set(this.status.documentsCreated, slotId, false)

      const file = this.form.files[slotId]
      try {
        const document = await this.$api.document.create({ file })
        this.uploadedDocuments[slotId] = document
        this.$set(this.status.documentsCreated, slotId, true)
      } catch (err) {
        if (
          err.name === 'APIValidationError' &&
          err.fields &&
          err.fields.file
        ) {
          this.$refs.form.setErrors({
            [`file-${slotId}`]: err.fields.file
          })
        } else {
          this.$delete(this.form.files, slotId)
          this.handleGenericError(err)
        }
        this.$set(this.status.documentsCreated, slotId, null)
      }
    },
    async onSubmit(goToNextStep) {
      this.isSubmitting = true

      const otherAuthors = this.form.authors.filter(
        x => x.public_id !== this.$auth.user.public_id
      )
      try {
        await this.$api.submission.create({
          trackId: this.form.trackId,
          title: this.form.title,
          other_authors: otherAuthors.map(x => x.public_id),
          documents: Object.entries(this.uploadedDocuments).map(
            ([slotId, document]) => ({
              slot: slotId,
              document_attachment_key: document.attachment_key
            })
          )
        })
        this.status.submissionCreated = true
      } catch (err) {
        this.status.submissionCreated = false
        this.isSubmitting = false
        this.handleGenericError(err)
        return
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
