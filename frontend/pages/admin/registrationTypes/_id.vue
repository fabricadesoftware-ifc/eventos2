<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{
              $t('pages.admin-registrationTypes-id.title', {
                registrationTypeName: original.name,
                registrationTypeNameInEnglish: original.name_english
              })
            }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-registrationTypes-id.description') }}
                </b-message>
              </div>

              <e-input
                v-model="form.name"
                name="eventRegistrationTypeName"
                :label="$t('forms.labels.eventRegistrationTypeName')"
                rules="required"
              />
              <e-input
                v-model="form.nameInEnglish"
                name="eventRegistrationTypeNameInEnglish"
                :label="$t('forms.labels.eventRegistrationTypeNameInEnglish')"
                rules="required"
              />

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{
                      $t('pages.admin-registrationTypes-id.submitButton')
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
  asyncData({ params, store }) {
    return {
      original: store.state.event.registration_types.filter(
        x => x.id.toString() === params.id
      )[0]
    }
  },
  data() {
    return {
      loading: false,
      error: null,
      form: {
        name: null,
        nameInEnglish: null
      }
    }
  },
  created() {
    this.form.name = this.original.name
    this.form.nameInEnglish = this.original.name_english
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$store
        .dispatch('admin/updateEventRegistrationType', {
          eventRegistrationTypeId: this.original.id,
          ...this.form
        })
        .then(() =>
          this.$router.push(
            this.localePath({ name: 'admin-registrationTypes' })
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
    }
  }
}
</script>
