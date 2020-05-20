<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-activities-new.title') }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-activities-new.description') }}
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
                    icon-left="plus"
                    :loading="loading"
                    >{{
                      $t('pages.admin-activities-new.submitButton')
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
  data() {
    return {
      loading: false,
      error: null,
      form: {
        name: '',
        name_english: '',
        slug: '',
        starts_on: new Date(),
        ends_on: new Date()
      }
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.activity
        .create({ eventId: this.$store.state.event.id, ...this.form })
        .then(() =>
          this.$router.push(this.localePath({ name: 'admin-activities' }))
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
