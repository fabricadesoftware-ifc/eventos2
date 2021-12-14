<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-tracks-id-manage-review-questions.title') }}
          </h1>

          <div v-visible="!loading" class="mb-4">
            <b-message v-if="error" type="is-danger">
              {{ error }}
            </b-message>
            <b-message v-else type="is-info">
              {{
                $t('pages.admin-tracks-id-manage-review-questions.description')
              }}
            </b-message>
          </div>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form class="mb-6" @submit.prevent="handleSubmit(onSubmit)">
              <e-input
                v-model="form.text"
                name="text"
                :label="$t('forms.labels.trackReviewQuestionText')"
                rules="required"
              />
              <e-radio-group
                name="answer_type"
                :label="$t('forms.labels.trackReviewQuestionAnswerType')"
                rules="required"
                :addons="false"
              >
                <div class="control">
                  <b-radio v-model="form.answer_type" native-value="text">{{
                    $t(
                      'pages.admin-tracks-id-manage-review-questions.answerTypes.text'
                    )
                  }}</b-radio
                  ><br />
                  <b-radio v-model="form.answer_type" native-value="yes_no">{{
                    $t(
                      'pages.admin-tracks-id-manage-review-questions.answerTypes.yesNo'
                    )
                  }}</b-radio
                  ><br />
                  <b-radio
                    v-model="form.answer_type"
                    native-value="grade_zero_to_ten"
                    >{{
                      $t(
                        'pages.admin-tracks-id-manage-review-questions.answerTypes.gradeZeroToTen'
                      )
                    }}</b-radio
                  >
                </div>
              </e-radio-group>

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{
                      $t(
                        'pages.admin-tracks-id-manage-review-questions.submitButton'
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
                'pages.admin-tracks-id-manage-review-questions.titleCurrentSlots'
              )
            }}
          </h2>
          <b-table :data="items" :show-header="items.length !== 0">
            <b-table-column
              v-slot="props"
              :label="
                $t('pages.admin-tracks-id-manage-review-questions.labels.text')
              "
            >
              {{ props.row.text }}
            </b-table-column>
            <b-table-column
              v-slot="props"
              :label="
                $t(
                  'pages.admin-tracks-id-manage-review-questions.labels.answerType'
                )
              "
            >
              {{ props.row.answer_type }}
            </b-table-column>
            <template #empty>
              <div class="has-text-grey">
                {{
                  $t(
                    'pages.admin-tracks-id-manage-review-questions.emptyMessage'
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

const questionToItem = ({ i18n, question }) => {
  const answerTypeKey =
    {
      text: 'text',
      yes_no: 'yesNo',
      grade_zero_to_ten: 'gradeZeroToTen'
    }[question.answer_type] || null

  let answerTypeValue = null
  if (answerTypeKey !== null) {
    const answerTypePathPrefix =
      'pages.admin-tracks-id-manage-review-questions.answerTypes.'
    answerTypeValue = i18n.t(answerTypePathPrefix + answerTypeKey)
  }
  return {
    ...question,
    answer_type: answerTypeValue
  }
}

export default {
  mixins: [errorMixin],
  layout: 'admin',

  async asyncData({ app, params, store }) {
    const track = await app.$api.track.getById(params.id)
    const items = await app.$api.track
      .listReviewQuestions(params.id)
      .then(questions =>
        questions.map(question => questionToItem({ i18n: app.i18n, question }))
      )
    return {
      loading: false,
      error: null,
      track,
      form: {
        text: '',
        answer_type: null
      },
      items
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.trackReviewQuestion
        .create({ trackId: this.track.id, ...this.form })
        .then(question =>
          this.items.push(questionToItem({ i18n: this.$i18n, question }))
        )
        .catch(this.handleGenericError)
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>
