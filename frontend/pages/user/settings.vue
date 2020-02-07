<template>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-8">
        <main class="section">
          <h1 class="title">{{ $t('pages.user-settings.title') }}</h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <e-input
                v-model="form.first_name"
                name="firstName"
                :label="$t('forms.labels.firstName')"
                rules="required"
                horizontal
              />
              <e-input
                v-model="form.last_name"
                name="lastName"
                :label="$t('forms.labels.lastName')"
                rules="required"
                horizontal
              />
              <div class="field is-horizontal">
                <div class="field-label"></div>
                <div class="field-body">
                  <div class="field">
                    <b-button
                      type="is-primary is-fullwidth"
                      native-type="submit"
                      icon-left="wrench"
                      :loading="loading"
                      >{{ $t('pages.user-settings.submitButton') }}</b-button
                    >
                  </div>
                </div>
                <div class="control"></div>
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
  data() {
    return {
      loading: false,
      form: {
        first_name: '',
        last_name: ''
      }
    }
  },
  created() {
    this.form = {
      first_name: this.$auth.user.first_name,
      last_name: this.$auth.user.last_name
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.user
        .update(this.form)
        .then(() => this.$auth.fetchUser())
        .catch(this.handleError)
        .finally(() => (this.loading = false))
    },
    handleError(error) {
      switch (error.name) {
        case 'APIValidationError':
          this.error = error.message
          this.$refs.form.setErrors(error.fields)
          break
        case 'APIError':
          this.error = this.$t('genericErrors.api')
          break
        default:
          this.error = this.$t('genericErrors.network')
      }
    }
  }
}
</script>
