<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-activities-id-edit.title') }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-activities-id-edit.description') }}
                </b-message>
              </div>

              <e-input
                v-model="form.name"
                name="name"
                :label="$t('forms.labels.activityName')"
                rules="required"
              />
              <e-input
                v-model="form.name_english"
                name="name_english"
                :label="$t('forms.labels.activityNameInEnglish')"
                rules="required"
              />
              <e-datetimepicker
                v-model="form.starts_on"
                name="starts_on"
                :label="$t('forms.labels.activityStartDate')"
              />
              <e-datetimepicker
                v-model="form.ends_on"
                name="ends_on"
                :label="$t('forms.labels.activityEndDate')"
              />

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{
                      $t('pages.admin-activities-id-edit.submitButton')
                    }}</b-button
                  >
                </div>
              </div>
            </form>
          </ValidationObserver>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import errorMixin from '~/mixins/errorMixin'

export default {
  mixins: [errorMixin],
  layout: 'admin',

  async asyncData({ app, params }) {
    const activity = await app.$api.activity.getById(params.id)
    return {
      loading: false,
      error: null,
      activity,
      form: {
        name: activity.name,
        name_english: activity.name_english,
        starts_on: new Date(activity.starts_on),
        ends_on: new Date(activity.ends_on)
      }
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.activity
        .update(this.activity.id, this.form)
        .then(() =>
          this.$router.push(
            this.localePath({
              name: 'admin-activities-id-manage',
              params: { id: this.activity.id }
            })
          )
        )
        .catch(this.handleGenericError)
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>
