<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-activities-id.title') }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-activities-id.description') }}
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
              <e-input
                v-model="form.slug"
                name="slug"
                :label="$t('forms.labels.activitySlug')"
              />

              <no-ssr>
                <b-field :label="$t('forms.labels.activityStartDate')">
                  <b-datetimepicker
                    v-model="form.starts_on"
                    name="starts_on"
                    :datetime-formatter="dateTimeFormatter"
                  ></b-datetimepicker>
                </b-field>
                <b-field :label="$t('forms.labels.activityEndDate')">
                  <b-datetimepicker
                    v-model="form.ends_on"
                    name="ends_on"
                    :datetime-formatter="dateTimeFormatter"
                  ></b-datetimepicker>
                </b-field>
              </no-ssr>

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{
                      $t('pages.admin-activities-id.submitButton')
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
export default {
  layout: 'admin',
  async asyncData({ app, params }) {
    const activity = await app.$api.activity.getBySlug(params.slug)
    return {
      loading: false,
      error: null,
      currentSlug: activity.slug,
      form: {
        name: activity.name,
        name_english: activity.name_english,
        slug: activity.slug,
        starts_on: new Date(activity.starts_on),
        ends_on: new Date(activity.ends_on)
      }
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.activity
        .update(this.currentSlug, this.form)
        .then(() =>
          this.$router.push(
            this.localePath({
              name: 'admin-activities-slug',
              params: { slug: this.form.slug }
            })
          )
        )
        .catch(this.handleError)
        .finally(() => {
          this.loading = false
        })
    },
    handleError(error) {
      switch (error.name) {
        case 'APIValidationError':
          this.error = error.message || this.$t('genericErrors.formValidation')
          this.$refs.form.setErrors(error.fields)
          break
        case 'APIError':
          this.error = this.$t('genericErrors.api')
          break
        default:
          this.error = this.$t('genericErrors.network')
      }
    },
    dateTimeFormatter(date) {
      return date.toLocaleDateString(undefined, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        timeZoneName: 'long'
      })
    }
  }
}
</script>
