<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{
              $t('pages.admin-tracks-id-manage-submission-document-slots.title')
            }}
          </h1>

          <div v-visible="!loading" class="mb-4">
            <b-message v-if="error" type="is-danger">
              {{ error }}
            </b-message>
            <b-message v-else type="is-info">
              {{
                $t(
                  'pages.admin-tracks-id-manage-submission-document-slots.description'
                )
              }}
            </b-message>
          </div>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form class="mb-6" @submit.prevent="handleSubmit(onSubmit)">
              <e-input
                v-model="form.name"
                name="name"
                :label="$t('forms.labels.trackName')"
                rules="required"
              />
              <e-input
                v-model="form.name_english"
                name="name_english"
                :label="$t('forms.labels.trackNameInEnglish')"
                rules="required"
              />
              <e-datetimepicker
                v-model="form.starts_on"
                name="starts_on"
                :label="$t('forms.labels.trackStartDate')"
              />
              <e-datetimepicker
                v-model="form.ends_on"
                name="ends_on"
                :label="$t('forms.labels.trackEndDate')"
              />

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{
                      $t(
                        'pages.admin-tracks-id-manage-submission-document-slots.submitButton'
                      )
                    }}</b-button
                  >
                </div>
              </div>
            </form>
          </ValidationObserver>

          <h2 class="title is-4">
            {{
              $t(
                'pages.admin-tracks-id-manage-submission-document-slots.titleCurrentSlots'
              )
            }}
          </h2>
          <b-table :data="items" :show-header="items.length !== 0">
            <b-table-column
              v-slot="props"
              :label="
                $t(
                  'pages.admin-tracks-id-manage-submission-document-slots.labels.name'
                )
              "
            >
              {{ props.row.name }}
            </b-table-column>
            <b-table-column
              v-slot="props"
              :label="
                $t(
                  'pages.admin-tracks-id-manage-submission-document-slots.labels.startDate'
                )
              "
            >
              {{ props.row.starts_on }}
            </b-table-column>
            <b-table-column
              v-slot="props"
              :label="
                $t(
                  'pages.admin-tracks-id-manage-submission-document-slots.labels.endDate'
                )
              "
            >
              {{ props.row.ends_on }}
            </b-table-column>
            <template v-slot:empty>
              <div class="has-text-grey">
                {{
                  $t(
                    'pages.admin-tracks-id-manage-submission-document-slots.emptyMessage'
                  )
                }}
              </div>
            </template>
          </b-table>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import errorMixin from '~/mixins/errorMixin'

const slotToItem = ({ locale, dayjs, slot }) => {
  if (locale === 'en' && slot.name_english) {
    slot.name = slot.name_english
  }
  delete slot.name_english
  slot.starts_on = dayjs(slot.starts_on).format('llll')
  slot.ends_on = dayjs(slot.ends_on).format('llll')
  return slot
}

export default {
  layout: 'admin',
  mixins: [errorMixin],

  async asyncData({ app, params, store }) {
    const track = await app.$api.track.getById(params.id)
    const slots = await app.$api.track
      .listSubmissionDocumentSlots(params.id)
      .then(slots =>
        slots.map(slot =>
          slotToItem({ locale: store.state.locale, dayjs: app.$dayjs, slot })
        )
      )
    return {
      loading: false,
      error: null,
      track,
      form: {
        name: '',
        name_english: '',
        starts_on: new Date(track.starts_on),
        ends_on: new Date(track.ends_on)
      },
      items: slots
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.trackSubmissionDocumentSlot
        .create({ trackId: this.track.id, ...this.form })
        .then(slot =>
          slotToItem({
            locale: this.$store.state.locale,
            dayjs: this.$dayjs,
            slot
          })
        )
        .then(item => this.items.push(item))
        .catch(this.handleGenericError)
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>
